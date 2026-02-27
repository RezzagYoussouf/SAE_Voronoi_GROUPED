"""
Module: base_exporter.py
Responsibility: Abstract base class defining the exporter contract.
SOLID:
  OCP – new formats (PDF, EPS …) can be added without changing existing code.
  DIP – callers depend on BaseExporter, not on any concrete format.
  ISP – single, minimal method kept as the interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class BaseExporter(ABC):
    """
    Contract for all figure exporters.

    An exporter takes an opaque figure object (produced by a renderer) and
    writes it to disk at the given path.  It is NOT responsible for rendering.
    """

    @abstractmethod
    def export(self, figure: object, output_path: str) -> None:
        """
        Persist *figure* to disk at *output_path*.

        Args:
            figure:      A backend-specific figure object (e.g. plt.Figure).
            output_path: The destination file path (extension may be appended
                         by the concrete implementation if missing).

        Raises:
            ExportError: if writing to disk fails.
        """

    @staticmethod
    def _ensure_parent_dir(output_path: str) -> None:
        """Create parent directory if it does not exist."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
