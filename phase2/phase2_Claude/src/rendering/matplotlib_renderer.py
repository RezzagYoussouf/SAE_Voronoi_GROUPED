"""
Module: matplotlib_renderer.py
Responsibility: Render a VoronoiResult using Matplotlib.
SOLID:
  SRP  – only creates the Figure; no file I/O.
  LSP  – substitutable for any BaseRenderer consumer.
Design patterns:
  Strategy – MatplotlibRenderer is one concrete strategy for the rendering step.
"""

from __future__ import annotations

import string

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from matplotlib.colors import to_rgba
from scipy.spatial import Voronoi

from src.models.voronoi_result import VoronoiResult
from src.rendering.base_renderer import BaseRenderer

# ── Visual constants (no magic numbers) ─────────────────────────────────────
FIGURE_SIZE_INCHES = (10, 8)
FIGURE_DPI = 100
POINT_MARKER = "o"
POINT_SIZE = 9
POINT_ZORDER = 5
LABEL_ZORDER = 6
LABEL_FONTSIZE = 10
LABEL_OFFSET_FACTOR = 0.015   # fraction of axis range for label nudge
CELL_ALPHA = 0.30             # fill transparency for Voronoi cells
EDGE_COLOR = "#333333"
EDGE_LINEWIDTH = 1.2
EDGE_ALPHA = 0.9
EDGE_ZORDER = 3
BACKGROUND_COLOR = "white"
TITLE_FONT_SIZE = 13

# How far to extend infinite Voronoi edges (in data units)
INFINITE_EDGE_EXTENSION_FACTOR = 0.25

# Colour palette – tab10 gives 10 visually distinct colours
COLOR_PALETTE = plt.get_cmap("tab10")


def _point_label(index: int) -> str:
    """Return 'A', 'B', … 'Z', 'AA', 'AB', … for any non-negative index."""
    letters = string.ascii_uppercase
    label = ""
    n = index
    while True:
        label = letters[n % 26] + label
        n = n // 26 - 1
        if n < 0:
            break
    return label


