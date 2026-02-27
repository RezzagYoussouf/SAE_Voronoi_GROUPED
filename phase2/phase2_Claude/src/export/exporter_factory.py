"""
Module: exporter_factory.py
Responsibility: Instantiate the correct exporter given a format string.
SOLID:
  OCP  – new formats require only one dict entry, not a chain of if/elif.
  SRP  – factory logic is isolated here.
  DIP  – returns BaseExporter; callers never import concrete classes directly.
Design pattern: Factory Method / Simple Factory.
  Justified because callers (CLI, tests) need to request a format by name
  without coupling to the concrete exporter classes.
"""

from __future__ import annotations

from src.export.base_exporter import BaseExporter
from src.export.svg_exporter import SVGExporter
from src.export.png_exporter import PNGExporter

# ── Supported formats ────────────────────────────────────────────────────────
FORMAT_SVG = "svg"
FORMAT_PNG = "png"

_EXPORTER_REGISTRY: dict[str, type[BaseExporter]] = {
    FORMAT_SVG: SVGExporter,
    FORMAT_PNG: PNGExporter,
}


class ExporterFactory:
    """
    Creates and returns a BaseExporter for the requested *format*.

    Usage::

        exporter = ExporterFactory.create("svg")
        exporter.export(figure, "output/diagram")
    """

    @staticmethod
    def create(format_name: str) -> BaseExporter:
        """
        Return an exporter for *format_name* (case-insensitive).

        Args:
            format_name: One of 'svg', 'png'.

        Raises:
            ValueError: if *format_name* is not supported.
        """
        normalised = format_name.strip().lower()
        exporter_class = _EXPORTER_REGISTRY.get(normalised)

        if exporter_class is None:
            supported = ", ".join(sorted(_EXPORTER_REGISTRY))
            raise ValueError(
                f"Unsupported export format '{format_name}'. "
                f"Supported formats: {supported}."
            )

        return exporter_class()

    @staticmethod
    def supported_formats() -> list[str]:
        """Return a sorted list of all supported format names."""
        return sorted(_EXPORTER_REGISTRY)
