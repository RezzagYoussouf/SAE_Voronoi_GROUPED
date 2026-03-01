from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.spatial import Voronoi


@dataclass(frozen=True, slots=True)
class Bounds:
    min_x: float
    min_y: float
    max_x: float
    max_y: float


def compute_bounds(points: np.ndarray, padding: float = 10.0) -> Bounds:
    if points.size == 0:
        raise ValueError("Cannot compute bounds for empty points array.")
    min_x = float(np.min(points[:, 0])) - float(padding)
    max_x = float(np.max(points[:, 0])) + float(padding)
    min_y = float(np.min(points[:, 1])) - float(padding)
    max_y = float(np.max(points[:, 1])) + float(padding)

    # Avoid degenerate bounds
    if max_x - min_x < 1e-9:
        max_x += 1.0
        min_x -= 1.0
    if max_y - min_y < 1e-9:
        max_y += 1.0
        min_y -= 1.0

    return Bounds(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)


def parse_bounds(text: str) -> Bounds:
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 4:
        raise ValueError("Bounds must have 4 comma-separated values: minx,miny,maxx,maxy.")
    try:
        min_x, min_y, max_x, max_y = map(float, parts)
    except ValueError as exc:
        raise ValueError("Bounds values must be numeric.") from exc
    if max_x <= min_x or max_y <= min_y:
        raise ValueError("Bounds must satisfy maxx>minx and maxy>miny.")
    return Bounds(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)


def _sort_polygon_vertices(poly: np.ndarray) -> np.ndarray:
    # Sort vertices counter-clockwise for nice rendering
    if poly.shape[0] < 3:
        return poly
    center = np.mean(poly, axis=0)
    angles = np.arctan2(poly[:, 1] - center[1], poly[:, 0] - center[0])
    order = np.argsort(angles)
    return poly[order]


def _clip_polygon_halfplane(poly: np.ndarray, inside_fn, intersect_fn) -> np.ndarray:
    if poly.size == 0:
        return poly
    output: list[np.ndarray] = []
    n = poly.shape[0]
    for i in range(n):
        curr = poly[i]
        prev = poly[i - 1]
        curr_in = inside_fn(curr)
        prev_in = inside_fn(prev)

        if curr_in:
            if not prev_in:
                output.append(intersect_fn(prev, curr))
            output.append(curr)
        elif prev_in:
            output.append(intersect_fn(prev, curr))

    if not output:
        return np.empty((0, 2), dtype=float)
    return np.vstack(output)


def clip_polygon_to_bounds(poly: np.ndarray, b: Bounds) -> np.ndarray:
    # Sutherland–Hodgman clipping against axis-aligned rectangle
    poly = poly.astype(float, copy=False)

    # Left: x >= min_x
    def inside(p): return p[0] >= b.min_x
    def intersect(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if abs(x2 - x1) < 1e-12:
            return np.array([b.min_x, y1], dtype=float)
        t = (b.min_x - x1) / (x2 - x1)
        return np.array([b.min_x, y1 + t * (y2 - y1)], dtype=float)
    poly = _clip_polygon_halfplane(poly, inside, intersect)

    # Right: x <= max_x
    def inside(p): return p[0] <= b.max_x
    def intersect(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if abs(x2 - x1) < 1e-12:
            return np.array([b.max_x, y1], dtype=float)
        t = (b.max_x - x1) / (x2 - x1)
        return np.array([b.max_x, y1 + t * (y2 - y1)], dtype=float)
    poly = _clip_polygon_halfplane(poly, inside, intersect)

    # Bottom: y >= min_y
    def inside(p): return p[1] >= b.min_y
    def intersect(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if abs(y2 - y1) < 1e-12:
            return np.array([x1, b.min_y], dtype=float)
        t = (b.min_y - y1) / (y2 - y1)
        return np.array([x1 + t * (x2 - x1), b.min_y], dtype=float)
    poly = _clip_polygon_halfplane(poly, inside, intersect)

    # Top: y <= max_y
    def inside(p): return p[1] <= b.max_y
    def intersect(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if abs(y2 - y1) < 1e-12:
            return np.array([x1, b.max_y], dtype=float)
        t = (b.max_y - y1) / (y2 - y1)
        return np.array([x1 + t * (x2 - x1), b.max_y], dtype=float)
    poly = _clip_polygon_halfplane(poly, inside, intersect)

    # Remove duplicates (can appear after clipping)
    if poly.shape[0] < 3:
        return poly
    cleaned: list[np.ndarray] = []
    for p in poly:
        if not cleaned or np.linalg.norm(p - cleaned[-1]) > 1e-9:
            cleaned.append(p)
    if len(cleaned) >= 2 and np.linalg.norm(cleaned[0] - cleaned[-1]) < 1e-9:
        cleaned.pop()
    if len(cleaned) < 3:
        return np.empty((0, 2), dtype=float)

    return _sort_polygon_vertices(np.vstack(cleaned))


def voronoi_finite_polygons_2d(vor: Voronoi, radius: float | None = None) -> tuple[list[list[int]], np.ndarray]:
    """
    Reconstruct infinite Voronoi regions in a 2D diagram to finite regions.
    Returns (regions, vertices) where regions is a list of indices into vertices.
    """
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input.")

    new_regions: list[list[int]] = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = float(np.ptp(vor.points, axis=0).max()) * 2.0

    # Map: point index -> ridges
    all_ridges: dict[int, list[tuple[int, int, int]]] = {i: [] for i in range(vor.points.shape[0])}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges[p1].append((p2, v1, v2))
        all_ridges[p2].append((p1, v1, v2))

    for p1, region_index in enumerate(vor.point_region):
        region = vor.regions[region_index]
        if not region:
            new_regions.append([])
            continue

        if all(v >= 0 for v in region):
            new_regions.append(region)
            continue

        # Reconstruct infinite region
        ridges = all_ridges[p1]
        new_region = [v for v in region if v >= 0]

        for p2, v1, v2 in ridges:
            if v1 >= 0 and v2 >= 0:
                continue

            # Compute the missing endpoint for an infinite ridge
            t = vor.points[p2] - vor.points[p1]
            t_norm = np.linalg.norm(t)
            if t_norm == 0:
                continue
            t = t / t_norm
            n = np.array([-t[1], t[0]])

            midpoint = (vor.points[p1] + vor.points[p2]) / 2.0
            direction = np.sign(np.dot(midpoint - center, n)) * n
            finite_vertex = vor.vertices[v1 if v1 >= 0 else v2]
            far_point = finite_vertex + direction * radius

            new_vertices.append(far_point.tolist())
            new_region.append(len(new_vertices) - 1)

        new_regions.append(new_region)

    return new_regions, np.asarray(new_vertices, dtype=float)
