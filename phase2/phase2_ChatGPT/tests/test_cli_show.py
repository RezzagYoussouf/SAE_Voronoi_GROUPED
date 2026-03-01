from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt

from voronoi_app.cli import main


def test_Should_CallShow_Given_ShowFlag_When_RunCli(tmp_path: Path, monkeypatch):
    # Arrange
    inp = tmp_path / "points.txt"
    inp.write_text("0,0\n10,0\n0,10\n10,10\n", encoding="utf-8")
    out_svg = tmp_path / "out.svg"

    called = {"show": False}

    def fake_show():
        called["show"] = True

    monkeypatch.setattr(plt, "show", fake_show)

    argv = ["--input", str(inp), "--svg", str(out_svg), "--show"]

    # Act
    code = main(argv)

    # Assert
    assert code == 0
    assert called["show"] is True
