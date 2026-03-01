from __future__ import annotations

from pathlib import Path
import numpy as np

from voronoi_app.infrastructure.export_svg import SvgExporter
from voronoi_app.application.voronoi_service import VoronoiResult
from voronoi_app.utils.geometry import Bounds


def test_Should_SkipSmallPolygon_Given_PolygonWithLessThan3Vertices_When_ExportFile(tmp_path: Path):
    # Arrange
    exporter = SvgExporter()
    bounds = Bounds(min_x=0, min_y=0, max_x=10, max_y=10)
    points = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]], dtype=float)
    polygons = [
        np.empty((0, 2)),
        np.array([[1.0, 1.0], [2.0, 2.0]]),
        np.empty((0, 2)),
        np.empty((0, 2)),
    ]
    result = VoronoiResult(points=points, polygons=polygons, bounds=bounds)
    out = tmp_path / "out.svg"

    # Act
    exporter.export(result, out)
    content = out.read_text(encoding="utf-8")

    # Assert
    assert "<svg" in content
    assert "<polygon" not in content
    assert content.count("<circle") == 4
