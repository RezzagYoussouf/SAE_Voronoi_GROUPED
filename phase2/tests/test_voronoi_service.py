from __future__ import annotations

import numpy as np

from voronoi_app.application.voronoi_service import VoronoiService
from voronoi_app.domain.models import Point
from voronoi_app.utils.geometry import Bounds


def test_Should_ComputePolygons_Given_SimplePoints_When_ComputeVoronoi():
    # Arrange
    service = VoronoiService()
    points = [Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10)]
    bounds = Bounds(min_x=-5, min_y=-5, max_x=15, max_y=15)

    # Act
    result = service.compute(points, bounds=bounds, padding=0.0)

    # Assert
    assert result.points.shape == (4, 2)
    assert len(result.polygons) == 4
    assert all(isinstance(p, np.ndarray) for p in result.polygons)
    assert all(poly.shape[1] == 2 for poly in result.polygons)


def test_Should_ComputeBounds_Given_NoBounds_When_ComputeVoronoi():
    # Arrange
    service = VoronoiService()
    points = [Point(1, 1), Point(2, 2), Point(1, 2), Point(2, 1)]
    padding = 3.0

    # Act
    result = service.compute(points, bounds=None, padding=padding)

    # Assert
    assert result.bounds.min_x <= 1 - padding + 1e-9
    assert result.bounds.max_y >= 2 + padding - 1e-9