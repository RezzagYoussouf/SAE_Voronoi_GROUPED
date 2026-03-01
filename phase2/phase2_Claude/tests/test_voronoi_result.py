"""
Tests for src/models/voronoi_result.py
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock

from src.models.point import Point
from src.models.voronoi_result import VoronoiResult


class TestVoronoiResult:

    def test_Should_StorePoints_Given_ValidPoints_When_Created(self):
        # Arrange
        points = (Point(0, 0), Point(1, 0), Point(0, 1))
        mock_voronoi = MagicMock()

        # Act
        result = VoronoiResult(points=points, scipy_voronoi=mock_voronoi)

        # Assert
        assert result.points == points

    def test_Should_StoreScipyVoronoi_Given_ValidObject_When_Created(self):
        # Arrange
        points = (Point(0, 0), Point(1, 0), Point(0, 1))
        mock_voronoi = MagicMock()

        # Act
        result = VoronoiResult(points=points, scipy_voronoi=mock_voronoi)

        # Assert
        assert result.scipy_voronoi is mock_voronoi

    def test_Should_ReturnCorrectCount_Given_ThreePoints_When_PointCountAccessed(self):
        # Arrange
        points = (Point(0, 0), Point(1, 0), Point(0, 1))
        mock_voronoi = MagicMock()

        # Act
        result = VoronoiResult(points=points, scipy_voronoi=mock_voronoi)

        # Assert
        assert result.point_count == 3

    def test_Should_RaiseValueError_Given_EmptyPoints_When_Created(self):
        # Arrange
        mock_voronoi = MagicMock()

        # Act / Assert
        with pytest.raises(ValueError):
            VoronoiResult(points=(), scipy_voronoi=mock_voronoi)

    def test_Should_RaiseValueError_Given_NoneScipyVoronoi_When_Created(self):
        # Arrange
        points = (Point(0, 0), Point(1, 0), Point(0, 1))

        # Act / Assert
        with pytest.raises(ValueError):
            VoronoiResult(points=points, scipy_voronoi=None)

    def test_Should_BeImmutable_Given_FrozenResult_When_AttributeAssignmentAttempted(self):
        # Arrange
        points = (Point(0, 0), Point(1, 0), Point(0, 1))
        mock_voronoi = MagicMock()
        result = VoronoiResult(points=points, scipy_voronoi=mock_voronoi)

        # Act / Assert
        with pytest.raises(Exception):
            result.points = ()  # type: ignore
