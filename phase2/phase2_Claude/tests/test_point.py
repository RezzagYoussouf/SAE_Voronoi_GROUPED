"""
Tests for src/models/point.py
TDD: these tests were written BEFORE the Point class to drive its design.
"""

from __future__ import annotations

import math
import pytest
from src.models.point import Point


class TestPointCreation:
    """Tests for valid Point creation."""

    def test_Should_CreatePoint_Given_IntegerCoordinates_When_Instantiated(self):
        # Arrange
        x, y = 3, 7

        # Act
        point = Point(x=x, y=y)

        # Assert
        assert point.x == 3
        assert point.y == 7

    def test_Should_CreatePoint_Given_FloatCoordinates_When_Instantiated(self):
        # Arrange
        x, y = 3.14, -2.71

        # Act
        point = Point(x=x, y=y)

        # Assert
        assert point.x == pytest.approx(3.14)
        assert point.y == pytest.approx(-2.71)

    def test_Should_CreatePoint_Given_ZeroCoordinates_When_Instantiated(self):
        # Arrange / Act
        point = Point(x=0, y=0)

        # Assert
        assert point.x == 0
        assert point.y == 0

    def test_Should_CreatePoint_Given_NegativeCoordinates_When_Instantiated(self):
        # Arrange / Act
        point = Point(x=-5.5, y=-10.0)

        # Assert
        assert point.x == pytest.approx(-5.5)
        assert point.y == pytest.approx(-10.0)

    def test_Should_ReturnCorrectTuple_Given_ValidPoint_When_ToTupleCalled(self):
        # Arrange
        point = Point(x=1.0, y=2.0)

        # Act
        result = point.to_tuple()

        # Assert
        assert result == (1.0, 2.0)

    def test_Should_BeHashable_Given_FrozenPoint_When_UsedInSet(self):
        # Arrange
        p1 = Point(x=1, y=2)
        p2 = Point(x=1, y=2)
        p3 = Point(x=3, y=4)

        # Act
        point_set = {p1, p2, p3}

        # Assert
        assert len(point_set) == 2  # p1 and p2 are duplicates

    def test_Should_BeEqual_Given_SameCoordinates_When_ComparedWithEquals(self):
        # Arrange
        p1 = Point(x=5.0, y=6.0)
        p2 = Point(x=5.0, y=6.0)

        # Act / Assert
        assert p1 == p2

    def test_Should_NotBeEqual_Given_DifferentCoordinates_When_ComparedWithEquals(self):
        # Arrange
        p1 = Point(x=5.0, y=6.0)
        p2 = Point(x=5.0, y=7.0)

        # Act / Assert
        assert p1 != p2

    def test_Should_BeImmutable_Given_FrozenPoint_When_AttributeAssignmentAttempted(self):
        # Arrange
        point = Point(x=1, y=2)

        # Act / Assert
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            point.x = 99  # type: ignore

    def test_Should_ContainCoordinatesInRepr_Given_ValidPoint_When_ReprCalled(self):
        # Arrange
        point = Point(x=4.0, y=9.0)

        # Act
        representation = repr(point)

        # Assert
        assert "4.0" in representation
        assert "9.0" in representation


class TestPointValidation:
    """Tests for Point input validation."""

    def test_Should_RaiseValueError_Given_InfiniteX_When_Instantiated(self):
        # Arrange / Act / Assert
        with pytest.raises(ValueError):
            Point(x=math.inf, y=0)

    def test_Should_RaiseValueError_Given_NaNX_When_Instantiated(self):
        # Arrange / Act / Assert
        with pytest.raises(ValueError):
            Point(x=math.nan, y=0)

    def test_Should_RaiseValueError_Given_InfiniteY_When_Instantiated(self):
        # Arrange / Act / Assert
        with pytest.raises(ValueError):
            Point(x=0, y=math.inf)

    def test_Should_RaiseValueError_Given_NaNY_When_Instantiated(self):
        # Arrange / Act / Assert
        with pytest.raises(ValueError):
            Point(x=0, y=math.nan)
