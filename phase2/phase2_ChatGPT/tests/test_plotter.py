from __future__ import annotations

from pathlib import Path

from voronoi_app.application.voronoi_service import VoronoiService
from voronoi_app.domain.models import Point
from voronoi_app.infrastructure.plotter import MatplotlibRenderer, PlotStyle
from voronoi_app.utils.geometry import Bounds


def test_Should_RenderFigure_Given_Result_When_Render():
    # Arrange
    service = VoronoiService()
    renderer = MatplotlibRenderer()
    points = [Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10)]
    bounds = Bounds(min_x=-5, min_y=-5, max_x=15, max_y=15)
    result = service.compute(points, bounds=bounds, padding=0.0)

    # Act
    fig = renderer.render(result, style=PlotStyle(show_axes=True))

    # Assert
    assert fig is not None
    assert len(fig.axes) == 1


def test_Should_HideAxes_Given_NoAxesStyle_When_Render():
    # Arrange
    service = VoronoiService()
    renderer = MatplotlibRenderer()
    points = [Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10)]
    bounds = Bounds(min_x=-5, min_y=-5, max_x=15, max_y=15)
    result = service.compute(points, bounds=bounds, padding=0.0)

    # Act
    fig = renderer.render(result, style=PlotStyle(show_axes=False))

    # Assert
    ax = fig.axes[0]
    assert ax.axison is False


def test_Should_WritePng_Given_OutputPath_When_ExportPng(tmp_path: Path):
    # Arrange
    service = VoronoiService()
    renderer = MatplotlibRenderer()
    points = [Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10)]
    bounds = Bounds(min_x=-5, min_y=-5, max_x=15, max_y=15)
    result = service.compute(points, bounds=bounds, padding=0.0)
    fig = renderer.render(result)
    out = tmp_path / "out.png"

    # Act
    renderer.export_png(fig, out, dpi=80)

    # Assert
    assert out.exists()
    assert out.stat().st_size > 0
