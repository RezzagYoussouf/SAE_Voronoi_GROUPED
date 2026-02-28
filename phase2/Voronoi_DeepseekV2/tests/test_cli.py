import pytest
import sys
import os
import tempfile
from src.cli import main

def test_Should_ExitWithZero_Given_HelpOption_When_RunningCli(monkeypatch, capsys):
    test_args = ["main.py", "-h"]
    monkeypatch.setattr(sys, 'argv', test_args)
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out

def test_Should_CreatePngFile_Given_ValidInputAndOutput_When_RunningCli(monkeypatch, tmp_path):
    input_file = tmp_path / "points.txt"
    input_file.write_text("0,0\n1,0\n0,1\n1,1\n")
    output_base = tmp_path / "output"
    test_args = ["main.py", str(input_file), "--output", str(output_base), "--noshow"]
    monkeypatch.setattr(sys, 'argv', test_args)
    main()
    png_file = tmp_path / "output.png"
    assert png_file.exists()

def test_Should_ExitSuccessfully_Given_ValidInputWithoutOutput_When_RunningCliWithNoshow(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("0,0\n1,0\n0,1\n1,1\n")
        input_file = f.name
    test_args = ["main.py", input_file, "--noshow"]
    monkeypatch.setattr(sys, 'argv', test_args)
    try:
        main()
    finally:
        os.unlink(input_file)

def test_Should_ExitWithOne_Given_NonexistentInputFile_When_RunningCli(monkeypatch):
    test_args = ["main.py", "fichier_inexistant.txt", "--noshow"]
    monkeypatch.setattr(sys, 'argv', test_args)
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1

def test_Should_ExitWithOne_Given_InvalidPointFormat_When_RunningCli(monkeypatch, tmp_path):
    input_file = tmp_path / "bad.txt"
    input_file.write_text("a,b\n")
    test_args = ["main.py", str(input_file), "--noshow"]
    monkeypatch.setattr(sys, 'argv', test_args)
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1

def test_Should_ExitWithOne_Given_DuplicatePoints_When_RunningCli(monkeypatch, tmp_path):
    input_file = tmp_path / "duplicate.txt"
    input_file.write_text("0,0\n1,1\n0,0\n")
    test_args = ["main.py", str(input_file), "--noshow"]
    monkeypatch.setattr(sys, 'argv', test_args)
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1

def test_Should_ExitWithOne_Given_InsufficientPoints_When_RunningCli(monkeypatch, tmp_path):
    input_file = tmp_path / "two_points.txt"
    input_file.write_text("0,0\n1,1\n")
    test_args = ["main.py", str(input_file), "--noshow"]
    monkeypatch.setattr(sys, 'argv', test_args)
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1