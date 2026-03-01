from __future__ import annotations

from pathlib import Path
import pytest

from voronoi_app.application.voronoi_service import VoronoiService
from voronoi_app.domain.models import Point
from voronoi_app.infrastructure.plotter import MatplotlibRenderer
from voronoi_app.utils.geometry import Bounds


def test_Should_RaiseError_Given_WriteFailure_When_ExportPng(tmp_path: Path, monkeypatch):
    # Arrange
    service = VoronoiService()
    renderer = MatplotlibRenderer()
    points = [Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10)]
    bounds = Bounds(min_x=-5, min_y=-5, max_x=15, max_y=15)
    result = service.compute(points, bounds=bounds, padding=0.0)
    fig = renderer.render(result)
    out = tmp_path / "out.png"

    def boom(*args, **kwargs):
        raise OSError("mkdir failed")

    monkeypatch.setattr(Path, "mkdir", boom)

    # Act / Assert
    with pytest.raises(OSError) as exc:
        renderer.export_png(fig, out)
    assert "Unable to write PNG" in str(exc.value)
