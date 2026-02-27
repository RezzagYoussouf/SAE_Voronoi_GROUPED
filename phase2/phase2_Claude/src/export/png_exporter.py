"""
Module: png_exporter.py
Responsibility: Export a matplotlib Figure to a PNG raster image.
SOLID: LSP – substitutable for any BaseExporter; SRP – only PNG writing.
"""

from __future__ import annotations

from matplotlib.figure import Figure

from src.export.base_exporter import BaseExporter
from src.models.errors import ExportError

PNG_EXTENSION = ".png"
PNG_FORMAT = "png"
DEFAULT_DPI = 150


class PNGExporter(BaseExporter):
    """
    Exports a matplotlib Figure to a PNG file.

    PNG export is optional but provided as a convenience for contexts where
    a raster image is more useful (e.g. embedding in a report).
    """

    def __init__(self, dpi: int = DEFAULT_DPI) -> None:
        if dpi <= 0:
            raise ValueError(f"DPI must be positive, got {dpi}.")
        self._dpi = dpi

    def export(self, figure: object, output_path: str) -> None:
        """
        Save *figure* as a PNG file.

        Args:
            figure:      A matplotlib Figure instance.
            output_path: Destination path.  The '.png' extension is appended
                         automatically if not already present.

        Raises:
            ExportError: if writing fails or *figure* is not a matplotlib Figure.
        """
        if not isinstance(figure, Figure):
            raise ExportError(
                f"PNGExporter expects a matplotlib Figure, got {type(figure).__name__}."
            )

        path = output_path if output_path.endswith(PNG_EXTENSION) else output_path + PNG_EXTENSION
        self._ensure_parent_dir(path)

        try:
            figure.savefig(path, format=PNG_FORMAT, dpi=self._dpi, bbox_inches="tight")
        except OSError as exc:
            raise ExportError(f"Failed to write PNG to '{path}': {exc}") from exc
