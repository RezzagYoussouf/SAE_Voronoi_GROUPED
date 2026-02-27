"""
Tests for src/models/errors.py
"""

from __future__ import annotations

import pytest
from src.models.errors import (
    CollinearPointsError,
    ExportError,
    InsufficientPointsError,
    ParseError,
    VoronoiAppError,
)


class TestParseError:
    def test_Should_IncludeLineNumber_Given_LineNumberProvided_When_Created(self):
        # Arrange / Act
        error = ParseError("bad value", line_number=5)

        # Assert
        assert error.line_number == 5
        assert "Line 5" in str(error)
        assert "bad value" in str(error)

    def test_Should_OmitLinePrefix_Given_NoLineNumber_When_Created(self):
        # Arrange / Act
        error = ParseError("generic error")

        # Assert
        assert error.line_number is None
        assert "Line" not in str(error)
        assert "generic error" in str(error)

    def test_Should_BeSubclassOfVoronoiAppError_Given_ParseError_When_Checked(self):
        # Arrange / Act / Assert
        assert issubclass(ParseError, VoronoiAppError)


class TestInsufficientPointsError:
    def test_Should_IncludeActualCount_Given_FewPoints_When_Created(self):
        # Arrange / Act
        error = InsufficientPointsError(actual=2)

        # Assert
        assert error.actual == 2
        assert "2" in str(error)

    def test_Should_MentionMinimumRequirement_Given_AnyCount_When_Created(self):
        # Arrange / Act
        error = InsufficientPointsError(actual=1)

        # Assert
        assert str(InsufficientPointsError.MINIMUM_POINTS) in str(error)

    def test_Should_BeSubclassOfVoronoiAppError_Given_InsufficientPointsError_When_Checked(self):
        # Arrange / Act / Assert
        assert issubclass(InsufficientPointsError, VoronoiAppError)


class TestCollinearPointsError:
    def test_Should_ProduceDescriptiveMessage_Given_NoArgs_When_Created(self):
        # Arrange / Act
        error = CollinearPointsError()

        # Assert
        assert "collinear" in str(error).lower()

    def test_Should_BeSubclassOfVoronoiAppError_Given_CollinearPointsError_When_Checked(self):
        # Arrange / Act / Assert
        assert issubclass(CollinearPointsError, VoronoiAppError)


class TestExportError:
    def test_Should_StoreMessage_Given_Message_When_Created(self):
        # Arrange / Act
        error = ExportError("disk full")

        # Assert
        assert "disk full" in str(error)

    def test_Should_BeSubclassOfVoronoiAppError_Given_ExportError_When_Checked(self):
        # Arrange / Act / Assert
        assert issubclass(ExportError, VoronoiAppError)
