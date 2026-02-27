"""
Module: svg_exporter.py
Responsibility: Export a matplotlib Figure to an SVG file.
SOLID: LSP – can replace any BaseExporter; SRP – only SVG writing.
"""

from __future__ import annotations

from matplotlib.figure import Figure

from src.export.base_exporter import BaseExporter
from src.models.errors import ExportError

SVG_EXTENSION = ".svg"
SVG_FORMAT = "svg"


class SVGExporter(BaseExporter):
    """
    Exports a matplotlib Figure to vector SVG format.

    SVG is the mandatory export format: it is resolution-independent and can
    be opened in any modern browser or vector editor without extra tools.
    """

    def export(self, figure: object, output_path: str) -> None:
        """
        Save *figure* as an SVG file.

        Args:
            figure:      A matplotlib Figure instance.
            output_path: Destination path.  The '.svg' extension is appended
                         automatically if not already present.

        Raises:
            ExportError: if writing fails or *figure* is not a matplotlib Figure.
        """
        if not isinstance(figure, Figure):
            raise ExportError(
                f"SVGExporter expects a matplotlib Figure, got {type(figure).__name__}."
            )

        path = output_path if output_path.endswith(SVG_EXTENSION) else output_path + SVG_EXTENSION
        self._ensure_parent_dir(path)

        try:
            figure.savefig(path, format=SVG_FORMAT, bbox_inches="tight")
        except OSError as exc:
            raise ExportError(f"Failed to write SVG to '{path}': {exc}") from exc
