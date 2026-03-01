from __future__ import annotations

from voronoi_app.domain.errors import DuplicatePointError, PointFileParseError
from voronoi_app.infrastructure.parsing import PointFileParser


def test_Should_ParsePoints_Given_ValidText_When_ParseText():
    # Arrange
    parser = PointFileParser()
    text = "2,4\n5.3, 4.5\n18,29\n12.5,23.7\n"

    # Act
    parsed = parser.parse_text(text, source_name="in-memory")

    # Assert
    assert len(parsed.points) == 4
    assert parsed.points[0].x == 2.0
    assert parsed.points[1].y == 4.5


def test_Should_RaiseError_Given_EmptyLine_When_ParseText():
    # Arrange
    parser = PointFileParser()
    text = "2,4\n\n5,6\n"

    # Act / Assert
    try:
        parser.parse_text(text, source_name="file.txt")
        assert False, "Expected PointFileParseError was not raised"
    except PointFileParseError as exc:
        assert "line 2 is empty" in str(exc)


def test_Should_RaiseError_Given_InvalidFormat_When_ParseText():
    # Arrange
    parser = PointFileParser()
    text = "2,4,7\n"

    # Act / Assert
    try:
        parser.parse_text(text, source_name="file.txt")
        assert False, "Expected PointFileParseError was not raised"
    except PointFileParseError as exc:
        assert "invalid format" in str(exc)


def test_Should_RaiseError_Given_NonNumericValues_When_ParseText():
    # Arrange
    parser = PointFileParser()
    text = "a,4\n"

    # Act / Assert
    try:
        parser.parse_text(text, source_name="file.txt")
        assert False, "Expected PointFileParseError was not raised"
    except PointFileParseError as exc:
        assert "non-numeric" in str(exc)


def test_Should_RaiseError_Given_DuplicatePoint_When_ParseText():
    # Arrange
    parser = PointFileParser()
    text = "2,4\n2,4\n"

    # Act / Assert
    try:
        parser.parse_text(text, source_name="file.txt")
        assert False, "Expected DuplicatePointError was not raised"
    except DuplicatePointError as exc:
        assert "duplicate point" in str(exc)


def test_Should_RaiseError_Given_OnlyOnePoint_When_ParseText():
    # Arrange
    parser = PointFileParser()
    text = "2,4\n"

    # Act / Assert
    try:
        parser.parse_text(text, source_name="file.txt")
        assert False, "Expected PointFileParseError was not raised"
    except PointFileParseError as exc:
        assert "at least 4 points" in str(exc)

def test_Should_RaiseError_Given_LessThanFourPoints_When_ParseText():
    # Arrange
    parser = PointFileParser()
    text = "0,0\n1,1\n2,2\n"

    # Act / Assert
    try:
        parser.parse_text(text, source_name="file.txt")
        assert False, "Expected PointFileParseError was not raised"
    except PointFileParseError as exc:
        assert "at least 4 points" in str(exc)
