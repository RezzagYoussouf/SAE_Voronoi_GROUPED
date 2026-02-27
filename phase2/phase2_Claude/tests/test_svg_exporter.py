"""
Tests for src/export/svg_exporter.py
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from src.export.svg_exporter import SVGExporter, SVG_EXTENSION
from src.models.errors import ExportError


def _make_simple_figure() -> plt.Figure:
    """Create a minimal matplotlib figure for testing."""
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    return fig


class TestSVGExporterSuccess:

    def test_Should_CreateSvgFile_Given_ValidFigureAndPath_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = SVGExporter()
        fig = _make_simple_figure()
        output_stem = os.path.join(tmp_dir, "diagram")

        # Act
        exporter.export(fig, output_stem)
        plt.close(fig)

        # Assert
        assert os.path.exists(output_stem + SVG_EXTENSION)

    def test_Should_AppendSvgExtension_Given_PathWithoutExtension_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = SVGExporter()
        fig = _make_simple_figure()
        output_stem = os.path.join(tmp_dir, "no_ext")

        # Act
        exporter.export(fig, output_stem)
        plt.close(fig)

        # Assert
        assert os.path.exists(output_stem + ".svg")

    def test_Should_NotDoubleAppendExtension_Given_PathWithSvgExtension_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = SVGExporter()
        fig = _make_simple_figure()
        output_path = os.path.join(tmp_dir, "diagram.svg")

        # Act
        exporter.export(fig, output_path)
        plt.close(fig)

        # Assert – file exists, no double .svg.svg
        assert os.path.exists(output_path)
        double = output_path + ".svg"
        assert not os.path.exists(double)

    def test_Should_ProduceValidSvgContent_Given_ValidFigure_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = SVGExporter()
        fig = _make_simple_figure()
        output_stem = os.path.join(tmp_dir, "check_content")

        # Act
        exporter.export(fig, output_stem)
        plt.close(fig)

        # Assert – file starts with SVG XML declaration or <svg tag
        with open(output_stem + ".svg", encoding="utf-8") as fh:
            content = fh.read()
        assert "<svg" in content.lower()

    def test_Should_CreateParentDirectory_Given_NestedPath_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = SVGExporter()
        fig = _make_simple_figure()
        output_stem = os.path.join(tmp_dir, "nested", "deep", "diagram")

        # Act
        exporter.export(fig, output_stem)
        plt.close(fig)

        # Assert
        assert os.path.exists(output_stem + ".svg")


class TestSVGExporterErrors:

    def test_Should_RaiseExportError_Given_NonFigureObject_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = SVGExporter()
        output_stem = os.path.join(tmp_dir, "bad")

        # Act / Assert
        with pytest.raises(ExportError):
            exporter.export("not a figure", output_stem)  # type: ignore
