"""
Tests for src/voronoi/voronoi_calculator.py
"""

from __future__ import annotations

import pytest
from src.models.errors import CollinearPointsError, InsufficientPointsError
from src.models.point import Point
from src.models.voronoi_result import VoronoiResult
from src.voronoi.voronoi_calculator import VoronoiCalculator


class TestVoronoiCalculatorSuccess:

    def test_Should_ReturnVoronoiResult_Given_ThreeNonCollinearPoints_When_ComputeCalled(
        self, three_points
    ):
        # Arrange
        calculator = VoronoiCalculator()

        # Act
        result = calculator.compute(three_points)

        # Assert
        assert isinstance(result, VoronoiResult)
        assert result.point_count == 3

    def test_Should_ReturnVoronoiResult_Given_FourSquarePoints_When_ComputeCalled(
        self, four_points
    ):
        # Arrange
        calculator = VoronoiCalculator()

        # Act
        result = calculator.compute(four_points)

        # Assert
        assert isinstance(result, VoronoiResult)
        assert result.point_count == 4

    def test_Should_ReturnVoronoiResult_Given_EightPoints_When_ComputeCalled(
        self, eight_points
    ):
        # Arrange
        calculator = VoronoiCalculator()

        # Act
        result = calculator.compute(eight_points)

        # Assert
        assert result.point_count == 8

    def test_Should_PreserveInputPoints_Given_ValidPoints_When_ComputeCalled(
        self, three_points
    ):
        # Arrange
        calculator = VoronoiCalculator()

        # Act
        result = calculator.compute(three_points)

        # Assert
        # Result must contain exactly the same points (as a tuple)
        assert set(result.points) == set(three_points)

    def test_Should_ContainScipyVoronoi_Given_ValidPoints_When_ComputeCalled(
        self, four_points
    ):
        # Arrange
        calculator = VoronoiCalculator()

        # Act
        result = calculator.compute(four_points)

        # Assert
        from scipy.spatial import Voronoi
        assert isinstance(result.scipy_voronoi, Voronoi)

    def test_Should_HaveVertices_Given_FourSquareCorners_When_ComputeCalled(
        self, four_points
    ):
        # Arrange
        calculator = VoronoiCalculator()

        # Act
        result = calculator.compute(four_points)

        # Assert
        # A square has one finite Voronoi vertex at its centre
        assert len(result.scipy_voronoi.vertices) >= 1

    def test_Should_ReturnSameResultTwice_Given_SameInput_When_ComputeCalledTwice(
        self, four_points
    ):
        # Arrange
        calculator = VoronoiCalculator()

        # Act
        result1 = calculator.compute(four_points)
        result2 = calculator.compute(four_points)

        # Assert (calculator is stateless)
        import numpy as np
        np.testing.assert_array_equal(
            result1.scipy_voronoi.points, result2.scipy_voronoi.points
        )


class TestVoronoiCalculatorErrors:

    def test_Should_RaiseInsufficientPointsError_Given_TwoPoints_When_ComputeCalled(self):
        # Arrange
        calculator = VoronoiCalculator()
        points = [Point(0, 0), Point(1, 1)]

        # Act / Assert
        with pytest.raises(InsufficientPointsError) as exc_info:
            calculator.compute(points)
        assert exc_info.value.actual == 2

    def test_Should_RaiseInsufficientPointsError_Given_OnePoint_When_ComputeCalled(self):
        # Arrange
        calculator = VoronoiCalculator()
        points = [Point(5, 5)]

        # Act / Assert
        with pytest.raises(InsufficientPointsError) as exc_info:
            calculator.compute(points)
        assert exc_info.value.actual == 1

    def test_Should_RaiseInsufficientPointsError_Given_NoPoints_When_ComputeCalled(self):
        # Arrange
        calculator = VoronoiCalculator()
        points: list[Point] = []

        # Act / Assert
        with pytest.raises(InsufficientPointsError) as exc_info:
            calculator.compute(points)
        assert exc_info.value.actual == 0

    def test_Should_RaiseCollinearPointsError_Given_ThreeCollinearPoints_When_ComputeCalled(
        self, collinear_points
    ):
        # Arrange
        calculator = VoronoiCalculator()

        # Act / Assert
        with pytest.raises(CollinearPointsError):
            calculator.compute(collinear_points)

    def test_Should_RaiseCollinearPointsError_Given_ManyCollinearPoints_When_ComputeCalled(self):
        # Arrange
        calculator = VoronoiCalculator()
        points = [Point(i, 0) for i in range(10)]  # all on y=0

        # Act / Assert
        with pytest.raises(CollinearPointsError):
            calculator.compute(points)
