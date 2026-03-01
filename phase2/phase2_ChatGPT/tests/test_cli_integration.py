from __future__ import annotations

from pathlib import Path

from voronoi_app.cli import main


def test_Should_CreateOutputs_Given_ValidInput_When_RunCli(tmp_path: Path):
    # Arrange
    inp = tmp_path / "points.txt"
    inp.write_text("0,0\n10,0\n0,10\n10,10\n", encoding="utf-8")
    out_svg = tmp_path / "out.svg"
    out_png = tmp_path / "out.png"

    argv = [
        "--input", str(inp),
        "--svg", str(out_svg),
        "--png", str(out_png),
        "--padding", "5",
    ]

    # Act
    code = main(argv)

    # Assert
    assert code == 0
    assert out_svg.exists()
    assert out_png.exists()
    assert out_svg.read_text(encoding="utf-8").startswith("<svg") or "<svg" in out_svg.read_text(encoding="utf-8")