"""
Module: geom_utils.py
Responsibility: Pure geometric utility functions (no I/O, no side effects).
SOLID: SRP – isolated mathematical helpers, easily testable in isolation.
"""

from __future__ import annotations

from src.models.point import Point

# Tolerance used to detect near-zero area (collinearity check)
COLLINEARITY_EPSILON = 1e-10


def are_collinear(points: list[Point]) -> bool:
    """
    Return True if all points in the list are collinear (or fewer than 3 points
    are provided, which is trivially collinear / degenerate).

    Uses the signed area of the triangle formed by the first three distinct
    points as a fast early-exit test, then checks remaining points against the
    same line.
    """
    if len(points) < 3:
        return True  # Degenerate: cannot form a 2-D arrangement

    # Pick anchor and two direction points
    p0 = points[0]
    p1 = points[1]
    p2 = points[2]

    ref_area = _triangle_doubled_area(p0, p1, p2)
    if abs(ref_area) > COLLINEARITY_EPSILON:
        return False  # Already non-collinear

    # All points must lie on the line defined by p0→p1
    for p in points[3:]:
        area = _triangle_doubled_area(p0, p1, p)
        if abs(area) > COLLINEARITY_EPSILON:
            return False

    return True


def _triangle_doubled_area(a: Point, b: Point, c: Point) -> float:
    """
    Return 2× the signed area of triangle ABC using the cross-product formula.
    Value is zero iff A, B, C are collinear.
    """
    return (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)
