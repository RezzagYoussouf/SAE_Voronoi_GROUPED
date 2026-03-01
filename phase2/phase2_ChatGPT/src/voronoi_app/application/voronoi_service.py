from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.spatial import Voronoi

from voronoi_app.domain.models import Point
from voronoi_app.utils.geometry import (
    Bounds,
    clip_polygon_to_bounds,
    compute_bounds,
    voronoi_finite_polygons_2d,
)


@dataclass(frozen=True, slots=True)
class VoronoiResult:
    points: np.ndarray               # shape (n,2)
    polygons: list[np.ndarray]       # list of (m_i,2) polygons (clipped)
    bounds: Bounds


class VoronoiService:
    def compute(self, points: list[Point], bounds: Bounds | None, padding: float = 10.0) -> VoronoiResult:
        pts = np.array([[p.x, p.y] for p in points], dtype=float)

        b = bounds if bounds is not None else compute_bounds(pts, padding=padding)

        vor = Voronoi(pts)
        regions, vertices = voronoi_finite_polygons_2d(vor)

        polygons: list[np.ndarray] = []
        for region in regions:
            if not region:
                polygons.append(np.empty((0, 2), dtype=float))
                continue
            poly = vertices[np.array(region, dtype=int)]
            poly = clip_polygon_to_bounds(poly, b)
            polygons.append(poly)

        return VoronoiResult(points=pts, polygons=polygons, bounds=b)
