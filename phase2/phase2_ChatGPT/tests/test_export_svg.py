from __future__ import annotations

from voronoi_app.application.voronoi_service import VoronoiService
from voronoi_app.domain.models import Point
from voronoi_app.infrastructure.export_svg import SvgExporter
from voronoi_app.utils.geometry import Bounds


def test_Should_ContainSvgElements_Given_Result_When_ExportToString():
    # Arrange
    service = VoronoiService()
    exporter = SvgExporter()
    points = [Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10)]
    bounds = Bounds(min_x=-5, min_y=-5, max_x=15, max_y=15)
    result = service.compute(points, bounds=bounds, padding=0.0)

    # Act
    svg = exporter.export_to_string(result)

    # Assert
    assert "<svg" in svg
    assert "</svg>" in svg
    # At least one polygon path + points circles
    assert "<polygon" in svg
    assert "<circle" in svg


def test_Should_WriteFile_Given_Path_When_Export():
    # Arrange
    service = VoronoiService()
    exporter = SvgExporter()
    points = [Point(0, 0), Point(10, 0), Point(0, 10)]
    bounds = Bounds(min_x=-5, min_y=-5, max_x=15, max_y=15)
    result = service.compute(points, bounds=bounds, padding=0.0)

    # Act
    # Use pytest tmp_path fixture by importing indirectly via function arg style
    # (kept as plain function to maintain naming constraints)
    # Assert handled by reading file afterwards
    from pathlib import Path
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "out.svg"
        exporter.export(result, out)
        content = out.read_text(encoding="utf-8")

    # Assert
    assert "<svg" in content