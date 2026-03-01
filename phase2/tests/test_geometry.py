from __future__ import annotations

import numpy as np
import pytest

from voronoi_app.utils.geometry import Bounds, compute_bounds, parse_bounds, _sort_polygon_vertices


def test_Should_ComputeBounds_Given_Points_When_ComputeBounds():
    # Arrange
    pts = np.array([[1.0, 2.0], [3.0, 5.0]], dtype=float)
    padding = 2.0

    # Act
    b = compute_bounds(pts, padding=padding)

    # Assert
    assert b.min_x == 1.0 - 2.0
    assert b.max_x == 3.0 + 2.0
    assert b.min_y == 2.0 - 2.0
    assert b.max_y == 5.0 + 2.0


def test_Should_ExpandBounds_Given_ZeroWidthOrHeight_When_ComputeBounds():
    # Arrange
    pts = np.array([[1.0, 1.0], [1.0, 1.0]], dtype=float)

    # Act
    b = compute_bounds(pts, padding=0.0)

    # Assert
    assert b.max_x > b.min_x
    assert b.max_y > b.min_y


def test_Should_RaiseError_Given_EmptyPoints_When_ComputeBounds():
    # Arrange
    pts = np.array([], dtype=float).reshape(0, 2)

    # Act / Assert
    with pytest.raises(ValueError):
        compute_bounds(pts, padding=1.0)


def test_Should_ParseBounds_Given_ValidText_When_ParseBounds():
    # Arrange
    text = "-1, -2, 3, 4"

    # Act
    b = parse_bounds(text)

    # Assert
    assert b == Bounds(min_x=-1.0, min_y=-2.0, max_x=3.0, max_y=4.0)


def test_Should_RaiseError_Given_WrongCount_When_ParseBounds():
    # Arrange
    text = "0,0,1"

    # Act / Assert
    with pytest.raises(ValueError):
        parse_bounds(text)


def test_Should_RaiseError_Given_NonNumeric_When_ParseBounds():
    # Arrange
    text = "a,0,1,2"

    # Act / Assert
    with pytest.raises(ValueError):
        parse_bounds(text)


def test_Should_RaiseError_Given_InvalidOrder_When_ParseBounds():
    # Arrange
    text = "0,0,0,1"

    # Act / Assert
    with pytest.raises(ValueError):
        parse_bounds(text)


def test_Should_SortVertices_Given_UnsortedPolygon_When_SortPolygonVertices():
    # Arrange
    poly = np.array([[1.0, 0.0], [0.0, 0.0], [0.0, 1.0]], dtype=float)

    # Act
    sorted_poly = _sort_polygon_vertices(poly)

    # Assert
    assert sorted_poly.shape == (3, 2)
    # mêmes points, ordre différent
    assert set(map(tuple, sorted_poly)) == set(map(tuple, poly))


def test_Should_ReturnSame_Given_LessThanThreeVertices_When_SortPolygonVertices():
    # Arrange
    poly = np.array([[0.0, 0.0], [1.0, 1.0]], dtype=float)

    # Act
    sorted_poly = _sort_polygon_vertices(poly)

    # Assert
    assert np.array_equal(sorted_poly, poly)
