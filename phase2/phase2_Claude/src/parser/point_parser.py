"""
Module: point_parser.py
Responsibility: Parse a text file into a validated list of Point objects.
SOLID:
  SRP  – only responsible for reading and validating raw text input.
  OCP  – new line formats can be added via subclassing or strategy injection.
  DIP  – depends on the Point abstraction, not on any concrete storage layer.

Design patterns:
  None artificially forced; plain class with small focused methods (KISS).
"""

from __future__ import annotations

import os
from typing import Iterator

from src.models.errors import ParseError
from src.models.point import Point

# ── Constants (no magic numbers) ────────────────────────────────────────────
COORDINATE_SEPARATOR = ","
EXPECTED_COORDINATE_COUNT = 2
COMMENT_PREFIX = "#"


class PointParser:
    """
    Reads a point file and returns a deduplicated, validated list of Points.

    Each non-empty, non-comment line must contain exactly two comma-separated
    float values.  Duplicate points are silently ignored (with a warning
    collected in `self.warnings`).
    """

    def __init__(self) -> None:
        self.warnings: list[str] = []

    # ── Public API ───────────────────────────────────────────────────────────

    def parse_file(self, file_path: str) -> list[Point]:
        """
        Parse a file located at *file_path* and return its points.

        Raises:
            FileNotFoundError: if the file does not exist.
            PermissionError:   if the file cannot be read.
            ParseError:        on any malformed line.
        """
        self._validate_file_exists(file_path)
        raw_lines = self._read_lines(file_path)
        return self._parse_lines(raw_lines)

    def parse_text(self, text: str) -> list[Point]:
        """
        Parse a multi-line string directly (useful for tests and piped input).

        Raises:
            ParseError: on any malformed line.
        """
        lines = text.splitlines()
        return self._parse_lines(enumerate(lines, start=1))

    # ── Private helpers ──────────────────────────────────────────────────────

    def _validate_file_exists(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: '{file_path}'")
        if not os.path.isfile(file_path):
            raise ValueError(f"Path is not a file: '{file_path}'")

    def _read_lines(self, file_path: str) -> Iterator[tuple[int, str]]:
        """Yield (line_number, raw_line) pairs from the file."""
        with open(file_path, encoding="utf-8") as fh:
            for line_number, line in enumerate(fh, start=1):
                yield line_number, line

    def _parse_lines(
        self, numbered_lines: Iterator[tuple[int, str]]
    ) -> list[Point]:
        """Convert numbered raw lines into a deduplicated list of Points."""
        points: list[Point] = []
        seen: set[Point] = set()
        self.warnings = []

        for line_number, raw_line in numbered_lines:
            stripped = raw_line.strip()

            if self._should_skip(stripped):
                continue

            point = self._parse_single_line(stripped, line_number)

            if point in seen:
                self.warnings.append(
                    f"Line {line_number}: duplicate point {point} ignored."
                )
                continue

            seen.add(point)
            points.append(point)

        return points

    def _should_skip(self, line: str) -> bool:
        """Return True for empty lines and comment lines."""
        return not line or line.startswith(COMMENT_PREFIX)

    def _parse_single_line(self, line: str, line_number: int) -> Point:
        """Parse one stripped, non-empty line into a Point or raise ParseError."""
        parts = line.split(COORDINATE_SEPARATOR)

        if len(parts) != EXPECTED_COORDINATE_COUNT:
            raise ParseError(
                f"Expected {EXPECTED_COORDINATE_COUNT} comma-separated values, "
                f"got {len(parts)} in '{line}'.",
                line_number=line_number,
            )

        raw_x, raw_y = parts[0].strip(), parts[1].strip()

        x = self._parse_float(raw_x, "x", line_number, line)
        y = self._parse_float(raw_y, "y", line_number, line)

        return Point(x=x, y=y)

    @staticmethod
    def _parse_float(
        value: str, coordinate_name: str, line_number: int, line: str
    ) -> float:
        """Convert a string to float or raise an informative ParseError."""
        if not value:
            raise ParseError(
                f"Missing value for coordinate '{coordinate_name}' in '{line}'.",
                line_number=line_number,
            )
        try:
            return float(value)
        except ValueError:
            raise ParseError(
                f"Non-numeric value '{value}' for coordinate "
                f"'{coordinate_name}' in '{line}'.",
                line_number=line_number,
            )
