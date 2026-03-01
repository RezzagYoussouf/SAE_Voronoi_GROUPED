"""
Tests for src/parser/point_parser.py
TDD: tests written before implementation to define expected behaviour.
All tests follow the AAA (Arrange / Act / Assert) pattern.
Naming convention: Should_<Expected>_Given_<Context>_When_<Action>
"""

from __future__ import annotations

import os
import pytest

from src.models.errors import ParseError
from src.models.point import Point
from src.parser.point_parser import PointParser


class TestParseTextValidInput:
    """Tests that parse_text succeeds on well-formed input."""

    def test_Should_ReturnThreePoints_Given_ThreeValidLines_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "2,4\n5.3,4.5\n18,29"

        # Act
        points = parser.parse_text(text)

        # Assert
        assert len(points) == 3
        assert Point(2.0, 4.0) in points
        assert Point(5.3, 4.5) in points
        assert Point(18.0, 29.0) in points

    def test_Should_IgnoreEmptyLines_Given_TextWithBlankLines_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "1,2\n\n3,4\n\n5,6"

        # Act
        points = parser.parse_text(text)

        # Assert
        assert len(points) == 3

    def test_Should_IgnoreCommentLines_Given_TextWithHashComments_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "# this is a comment\n1,2\n# another comment\n3,4"

        # Act
        points = parser.parse_text(text)

        # Assert
        assert len(points) == 2

    def test_Should_StripWhitespace_Given_LinesWithLeadingTrailingSpaces_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "  1 , 2  \n  3.0 , 4.5  "

        # Act
        points = parser.parse_text(text)

        # Assert
        assert Point(1.0, 2.0) in points
        assert Point(3.0, 4.5) in points

    def test_Should_DeduplicatePoints_Given_DuplicateLines_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "1,2\n1,2\n3,4"

        # Act
        points = parser.parse_text(text)

        # Assert
        assert len(points) == 2  # duplicate removed
        assert len(parser.warnings) == 1

    def test_Should_RecordWarning_Given_DuplicateLine_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "1,2\n1,2"

        # Act
        parser.parse_text(text)

        # Assert
        assert len(parser.warnings) == 1
        assert "duplicate" in parser.warnings[0].lower()

    def test_Should_ParseNegativeCoordinates_Given_NegativeValues_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "-1,-2\n-3.5,4.5"

        # Act
        points = parser.parse_text(text)

        # Assert
        assert Point(-1.0, -2.0) in points
        assert Point(-3.5, 4.5) in points

    def test_Should_ReturnEmptyList_Given_AllCommentLines_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "# only comments\n# nothing here"

        # Act
        points = parser.parse_text(text)

        # Assert
        assert points == []

    def test_Should_ReturnEmptyList_Given_EmptyString_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()

        # Act
        points = parser.parse_text("")

        # Assert
        assert points == []

    def test_Should_ParseScientificNotation_Given_ScientificValues_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "1e2,2e3\n1.5e-1,3.0e0"

        # Act
        points = parser.parse_text(text)

        # Assert
        assert Point(100.0, 2000.0) in points
        assert Point(0.15, 3.0) in points

    def test_Should_PreserveInsertionOrder_Given_OrderedInput_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "10,20\n30,40\n50,60"

        # Act
        points = parser.parse_text(text)

        # Assert
        assert points[0] == Point(10.0, 20.0)
        assert points[1] == Point(30.0, 40.0)
        assert points[2] == Point(50.0, 60.0)


class TestParseTextInvalidInput:
    """Tests that parse_text raises ParseError on malformed input."""

    def test_Should_RaiseParseError_Given_LineWithOneValue_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "42"

        # Act / Assert
        with pytest.raises(ParseError) as exc_info:
            parser.parse_text(text)
        assert exc_info.value.line_number == 1

    def test_Should_RaiseParseError_Given_LineWithThreeValues_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "1,2,3"

        # Act / Assert
        with pytest.raises(ParseError):
            parser.parse_text(text)

    def test_Should_RaiseParseError_Given_NonNumericX_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "abc,4"

        # Act / Assert
        with pytest.raises(ParseError) as exc_info:
            parser.parse_text(text)
        assert "abc" in str(exc_info.value)

    def test_Should_RaiseParseError_Given_NonNumericY_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "1,xyz"

        # Act / Assert
        with pytest.raises(ParseError) as exc_info:
            parser.parse_text(text)
        assert "xyz" in str(exc_info.value)

    def test_Should_RaiseParseError_Given_MissingY_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "1,"

        # Act / Assert
        with pytest.raises(ParseError):
            parser.parse_text(text)

    def test_Should_RaiseParseError_Given_MissingX_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = ",5"

        # Act / Assert
        with pytest.raises(ParseError):
            parser.parse_text(text)

    def test_Should_IncludeLineNumber_Given_ErrorOnSecondLine_When_ParseTextCalled(self):
        # Arrange
        parser = PointParser()
        text = "1,2\nbad_line"

        # Act / Assert
        with pytest.raises(ParseError) as exc_info:
            parser.parse_text(text)
        assert exc_info.value.line_number == 2


class TestParseFile:
    """Tests for parse_file: file I/O handling."""

    def test_Should_ReturnPoints_Given_ValidFile_When_ParseFileCalled(
        self, point_file_factory
    ):
        # Arrange
        parser = PointParser()
        path = point_file_factory("1,2\n3,4\n5,6")

        # Act
        points = parser.parse_file(path)

        # Assert
        assert len(points) == 3

    def test_Should_RaiseFileNotFoundError_Given_NonExistentPath_When_ParseFileCalled(self):
        # Arrange
        parser = PointParser()
        path = "/nonexistent/path/to/file.txt"

        # Act / Assert
        with pytest.raises(FileNotFoundError):
            parser.parse_file(path)

    def test_Should_RaiseValueError_Given_DirectoryPath_When_ParseFileCalled(
        self, tmp_dir
    ):
        # Arrange
        parser = PointParser()

        # Act / Assert
        with pytest.raises(ValueError):
            parser.parse_file(tmp_dir)

    def test_Should_ParseFileCorrectly_Given_FileWithCommentsAndBlanks_When_ParseFileCalled(
        self, point_file_factory
    ):
        # Arrange
        parser = PointParser()
        content = "# header\n1,2\n\n3,4\n# footer"
        path = point_file_factory(content)

        # Act
        points = parser.parse_file(path)

        # Assert
        assert len(points) == 2

    def test_Should_RaiseParseError_Given_FileWithInvalidLine_When_ParseFileCalled(
        self, point_file_factory
    ):
        # Arrange
        parser = PointParser()
        path = point_file_factory("1,2\nnot_a_number,4")

        # Act / Assert
        with pytest.raises(ParseError):
            parser.parse_file(path)
