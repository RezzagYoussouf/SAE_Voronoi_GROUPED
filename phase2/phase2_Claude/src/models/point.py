"""
Module: point.py
Responsibility: Immutable 2D point data model.
SOLID: SRP – this module only defines the Point value object.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """
    Immutable 2D point with float coordinates.
    Using frozen=True enforces immutability and enables hashing (for dedup sets).
    """

    x: float
    y: float

    def __post_init__(self) -> None:
        """Validate that coordinates are finite numbers."""
        import math

        if not isinstance(self.x, (int, float)):
            raise TypeError(f"x must be a number, got {type(self.x).__name__}")
        if not isinstance(self.y, (int, float)):
            raise TypeError(f"y must be a number, got {type(self.y).__name__}")
        if math.isinf(self.x) or math.isnan(self.x):
            raise ValueError(f"x must be a finite number, got {self.x}")
        if math.isinf(self.y) or math.isnan(self.y):
            raise ValueError(f"y must be a finite number, got {self.y}")

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def to_tuple(self) -> tuple[float, float]:
        """Return coordinates as a plain tuple (useful for numpy/scipy)."""
        return (self.x, self.y)
