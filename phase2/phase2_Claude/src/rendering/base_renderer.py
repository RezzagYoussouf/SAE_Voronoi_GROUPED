"""
Module: base_renderer.py
Responsibility: Abstract base class defining the renderer contract.
SOLID:
  OCP – new renderers (e.g. HTML canvas, PyQt) are added without changing callers.
  DIP – callers depend on BaseRenderer, not on Matplotlib specifically.
  ISP – the interface is kept minimal (one method: render).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models.voronoi_result import VoronoiResult


class BaseRenderer(ABC):
    """
    Contract for all Voronoi renderers.

    A renderer is responsible for turning a VoronoiResult into a visual
    representation (e.g. a matplotlib Figure).  It does NOT handle file I/O –
    that is the responsibility of the exporter layer.
    """

    @abstractmethod
    def render(self, result: VoronoiResult) -> object:
        """
        Render the Voronoi diagram described by *result*.

        Returns:
            A backend-specific figure object (e.g. matplotlib.figure.Figure).
            Callers should treat this as opaque unless they know the concrete type.
        """
