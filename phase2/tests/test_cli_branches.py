from __future__ import annotations

from pathlib import Path

from voronoi_app.cli import main


def test_Should_RunWithNoAxes_Given_ValidInput_When_RunCli(tmp_path: Path):
    # Arrange
    inp = tmp_path / "points.txt"
    inp.write_text("0,0\n10,0\n0,10\n10,10\n", encoding="utf-8")
    out_svg = tmp_path / "out.svg"

    argv = [
        "--input", str(inp),
        "--svg", str(out_svg),
        "--no-axes",
    ]

    # Act
    code = main(argv)

    # Assert
    assert code == 0
    assert out_svg.exists()


def test_Should_RunWithBounds_Given_ValidInput_When_RunCli(tmp_path: Path):
    # Arrange
    inp = tmp_path / "points.txt"
    inp.write_text("0,0\n10,0\n0,10\n10,10\n", encoding="utf-8")
    out_svg = tmp_path / "out.svg"

    argv = [
        "--input", str(inp),
        "--svg", str(out_svg),
        "--bounds=-5,-5,15,15",
    ]

    # Act
    code = main(argv)

    # Assert
    assert code == 0
    assert out_svg.exists()
