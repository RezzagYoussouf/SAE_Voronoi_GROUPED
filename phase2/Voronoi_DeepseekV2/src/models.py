from dataclasses import dataclass
from typing import List, Optional
import numpy as np


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


@dataclass
class VoronoiResult:
    points: List[Point]
    vertices: np.ndarray          # tous les sommets
    regions: List[List[int]]      # régions (indices de vertices, -1 pour infini)
    point_region: List[int]        # association point -> région

    # Champs calculés après coup
    finite_regions: List[List[int]] = None
    finite_vertices: np.ndarray = None


class VoronoiError(Exception):
    """Erreur de base pour l'application."""
    pass


class ParsingError(VoronoiError):
    pass


class DuplicatePointError(ParsingError):
    pass


class InvalidPointError(ParsingError):
    pass