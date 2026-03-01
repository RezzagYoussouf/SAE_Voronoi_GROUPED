from __future__ import annotations

from pathlib import Path
import pytest

from voronoi_app.application.voronoi_service import VoronoiService
from voronoi_app.domain.models import Point
from voronoi_app.infrastructure.export_svg import SvgExporter
from voronoi_app.utils.geometry import Bounds


def test_Should_RaiseError_Given_WriteFailure_When_ExportSvg(tmp_path: Path, monkeypatch):
    # Arrange
    service = VoronoiService()
    exporter = SvgExporter()
    points = [Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10)]
    bounds = Bounds(min_x=-5, min_y=-5, max_x=15, max_y=15)
    result = service.compute(points, bounds=bounds, padding=0.0)
    out = tmp_path / "out.svg"

    def boom(*args, **kwargs):
        raise OSError("write failed")

    # force l'erreur sur mkdir (ou save), peu importe, on couvre la branche d'exception
    monkeypatch.setattr(Path, "mkdir", boom)

    # Act / Assert
    with pytest.raises(OSError) as exc:
        exporter.export(result, out)
    assert "Unable to write SVG" in str(exc.value)
