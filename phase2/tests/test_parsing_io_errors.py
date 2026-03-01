from __future__ import annotations

from pathlib import Path
import pytest

from voronoi_app.domain.errors import PointFileParseError
from voronoi_app.infrastructure.parsing import PointFileParser


def test_Should_RaiseError_Given_MissingFile_When_ParseFile(tmp_path: Path):
    # Arrange
    parser = PointFileParser()
    missing = tmp_path / "does_not_exist.txt"

    # Act / Assert
    with pytest.raises(PointFileParseError) as exc:
        parser.parse_file(missing)
    assert "Input file not found" in str(exc.value)


def test_Should_RaiseError_Given_ReadFailure_When_ParseFile(tmp_path: Path, monkeypatch):
    # Arrange
    parser = PointFileParser()
    p = tmp_path / "points.txt"
    p.write_text("0,0\n10,0\n0,10\n10,10\n", encoding="utf-8")

    def boom(*args, **kwargs):
        raise OSError("read failed")

    monkeypatch.setattr(Path, "read_text", boom)

    # Act / Assert
    with pytest.raises(PointFileParseError) as exc:
        parser.parse_file(p)
    assert "Unable to read file" in str(exc.value)
