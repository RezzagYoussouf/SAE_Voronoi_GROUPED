from __future__ import annotations

import numpy as np

from voronoi_app.infrastructure.export_svg import SvgExporter
from voronoi_app.application.voronoi_service import VoronoiResult
from voronoi_app.utils.geometry import Bounds


def test_Should_SkipSmallPolygon_Given_PolygonWithLessThan3Vertices_When_ExportToString():
    # Arrange
    exporter = SvgExporter()
    bounds = Bounds(min_x=0, min_y=0, max_x=10, max_y=10)
    points = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]], dtype=float)
    polygons = [np.empty((0, 2)), np.array([[1.0, 1.0], [2.0, 2.0]]), np.empty((0, 2)), np.empty((0, 2))]
    result = VoronoiResult(points=points, polygons=polygons, bounds=bounds)

    # Act
    svg = exporter.export_to_string(result)

    # Assert
    assert "<svg" in svg
    # aucun polygon attendu car tous < 3 sommets
    assert "<polygon" not in svg
    # mais les points doivent être là
    assert svg.count("<circle") == 4
