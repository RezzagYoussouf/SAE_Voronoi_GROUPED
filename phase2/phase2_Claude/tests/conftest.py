"""
conftest.py – Shared pytest fixtures for the Voronoi test suite.
"""

from __future__ import annotations

import os
import tempfile
import pytest
import matplotlib
matplotlib.use("Agg")  # Force non-interactive backend before any figure is created

from src.models.point import Point
from src.models.voronoi_result import VoronoiResult
from src.voronoi.voronoi_calculator import VoronoiCalculator


# ── Reusable Point sets ──────────────────────────────────────────────────────

@pytest.fixture
def three_points() -> list[Point]:
    """Minimal valid set: 3 non-collinear points."""
    return [Point(0, 0), Point(4, 0), Point(2, 4)]


@pytest.fixture
def four_points() -> list[Point]:
    """Square corners – classic 4-point Voronoi."""
    return [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]


@pytest.fixture
def eight_points() -> list[Point]:
    """Varied cloud of 8 points."""
    return [
        Point(2, 4),
        Point(5.3, 4.5),
        Point(18, 29),
        Point(12.5, 23.7),
        Point(7, 15),
        Point(3.2, 18.1),
        Point(22, 8),
        Point(10, 10),
    ]


@pytest.fixture
def collinear_points() -> list[Point]:
    """Three collinear points on y = x."""
    return [Point(0, 0), Point(1, 1), Point(2, 2)]


# ── Computed VoronoiResult fixtures ─────────────────────────────────────────

@pytest.fixture
def voronoi_result_three(three_points) -> VoronoiResult:
    return VoronoiCalculator().compute(three_points)


@pytest.fixture
def voronoi_result_four(four_points) -> VoronoiResult:
    return VoronoiCalculator().compute(four_points)


@pytest.fixture
def voronoi_result_eight(eight_points) -> VoronoiResult:
    return VoronoiCalculator().compute(eight_points)


# ── Temporary file helpers ───────────────────────────────────────────────────

@pytest.fixture
def tmp_dir(tmp_path):
    """Provide a temporary directory path as a string."""
    return str(tmp_path)


@pytest.fixture
def point_file_factory(tmp_path):
    """
    Factory fixture: writes content to a temp file and returns its path.

    Usage::

        def test_something(point_file_factory):
            path = point_file_factory("1,2\\n3,4\\n5,6")
    """
    def _factory(content: str, filename: str = "points.txt") -> str:
        filepath = tmp_path / filename
        filepath.write_text(content, encoding="utf-8")
        return str(filepath)

    return _factory