class MatplotlibRenderer(BaseRenderer):
    """
    Renders a VoronoiResult to a matplotlib Figure with per-point colours.

    Each input point gets:
      • a unique colour drawn from the tab10 palette,
      • its Voronoi cell filled with that colour (semi-transparent),
      • a labelled marker (A, B, C …) at its location.

    Handles infinite Voronoi ridges by clipping them to a bounding box
    slightly larger than the input point cloud.
    """

    def __init__(self, show_axes: bool = True) -> None:
        self._show_axes = show_axes

    # ── BaseRenderer contract ────────────────────────────────────────────────

    def render(self, result: VoronoiResult) -> Figure:
        """Build and return a matplotlib Figure for the given VoronoiResult."""
        fig, ax = self._create_figure()
        vor = result.scipy_voronoi
        bounds = self._compute_bounds(vor)
        colors = self._build_color_map(len(result.points))

        self._fill_cells(ax, vor, bounds, colors)
        self._draw_ridges(ax, vor, bounds)
        self._draw_labeled_points(ax, vor, bounds, colors)
        self._draw_legend(ax, vor, colors)
        self._apply_styling(ax, bounds)

        return fig

    # ── Private helpers ──────────────────────────────────────────────────────

    def _create_figure(self) -> tuple[Figure, plt.Axes]:
        """Create and configure a new Figure/Axes pair."""
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_INCHES, dpi=FIGURE_DPI)
        fig.patch.set_facecolor(BACKGROUND_COLOR)
        ax.set_facecolor(BACKGROUND_COLOR)
        return fig, ax

    @staticmethod
    def _build_color_map(n: int) -> list:
        """Return a list of *n* RGBA colours from the tab10 palette."""
        return [COLOR_PALETTE(i % 10) for i in range(n)]

    @staticmethod
    def _compute_bounds(vor: Voronoi) -> tuple[float, float, float, float]:
        """Return (xmin, xmax, ymin, ymax) with a margin around the point cloud."""
        pts = vor.points
        x_range = pts[:, 0].max() - pts[:, 0].min()
        y_range = pts[:, 1].max() - pts[:, 1].min()
        margin = max(x_range, y_range) * INFINITE_EDGE_EXTENSION_FACTOR + 1.0
        return (
            pts[:, 0].min() - margin,
            pts[:, 0].max() + margin,
            pts[:, 1].min() - margin,
            pts[:, 1].max() + margin,
        )

    # ── Cell filling ─────────────────────────────────────────────────────────

    def _fill_cells(
        self,
        ax: plt.Axes,
        vor: Voronoi,
        bounds: tuple[float, float, float, float],
        colors: list,
    ) -> None:
        """Fill each finite Voronoi region with the colour of its seed point."""
        for point_idx, region_idx in enumerate(vor.point_region):
            region = vor.regions[region_idx]

            # Skip empty or infinite regions
            if not region or -1 in region:
                continue

            polygon = vor.vertices[region]
            color = to_rgba(colors[point_idx], alpha=CELL_ALPHA)
            ax.fill(polygon[:, 0], polygon[:, 1], color=color, zorder=1)

    # ── Ridge drawing ─────────────────────────────────────────────────────────

    def _draw_ridges(
        self,
        ax: plt.Axes,
        vor: Voronoi,
        bounds: tuple[float, float, float, float],
    ) -> None:
        """Draw all Voronoi ridges, clipping infinite ones to bounds."""
        center = vor.points.mean(axis=0)

        for point_index_pair, vertex_index_pair in zip(
            vor.ridge_points, vor.ridge_vertices
        ):
            i, j = vertex_index_pair
            if i >= 0 and j >= 0:
                self._draw_finite_ridge(ax, vor.vertices[i], vor.vertices[j])
            else:
                self._draw_infinite_ridge(
                    ax, vor, i, j, point_index_pair, center, bounds
                )

    def _draw_finite_ridge(
        self, ax: plt.Axes, v_start: np.ndarray, v_end: np.ndarray
    ) -> None:
        ax.plot(
            [v_start[0], v_end[0]],
            [v_start[1], v_end[1]],
            color=EDGE_COLOR,
            linewidth=EDGE_LINEWIDTH,
            alpha=EDGE_ALPHA,
            zorder=EDGE_ZORDER,
        )

    def _draw_infinite_ridge(
        self,
        ax: plt.Axes,
        vor: Voronoi,
        i: int,
        j: int,
        point_index_pair: np.ndarray,
        center: np.ndarray,
        bounds: tuple[float, float, float, float],
    ) -> None:
        finite_vertex = vor.vertices[max(i, j)]
        p1 = vor.points[point_index_pair[0]]
        p2 = vor.points[point_index_pair[1]]

        tangent = p2 - p1
        normal = np.array([-tangent[1], tangent[0]])
        normal /= np.linalg.norm(normal)

        midpoint = (p1 + p2) / 2.0
        if np.dot(midpoint - center, normal) < 0:
            normal = -normal

        xmin, xmax, ymin, ymax = bounds
        max_extent = max(xmax - xmin, ymax - ymin) * 2
        far_point = finite_vertex + normal * max_extent

        ax.plot(
            [finite_vertex[0], far_point[0]],
            [finite_vertex[1], far_point[1]],
            color=EDGE_COLOR,
            linewidth=EDGE_LINEWIDTH,
            alpha=EDGE_ALPHA,
            zorder=EDGE_ZORDER,
        )

    # ── Point markers & labels ────────────────────────────────────────────────

    def _draw_labeled_points(
        self,
        ax: plt.Axes,
        vor: Voronoi,
        bounds: tuple[float, float, float, float],
        colors: list,
    ) -> None:
        """Draw each seed point as a coloured marker with its letter label."""
        xmin, xmax, ymin, ymax = bounds
        x_offset = (xmax - xmin) * LABEL_OFFSET_FACTOR
        y_offset = (ymax - ymin) * LABEL_OFFSET_FACTOR

        for idx, (x, y) in enumerate(vor.points):
            color = colors[idx]
            label = _point_label(idx)

            ax.plot(
                x, y,
                marker=POINT_MARKER,
                color=color,
                markeredgecolor="black",
                markeredgewidth=0.8,
                markersize=POINT_SIZE,
                linestyle="None",
                zorder=POINT_ZORDER,
            )
            ax.text(
                x + x_offset,
                y + y_offset,
                label,
                fontsize=LABEL_FONTSIZE,
                fontweight="bold",
                color=color,
                zorder=LABEL_ZORDER,
                bbox=dict(
                    boxstyle="round,pad=0.15",
                    facecolor="white",
                    edgecolor=color,
                    linewidth=0.8,
                    alpha=0.85,
                ),
            )

    # ── Legend ───────────────────────────────────────────────────────────────

    @staticmethod
    def _draw_legend(ax: plt.Axes, vor: Voronoi, colors: list) -> None:
        """Build a legend that maps each letter to its (x, y) coordinates."""
        handles = []
        for idx, (x, y) in enumerate(vor.points):
            label = _point_label(idx)
            patch = mpatches.Patch(
                color=colors[idx],
                label=f"{label}  ({x:.2g}, {y:.2g})",
            )
            handles.append(patch)
        ax.legend(
            handles=handles,
            loc="upper right",
            fontsize=8,
            framealpha=0.9,
            title="Points",
            title_fontsize=9,
        )

    # ── Styling ──────────────────────────────────────────────────────────────

    def _apply_styling(
        self,
        ax: plt.Axes,
        bounds: tuple[float, float, float, float],
    ) -> None:
        """Set axis limits, title, grid."""
        xmin, xmax, ymin, ymax = bounds
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_title("Voronoi Diagram", fontsize=TITLE_FONT_SIZE)

        if self._show_axes:
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True, linestyle="--", alpha=0.35)
        else:
            ax.axis("off")
