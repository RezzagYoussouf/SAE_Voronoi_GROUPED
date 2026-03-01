from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from voronoi_app.domain.errors import DuplicatePointError, PointFileParseError
from voronoi_app.domain.models import Point


@dataclass(frozen=True, slots=True)
class ParsedPoints:
    points: list[Point]


class PointFileParser:
    """
    Parse a points file where each line is "x,y" (comma-separated), spaces allowed.
    Provides explicit, user-friendly errors.
    """

    def parse_file(self, path: Path) -> ParsedPoints:
        if not path.exists():
            raise PointFileParseError(f"Input file not found: {path}")

        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise PointFileParseError(f"Unable to read file '{path}': {exc}") from exc

        return self.parse_text(text, source_name=str(path))

    def parse_text(self, text: str, source_name: str = "<text>") -> ParsedPoints:
        points: list[Point] = []
        seen: set[tuple[float, float]] = set()

        lines = text.splitlines()
        for i, raw in enumerate(lines, start=1):
            line = raw.strip()
            if line == "":
                raise PointFileParseError(f"{source_name}: line {i} is empty.")

            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 2:
                raise PointFileParseError(
                    f"{source_name}: line {i} has invalid format. Expected 'x,y' (comma-separated). Got: '{raw}'."
                )

            try:
                x = float(parts[0])
                y = float(parts[1])
            except ValueError:
                raise PointFileParseError(
                    f"{source_name}: line {i} has non-numeric values. Got: '{raw}'."
                )

            key = (x, y)
            if key in seen:
                raise DuplicatePointError(f"{source_name}: duplicate point at line {i}: ({x},{y}).")

            seen.add(key)
            points.append(Point(x=x, y=y))

        if len(points) < 4:
            raise PointFileParseError(f"{source_name}: at least 4 points are required to compute a 2D Voronoi diagram with SciPy/Qhull.")

        return ParsedPoints(points=points)