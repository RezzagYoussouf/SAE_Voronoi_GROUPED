from __future__ import annotations


class PointFileParseError(ValueError):
    """Raised when the points file cannot be parsed safely."""
    pass


class DuplicatePointError(PointFileParseError):
    """Raised when duplicate points exist."""
    pass