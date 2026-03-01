from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import svgwrite

from voronoi_app.application.voronoi_service import VoronoiResult


@dataclass(frozen=True, slots=True)
class SvgStyle:
    cell_stroke: str = "#333333"
    cell_stroke_width: float = 1.0
    cell_fill: str = "#e8f0ff"
    cell_fill_opacity: float = 0.6
    point_fill: str = "#cc0000"
    point_radius: float = 2.5


class SvgExporter:
    def export(self, result: VoronoiResult, output: Path, style: SvgStyle | None = None) -> None:
        style = style or SvgStyle()

        b = result.bounds
        width = b.max_x - b.min_x
        height = b.max_y - b.min_y

        dwg = svgwrite.Drawing(
            filename=str(output),
            size=(f"{width}", f"{height}"),
            viewBox=f"{b.min_x} {b.min_y} {width} {height}",
        )

        # Background
        dwg.add(dwg.rect(insert=(b.min_x, b.min_y), size=(width, height), fill="white"))

        # Cells (polygons)
        for poly in result.polygons:
            if poly.shape[0] < 3:
                continue
            points = [(float(x), float(y)) for x, y in poly]
            dwg.add(
                dwg.polygon(
                    points=points,
                    fill=style.cell_fill,
                    fill_opacity=style.cell_fill_opacity,
                    stroke=style.cell_stroke,
                    stroke_width=style.cell_stroke_width,
                )
            )

        # Points
        for x, y in result.points:
            dwg.add(dwg.circle(center=(float(x), float(y)), r=style.point_radius, fill=style.point_fill))

        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            dwg.save()
        except OSError as exc:
            raise OSError(f"Unable to write SVG to '{output}': {exc}") from exc

    def export_to_string(self, result: VoronoiResult, style: SvgStyle | None = None) -> str:
        """
        Helper used for tests: produce SVG XML as string without filesystem.
        """
        style = style or SvgStyle()
        b = result.bounds
        width = b.max_x - b.min_x
        height = b.max_y - b.min_y

        dwg = svgwrite.Drawing(
            size=(f"{width}", f"{height}"),
            viewBox=f"{b.min_x} {b.min_y} {width} {height}",
        )

        dwg.add(dwg.rect(insert=(b.min_x, b.min_y), size=(width, height), fill="white"))

        for poly in result.polygons:
            if poly.shape[0] < 3:
                continue
            points = [(float(x), float(y)) for x, y in poly]
            dwg.add(
                dwg.polygon(
                    points=points,
                    fill=style.cell_fill,
                    fill_opacity=style.cell_fill_opacity,
                    stroke=style.cell_stroke,
                    stroke_width=style.cell_stroke_width,
                )
            )

        for x, y in result.points:
            dwg.add(dwg.circle(center=(float(x), float(y)), r=style.point_radius, fill=style.point_fill))

        return dwg.tostring()