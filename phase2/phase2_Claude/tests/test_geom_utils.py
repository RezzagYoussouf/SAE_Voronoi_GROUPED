"""
Tests for src/voronoi/geom_utils.py
"""

from __future__ import annotations

import pytest
from src.models.point import Point
from src.voronoi.geom_utils import are_collinear, _triangle_doubled_area


class TestAreCollinear:

    def test_Should_ReturnTrue_Given_ThreeCollinearPoints_When_AreCollinearCalled(self):
        # Arrange
        points = [Point(0, 0), Point(1, 1), Point(2, 2)]

        # Act
        result = are_collinear(points)

        # Assert
        assert result is True

    def test_Should_ReturnFalse_Given_ThreeNonCollinearPoints_When_AreCollinearCalled(self):
        # Arrange
        points = [Point(0, 0), Point(4, 0), Point(2, 4)]

        # Act
        result = are_collinear(points)

        # Assert
        assert result is False

    def test_Should_ReturnTrue_Given_TwoPoints_When_AreCollinearCalled(self):
        # Arrange
        points = [Point(0, 0), Point(1, 1)]

        # Act
        result = are_collinear(points)

        # Assert
        assert result is True  # degenerate

    def test_Should_ReturnTrue_Given_OnePoint_When_AreCollinearCalled(self):
        # Arrange
        points = [Point(5, 5)]

        # Act
        result = are_collinear(points)

        # Assert
        assert result is True

    def test_Should_ReturnTrue_Given_EmptyList_When_AreCollinearCalled(self):
        # Arrange
        points: list[Point] = []

        # Act
        result = are_collinear(points)

        # Assert
        assert result is True

    def test_Should_ReturnFalse_Given_FourPointsWithOneOffLine_When_AreCollinearCalled(self):
        # Arrange – 3 collinear + 1 off-line
        points = [Point(0, 0), Point(1, 0), Point(2, 0), Point(1, 1)]

        # Act
        result = are_collinear(points)

        # Assert
        assert result is False

    def test_Should_ReturnTrue_Given_ManyCollinearPoints_When_AreCollinearCalled(self):
        # Arrange
        points = [Point(i, i * 2) for i in range(10)]  # y = 2x line

        # Act
        result = are_collinear(points)

        # Assert
        assert result is True


class TestTriangleDoubledArea:

    def test_Should_ReturnZero_Given_CollinearPoints_When_TriangleAreaComputed(self):
        # Arrange
        a, b, c = Point(0, 0), Point(1, 0), Point(2, 0)

        # Act
        area = _triangle_doubled_area(a, b, c)

        # Assert
        assert area == pytest.approx(0.0)

    def test_Should_ReturnNonZero_Given_NonCollinearPoints_When_TriangleAreaComputed(self):
        # Arrange
        a, b, c = Point(0, 0), Point(1, 0), Point(0, 1)

        # Act
        area = _triangle_doubled_area(a, b, c)

        # Assert
        assert area != pytest.approx(0.0)

    def test_Should_ReturnTwo_Given_UnitRightTriangle_When_TriangleAreaComputed(self):
        # Arrange – right-angled triangle with legs 1 and 2; 2*area = base*height = 2
        a, b, c = Point(0, 0), Point(2, 0), Point(0, 1)

        # Act
        area = _triangle_doubled_area(a, b, c)

        # Assert
        assert area == pytest.approx(2.0)
