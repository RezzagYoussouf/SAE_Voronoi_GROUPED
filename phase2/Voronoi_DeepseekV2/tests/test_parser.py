import pytest
import tempfile
import os
from src.parser import parse_points_file
from src.models import Point, ParsingError, InvalidPointError, DuplicatePointError

def test_Should_ReturnPoints_Given_ValidFile_When_Parsing():
    content = "2,4\n5.3,4.5\n"
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        name = f.name
    try:
        points = parse_points_file(name)
        assert points == [Point(2, 4), Point(5.3, 4.5)]
    finally:
        os.unlink(name)

def test_Should_RaiseDuplicatePointError_Given_DuplicatePoints_When_Parsing():
    content = "2,4\n2,4\n"
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        name = f.name
    try:
        with pytest.raises(DuplicatePointError):
            parse_points_file(name)
    finally:
        os.unlink(name)

def test_Should_RaiseParsingError_Given_NonExistentFile_When_Parsing():
    with pytest.raises(ParsingError) as excinfo:
        parse_points_file("fichier_inexistant.txt")
    assert "Fichier introuvable" in str(excinfo.value)

def test_Should_RaiseParsingError_Given_EmptyFile_When_Parsing():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        name = f.name
    try:
        with pytest.raises(ParsingError) as excinfo:
            parse_points_file(name)
        assert "aucun point" in str(excinfo.value)
    finally:
        os.unlink(name)

def test_Should_RaiseParsingError_Given_InvalidFormat_When_Parsing():
    content = "2,4,6\n"
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        name = f.name
    try:
        with pytest.raises(ParsingError) as excinfo:
            parse_points_file(name)
        assert "format invalide" in str(excinfo.value)
    finally:
        os.unlink(name)

def test_Should_RaiseInvalidPointError_Given_NonNumericValues_When_Parsing():
    content = "a,b\n"
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        name = f.name
    try:
        with pytest.raises(InvalidPointError) as excinfo:
            parse_points_file(name)
        assert "non numériques" in str(excinfo.value)
    finally:
        os.unlink(name)

def test_Should_ReturnPoints_Given_FileWithEmptyLines_When_Parsing():
    content = "2,4\n\n5.3,4.5\n"
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        name = f.name
    try:
        points = parse_points_file(name)
        assert points == [Point(2, 4), Point(5.3, 4.5)]
    finally:
        os.unlink(name)