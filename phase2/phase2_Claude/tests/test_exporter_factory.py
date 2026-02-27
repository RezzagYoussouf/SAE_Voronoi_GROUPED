"""
Tests for src/export/exporter_factory.py
"""

from __future__ import annotations

import pytest
from src.export.exporter_factory import ExporterFactory, FORMAT_SVG, FORMAT_PNG
from src.export.svg_exporter import SVGExporter
from src.export.png_exporter import PNGExporter


class TestExporterFactory:

    def test_Should_ReturnSVGExporter_Given_SvgFormat_When_CreateCalled(self):
        # Arrange / Act
        exporter = ExporterFactory.create(FORMAT_SVG)

        # Assert
        assert isinstance(exporter, SVGExporter)

    def test_Should_ReturnPNGExporter_Given_PngFormat_When_CreateCalled(self):
        # Arrange / Act
        exporter = ExporterFactory.create(FORMAT_PNG)

        # Assert
        assert isinstance(exporter, PNGExporter)

    def test_Should_BeFormatCaseInsensitive_Given_UppercaseName_When_CreateCalled(self):
        # Arrange / Act
        exporter = ExporterFactory.create("SVG")

        # Assert
        assert isinstance(exporter, SVGExporter)

    def test_Should_BeFormatCaseInsensitive_Given_MixedCaseName_When_CreateCalled(self):
        # Arrange / Act
        exporter = ExporterFactory.create("Png")

        # Assert
        assert isinstance(exporter, PNGExporter)

    def test_Should_RaiseValueError_Given_UnsupportedFormat_When_CreateCalled(self):
        # Arrange / Act / Assert
        with pytest.raises(ValueError) as exc_info:
            ExporterFactory.create("bmp")
        assert "bmp" in str(exc_info.value).lower()

    def test_Should_RaiseValueError_Given_EmptyString_When_CreateCalled(self):
        # Arrange / Act / Assert
        with pytest.raises(ValueError):
            ExporterFactory.create("")

    def test_Should_HandleWhitespace_Given_PaddedFormatName_When_CreateCalled(self):
        # Arrange / Act
        exporter = ExporterFactory.create("  svg  ")

        # Assert
        assert isinstance(exporter, SVGExporter)

    def test_Should_ReturnSortedFormats_Given_NoArgs_When_SupportedFormatsCalled(self):
        # Arrange / Act
        formats = ExporterFactory.supported_formats()

        # Assert
        assert FORMAT_PNG in formats
        assert FORMAT_SVG in formats
        assert formats == sorted(formats)
