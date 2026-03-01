"""
Module: voronoi_calculator.py
Responsibility: Compute the Voronoi diagram from a validated list of Points.
SOLID:
  SRP  – only responsible for the computation step.
  OCP  – the public interface is stable; the backend (scipy) is swappable.
  DIP  – depends on Point/VoronoiResult abstractions, not the calling layer.
"""

from __future__ import annotations

import numpy as np
from scipy.spatial import Voronoi

from src.models.errors import CollinearPointsError, InsufficientPointsError
from src.models.point import Point
from src.models.voronoi_result import VoronoiResult
from src.voronoi.geom_utils import are_collinear

# Minimum points required by scipy.spatial.Voronoi in 2-D
MINIMUM_POINTS_FOR_VORONOI = 3


class VoronoiCalculator:
    """
    Computes a Voronoi diagram using scipy as the computational backend.

    This class is intentionally stateless: every call to `compute` is
    independent, which simplifies testing and avoids hidden mutable state
    (Clean Code, KISS).
    """

    def compute(self, points: list[Point]) -> VoronoiResult:
        """
        Compute and return the Voronoi diagram for the given point set.

        Args:
            points: A list of at least 3 non-collinear Point objects.

        Returns:
            A VoronoiResult wrapping the raw scipy Voronoi object.

        Raises:
            InsufficientPointsError: if fewer than 3 points are provided.
            CollinearPointsError:    if all points are collinear.
        """
        self._validate_point_count(points)
        self._validate_non_collinear(points)

        coords = self._to_numpy_array(points)
        scipy_voronoi = Voronoi(coords)

        return VoronoiResult(
            points=tuple(points),
            scipy_voronoi=scipy_voronoi,
        )

    # ── Private helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _validate_point_count(points: list[Point]) -> None:
        if len(points) < MINIMUM_POINTS_FOR_VORONOI:
            raise InsufficientPointsError(len(points))

    @staticmethod
    def _validate_non_collinear(points: list[Point]) -> None:
        if are_collinear(points):
            raise CollinearPointsError()

    @staticmethod
    def _to_numpy_array(points: list[Point]) -> np.ndarray:
        """Convert a list of Points to a (N, 2) numpy array."""
        return np.array([p.to_tuple() for p in points], dtype=float)
