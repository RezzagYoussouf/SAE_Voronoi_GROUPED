from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from voronoi_app.application.voronoi_service import VoronoiResult


@dataclass(frozen=True, slots=True)
class PlotStyle:
    show_axes: bool = True
    show_labels: bool = True
    show_grid: bool = True


class MatplotlibRenderer:
    def render(self, result: VoronoiResult, style: PlotStyle | None = None) -> plt.Figure:
        style = style or PlotStyle()

        fig, ax = plt.subplots()
        ax.set_aspect("equal", adjustable="box")

        # --- Cells (filled) ---
        for i, poly in enumerate(result.polygons):
            if poly.shape[0] < 3:
                continue
            ax.fill(
                poly[:, 0],
                poly[:, 1],
                alpha=0.25,          # transparency
                edgecolor="black",
                linewidth=1.2,
            )

        # --- Cell borders (draw again for crispness) ---
        for poly in result.polygons:
            if poly.shape[0] < 3:
                continue
            closed = np.vstack([poly, poly[0]])
            ax.plot(closed[:, 0], closed[:, 1], color="black", linewidth=1.2)

        # --- Points ---
        ax.scatter(result.points[:, 0], result.points[:, 1], s=40, color="red", zorder=5, label="Input points")

        # --- Labels (optional) ---
        if style.show_labels:
            for idx, (x, y) in enumerate(result.points):
                ax.text(x, y, f"P{idx}", fontsize=9, ha="left", va="bottom")

        # --- Bounds / framing ---
        b = result.bounds
        ax.set_xlim(b.min_x, b.max_x)
        ax.set_ylim(b.min_y, b.max_y)

        ax.set_title("Voronoi Diagram")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend(loc="upper right")

        if style.show_grid:
            ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.4)

        if not style.show_axes:
            ax.axis("off")

        return fig

    def export_png(self, fig: plt.Figure, output: Path, dpi: int = 200) -> None:
        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(output, dpi=dpi, bbox_inches="tight")
        except OSError as exc:
            raise OSError(f"Unable to write PNG to '{output}': {exc}") from exc
