import pytest
from src.calculator import VoronoiCalculator
from src.models import Point

def test_Should_HaveNoFiniteRegions_Given_FourPointsInASquare_When_Computing():
    points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]
    calc = VoronoiCalculator()
    result = calc.compute(points)
    assert len(result.finite_regions) == 0
    assert result.finite_vertices.size == 0
    assert len(result.point_region) == len(points)

def test_Should_HaveAtLeastOneFiniteRegion_Given_FivePointsWithCentralPoint_When_Computing():
    points = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2), Point(1, 1)]
    calc = VoronoiCalculator()
    result = calc.compute(points)
    assert len(result.finite_regions) >= 1
    assert result.finite_vertices.shape[0] > 0
    assert len(result.point_region) == len(points)