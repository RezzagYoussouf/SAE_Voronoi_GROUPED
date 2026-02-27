"""
Tests for src/export/png_exporter.py
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from src.export.png_exporter import PNGExporter, PNG_EXTENSION, DEFAULT_DPI
from src.models.errors import ExportError


def _make_simple_figure() -> plt.Figure:
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    return fig


class TestPNGExporterSuccess:

    def test_Should_CreatePngFile_Given_ValidFigureAndPath_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = PNGExporter()
        fig = _make_simple_figure()
        output_stem = os.path.join(tmp_dir, "diagram")

        # Act
        exporter.export(fig, output_stem)
        plt.close(fig)

        # Assert
        assert os.path.exists(output_stem + PNG_EXTENSION)

    def test_Should_AppendPngExtension_Given_PathWithoutExtension_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = PNGExporter()
        fig = _make_simple_figure()
        output_stem = os.path.join(tmp_dir, "no_ext")

        # Act
        exporter.export(fig, output_stem)
        plt.close(fig)

        # Assert
        assert os.path.exists(output_stem + ".png")

    def test_Should_NotDoubleAppendExtension_Given_PathWithPngExtension_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = PNGExporter()
        fig = _make_simple_figure()
        output_path = os.path.join(tmp_dir, "diagram.png")

        # Act
        exporter.export(fig, output_path)
        plt.close(fig)

        # Assert
        assert os.path.exists(output_path)
        assert not os.path.exists(output_path + ".png")

    def test_Should_CreateNonEmptyFile_Given_ValidFigure_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = PNGExporter()
        fig = _make_simple_figure()
        output_stem = os.path.join(tmp_dir, "nonempty")

        # Act
        exporter.export(fig, output_stem)
        plt.close(fig)

        # Assert
        file_size = os.path.getsize(output_stem + ".png")
        assert file_size > 0

    def test_Should_UseDefaultDpi_Given_NoExplicitDpi_When_ExporterCreated(self):
        # Arrange / Act
        exporter = PNGExporter()

        # Assert
        assert exporter._dpi == DEFAULT_DPI

    def test_Should_AcceptCustomDpi_Given_ValidDpi_When_ExporterCreated(self):
        # Arrange / Act
        exporter = PNGExporter(dpi=300)

        # Assert
        assert exporter._dpi == 300

    def test_Should_CreateParentDirectory_Given_NestedPath_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = PNGExporter()
        fig = _make_simple_figure()
        output_stem = os.path.join(tmp_dir, "a", "b", "diagram")

        # Act
        exporter.export(fig, output_stem)
        plt.close(fig)

        # Assert
        assert os.path.exists(output_stem + ".png")


class TestPNGExporterErrors:

    def test_Should_RaiseValueError_Given_ZeroDpi_When_ExporterCreated(self):
        # Arrange / Act / Assert
        with pytest.raises(ValueError):
            PNGExporter(dpi=0)

    def test_Should_RaiseValueError_Given_NegativeDpi_When_ExporterCreated(self):
        # Arrange / Act / Assert
        with pytest.raises(ValueError):
            PNGExporter(dpi=-100)

    def test_Should_RaiseExportError_Given_NonFigureObject_When_ExportCalled(
        self, tmp_dir
    ):
        # Arrange
        exporter = PNGExporter()
        output_stem = os.path.join(tmp_dir, "bad")

        # Act / Assert
        with pytest.raises(ExportError):
            exporter.export(42, output_stem)  # type: ignore
