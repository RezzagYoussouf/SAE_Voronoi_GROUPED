"""
Tests for src/rendering/matplotlib_renderer.py
Uses the Agg non-interactive backend (set in conftest.py).
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

import pytest
from matplotlib.figure import Figure

from src.rendering.matplotlib_renderer import MatplotlibRenderer
from src.rendering.base_renderer import BaseRenderer


class TestMatplotlibRendererContract:

    def test_Should_BeSubclassOfBaseRenderer_Given_MatplotlibRenderer_When_Checked(self):
        # Arrange / Act / Assert
        assert issubclass(MatplotlibRenderer, BaseRenderer)

    def test_Should_ReturnFigure_Given_ThreePointResult_When_RenderCalled(
        self, voronoi_result_three
    ):
        # Arrange
        renderer = MatplotlibRenderer()

        # Act
        fig = renderer.render(voronoi_result_three)

        # Assert
        assert isinstance(fig, Figure)

        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_Should_ReturnFigure_Given_EightPointResult_When_RenderCalled(
        self, voronoi_result_eight
    ):
        # Arrange
        renderer = MatplotlibRenderer()

        # Act
        fig = renderer.render(voronoi_result_eight)

        # Assert
        assert isinstance(fig, Figure)

        import matplotlib.pyplot as plt
        plt.close(fig)


class TestMatplotlibRendererStyling:

    def test_Should_ReturnFigureWithAxes_Given_ShowAxesTrue_When_RenderCalled(
        self, voronoi_result_four
    ):
        # Arrange
        renderer = MatplotlibRenderer(show_axes=True)

        # Act
        fig = renderer.render(voronoi_result_four)

        # Assert
        ax = fig.axes[0]
        assert ax.get_xlabel() == "x"
        assert ax.get_ylabel() == "y"

        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_Should_ReturnFigureWithoutAxes_Given_ShowAxesFalse_When_RenderCalled(
        self, voronoi_result_four
    ):
        # Arrange
        renderer = MatplotlibRenderer(show_axes=False)

        # Act
        fig = renderer.render(voronoi_result_four)

        # Assert
        ax = fig.axes[0]
        assert not ax.axison  # axes are off

        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_Should_SetTitle_Given_AnyResult_When_RenderCalled(
        self, voronoi_result_three
    ):
        # Arrange
        renderer = MatplotlibRenderer()

        # Act
        fig = renderer.render(voronoi_result_three)

        # Assert
        ax = fig.axes[0]
        assert "Voronoi" in ax.get_title()

        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_Should_HaveExpectedFigureSize_Given_DefaultRenderer_When_RenderCalled(
        self, voronoi_result_four
    ):
        # Arrange
        from src.rendering.matplotlib_renderer import FIGURE_SIZE_INCHES
        renderer = MatplotlibRenderer()

        # Act
        fig = renderer.render(voronoi_result_four)

        # Assert
        width, height = fig.get_size_inches()
        assert (width, height) == FIGURE_SIZE_INCHES

        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_Should_ContainInputPointsInPlot_Given_FourPoints_When_RenderCalled(
        self, voronoi_result_four
    ):
        # Arrange
        renderer = MatplotlibRenderer()

        # Act
        fig = renderer.render(voronoi_result_four)
        ax = fig.axes[0]

        # Assert – at least one scatter/line collection with colored markers is present
        has_lines = len(ax.lines) > 0
        has_collections = len(ax.collections) > 0
        assert has_lines or has_collections

        import matplotlib.pyplot as plt
        plt.close(fig)
