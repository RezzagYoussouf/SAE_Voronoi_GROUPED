"""
Module: errors.py
Responsibility: Custom exception hierarchy for the application.
SOLID: SRP – all domain exceptions live here, not scattered across modules.
"""


class VoronoiAppError(Exception):
    """Base exception for all application-level errors."""


class ParseError(VoronoiAppError):
    """Raised when a point file cannot be parsed correctly."""

    def __init__(self, message: str, line_number: int | None = None) -> None:
        self.line_number = line_number
        prefix = f"Line {line_number}: " if line_number is not None else ""
        super().__init__(f"{prefix}{message}")


class InsufficientPointsError(VoronoiAppError):
    """Raised when too few points are provided to compute a Voronoi diagram."""

    MINIMUM_POINTS = 3

    def __init__(self, actual: int) -> None:
        self.actual = actual
        super().__init__(
            f"At least {self.MINIMUM_POINTS} non-collinear points are required "
            f"to build a Voronoi diagram; got {actual}."
        )


class CollinearPointsError(VoronoiAppError):
    """Raised when all input points are collinear (degenerate case)."""

    def __init__(self) -> None:
        super().__init__(
            "All input points are collinear. "
            "A non-degenerate Voronoi diagram cannot be computed."
        )


class ExportError(VoronoiAppError):
    """Raised when an export operation fails."""
