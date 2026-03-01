"""
Integration tests: full pipeline from file → Voronoi → export.
These tests exercise multiple modules together to validate end-to-end correctness.
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")

import pytest

from src.parser.point_parser import PointParser
from src.voronoi.voronoi_calculator import VoronoiCalculator
from src.rendering.matplotlib_renderer import MatplotlibRenderer
from src.export.exporter_factory import ExporterFactory
import matplotlib.pyplot as plt


class TestFullPipeline:

    def test_Should_ProduceSvgFile_Given_ValidPointFile_When_FullPipelineExecuted(
        self, point_file_factory, tmp_dir
    ):
        # Arrange
        content = "0,0\n4,0\n4,4\n0,4\n2,2"
        path = point_file_factory(content)
        output_stem = os.path.join(tmp_dir, "integration_svg")

        # Act
        parser = PointParser()
        points = parser.parse_file(path)
        calculator = VoronoiCalculator()
        result = calculator.compute(points)
        renderer = MatplotlibRenderer()
        figure = renderer.render(result)
        exporter = ExporterFactory.create("svg")
        exporter.export(figure, output_stem)
        plt.close(figure)

        # Assert
        assert os.path.exists(output_stem + ".svg")
        with open(output_stem + ".svg", encoding="utf-8") as fh:
            content_svg = fh.read()
        assert "<svg" in content_svg.lower()

    def test_Should_ProducePngFile_Given_ValidPointFile_When_FullPipelineExecuted(
        self, point_file_factory, tmp_dir
    ):
        # Arrange
        content = "1,1\n5,1\n5,5\n1,5\n3,3"
        path = point_file_factory(content)
        output_stem = os.path.join(tmp_dir, "integration_png")

        # Act
        parser = PointParser()
        points = parser.parse_file(path)
        result = VoronoiCalculator().compute(points)
        figure = MatplotlibRenderer().render(result)
        ExporterFactory.create("png").export(figure, output_stem)
        plt.close(figure)

        # Assert
        assert os.path.exists(output_stem + ".png")
        assert os.path.getsize(output_stem + ".png") > 0

    def test_Should_HandleDuplicatesAndExport_Given_FileWithDuplicates_When_FullPipelineExecuted(
        self, point_file_factory, tmp_dir
    ):
        # Arrange – file has a duplicate that should be silently ignored
        content = "0,0\n4,0\n2,4\n0,4\n0,0"  # last line is duplicate
        path = point_file_factory(content)
        output_stem = os.path.join(tmp_dir, "dedup_integration")

        # Act
        parser = PointParser()
        points = parser.parse_file(path)
        result = VoronoiCalculator().compute(points)
        figure = MatplotlibRenderer().render(result)
        ExporterFactory.create("svg").export(figure, output_stem)
        plt.close(figure)

        # Assert
        assert len(points) == 4  # duplicate removed
        assert os.path.exists(output_stem + ".svg")

    def test_Should_ProduceCorrectPointCount_Given_CommentsAndBlanks_When_FullPipelineExecuted(
        self, point_file_factory, tmp_dir
    ):
        # Arrange – points intentionally non-collinear: (1,2), (3,4), (1,6)
        content = "# header\n\n1,2\n3,4\n1,6\n\n# footer"
        path = point_file_factory(content)
        output_stem = os.path.join(tmp_dir, "comments_integration")

        # Act
        parser = PointParser()
        points = parser.parse_file(path)
        result = VoronoiCalculator().compute(points)
        figure = MatplotlibRenderer().render(result)
        ExporterFactory.create("svg").export(figure, output_stem)
        plt.close(figure)

        # Assert
        assert result.point_count == 3
        assert os.path.exists(output_stem + ".svg")
