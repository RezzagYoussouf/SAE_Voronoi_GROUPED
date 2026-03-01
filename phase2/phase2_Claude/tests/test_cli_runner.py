"""
Tests for src/cli/cli_runner.py
"""

from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")

import pytest
from unittest.mock import patch, MagicMock

from src.cli.cli_runner import CLIRunner, EXIT_SUCCESS, EXIT_ERROR


class TestCLIRunnerArgParsing:

    def test_Should_ExitWithError_Given_NoArguments_When_RunCalled(self):
        # Arrange
        runner = CLIRunner()

        # Act / Assert – argparse prints to stderr and raises SystemExit
        with pytest.raises(SystemExit) as exc_info:
            runner.run([])
        assert exc_info.value.code != 0

    def test_Should_ExitWithError_Given_MissingInputFlag_When_RunCalled(self):
        # Arrange
        runner = CLIRunner()

        # Act / Assert
        with pytest.raises(SystemExit):
            runner.run(["--output", "out"])

    def test_Should_PrintHelp_Given_HelpFlag_When_RunCalled(self, capsys):
        # Arrange
        runner = CLIRunner()

        # Act / Assert
        with pytest.raises(SystemExit) as exc_info:
            runner.run(["--help"])
        assert exc_info.value.code == 0


class TestCLIRunnerPipeline:
    """Integration-style tests: full pipeline through run() with a real file."""

    def test_Should_ReturnSuccess_Given_ValidInputFile_When_RunCalled(
        self, point_file_factory, tmp_dir
    ):
        # Arrange
        runner = CLIRunner()
        path = point_file_factory("0,0\n4,0\n2,4\n0,4\n4,4")
        output = os.path.join(tmp_dir, "out")

        # Act
        code = runner.run(["-i", path, "-o", output, "-f", "svg"])

        # Assert
        assert code == EXIT_SUCCESS
        assert os.path.exists(output + ".svg")

    def test_Should_ReturnSuccess_Given_ValidInputFileAndPngFormat_When_RunCalled(
        self, point_file_factory, tmp_dir
    ):
        # Arrange
        runner = CLIRunner()
        path = point_file_factory("0,0\n4,0\n2,4\n0,4\n4,4")
        output = os.path.join(tmp_dir, "out_png")

        # Act
        code = runner.run(["-i", path, "-o", output, "-f", "png"])

        # Assert
        assert code == EXIT_SUCCESS
        assert os.path.exists(output + ".png")

    def test_Should_ReturnSuccessAndCreateBothFiles_Given_TwoFormats_When_RunCalled(
        self, point_file_factory, tmp_dir
    ):
        # Arrange
        runner = CLIRunner()
        path = point_file_factory("0,0\n4,0\n2,4\n0,4")
        output = os.path.join(tmp_dir, "dual")

        # Act
        code = runner.run(["-i", path, "-o", output, "-f", "svg", "-f", "png"])

        # Assert
        assert code == EXIT_SUCCESS
        assert os.path.exists(output + ".svg")
        assert os.path.exists(output + ".png")

    def test_Should_ReturnError_Given_NonExistentInputFile_When_RunCalled(self):
        # Arrange
        runner = CLIRunner()

        # Act
        code = runner.run(["-i", "does_not_exist.txt"])

        # Assert
        assert code == EXIT_ERROR

    def test_Should_ReturnError_Given_FileWithTooFewPoints_When_RunCalled(
        self, point_file_factory
    ):
        # Arrange
        runner = CLIRunner()
        path = point_file_factory("1,2\n3,4")  # only 2 points

        # Act
        code = runner.run(["-i", path])

        # Assert
        assert code == EXIT_ERROR

    def test_Should_ReturnError_Given_FileWithCollinearPoints_When_RunCalled(
        self, point_file_factory
    ):
        # Arrange
        runner = CLIRunner()
        path = point_file_factory("0,0\n1,1\n2,2")  # collinear

        # Act
        code = runner.run(["-i", path])

        # Assert
        assert code == EXIT_ERROR

    def test_Should_ReturnError_Given_FileWithInvalidLine_When_RunCalled(
        self, point_file_factory
    ):
        # Arrange
        runner = CLIRunner()
        path = point_file_factory("1,2\nbad\n3,4")

        # Act
        code = runner.run(["-i", path])

        # Assert
        assert code == EXIT_ERROR

    def test_Should_PrintWarning_Given_DuplicatePoints_When_RunCalled(
        self, point_file_factory, tmp_dir, capsys
    ):
        # Arrange
        runner = CLIRunner()
        path = point_file_factory("0,0\n4,0\n2,4\n4,4\n0,0")  # last 0,0 is duplicate
        output = os.path.join(tmp_dir, "dup")

        # Act
        code = runner.run(["-i", path, "-o", output, "-f", "svg"])

        # Assert
        assert code == EXIT_SUCCESS
        captured = capsys.readouterr()
        assert "WARN" in captured.err or "duplicate" in captured.err.lower()

    def test_Should_RespectNoAxesFlag_Given_NoAxesOption_When_RunCalled(
        self, point_file_factory, tmp_dir
    ):
        # Arrange
        runner = CLIRunner()
        path = point_file_factory("0,0\n4,0\n2,4\n0,4")
        output = os.path.join(tmp_dir, "no_axes")

        # Act
        code = runner.run(["-i", path, "-o", output, "-f", "svg", "--no-axes"])

        # Assert
        assert code == EXIT_SUCCESS

    def test_Should_DeduplicateFormats_Given_SameFormatTwice_When_RunCalled(
        self, point_file_factory, tmp_dir
    ):
        # Arrange
        runner = CLIRunner()
        path = point_file_factory("0,0\n4,0\n2,4\n0,4")
        output = os.path.join(tmp_dir, "dedup")

        # Act – specifying svg twice should not error
        code = runner.run(["-i", path, "-o", output, "-f", "svg", "-f", "svg"])

        # Assert
        assert code == EXIT_SUCCESS
        assert os.path.exists(output + ".svg")
