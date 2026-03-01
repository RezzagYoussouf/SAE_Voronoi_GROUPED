"""
Module: voronoi_result.py
Responsibility: Data container for Voronoi computation output.
SOLID: SRP – this module only holds computed Voronoi data.
         DIP – higher-level modules depend on this abstraction, not on scipy directly.
"""

from dataclasses import dataclass
from typing import Any

from src.models.point import Point


@dataclass(frozen=True)
class VoronoiResult:
    """
    Wraps the raw scipy Voronoi object alongside the list of parsed input points.
    This indirection (Adapter-like) decouples the rest of the application from
    the scipy API: if the computation backend changes, only VoronoiCalculator
    and this class need updating.
    """

    points: tuple[Point, ...]
    scipy_voronoi: Any  # scipy.spatial.Voronoi – typed as Any to avoid hard coupling

    def __post_init__(self) -> None:
        if not self.points:
            raise ValueError("VoronoiResult requires at least one point.")
        if self.scipy_voronoi is None:
            raise ValueError("VoronoiResult requires a non-None scipy_voronoi object.")

    @property
    def point_count(self) -> int:
        """Number of input points."""
        return len(self.points)
