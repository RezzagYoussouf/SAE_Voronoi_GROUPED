"""
Module: cli_runner.py
Responsibility: Parse command-line arguments and orchestrate the pipeline.
SOLID:
  SRP  – CLI argument handling is isolated here; the pipeline steps live in
         their own modules.
  DIP  – depends on abstractions (BaseRenderer, BaseExporter) and on the
         concrete classes only via the factory.
  OCP  – adding a new export format requires only an update to ExporterFactory.

Why CLI over GUI?
  A CLI is portable, scriptable, and trivially testable without a display
  server.  It aligns perfectly with "KISS" and student machine compatibility
  (no additional GUI toolkit required).

Usage (see README or --help):
    python main.py -i points.txt
    python main.py -i points.txt -o output/voronoi -f svg
    python main.py -i points.txt -f png --show
    python main.py -i points.txt -f svg -f png --no-axes
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from typing import Sequence

import matplotlib
import matplotlib.pyplot as plt

from src.export.exporter_factory import ExporterFactory
from src.models.errors import (
    CollinearPointsError,
    ExportError,
    InsufficientPointsError,
    ParseError,
    VoronoiAppError,
)
from src.parser.point_parser import PointParser
from src.rendering.matplotlib_renderer import MatplotlibRenderer
from src.voronoi.voronoi_calculator import VoronoiCalculator

# ── Constants ────────────────────────────────────────────────────────────────
DEFAULT_OUTPUT_STEM = "voronoi_output"
DEFAULT_FORMAT = "svg"
EXIT_SUCCESS = 0
EXIT_ERROR = 1


class CLIRunner:
    """
    Orchestrates the full pipeline from file path to exported diagram.

    Pipeline:
        1. Parse arguments.
        2. Read and validate points from input file.
        3. Compute Voronoi diagram.
        4. Render to a matplotlib Figure.
        5. Export to requested format(s).
        6. Optionally display the interactive window.
    """

    def __init__(self) -> None:
        self._parser = self._build_arg_parser()

    # ── Public API ───────────────────────────────────────────────────────────

    def run(self, argv: Sequence[str] | None = None) -> int:
        """
        Execute the CLI pipeline.

        Args:
            argv: Argument list (defaults to sys.argv[1:]).

        Returns:
            Exit code: 0 on success, 1 on error.
        """
        args = self._parser.parse_args(argv)

        try:
            return self._execute_pipeline(args)
        except (FileNotFoundError, PermissionError) as exc:
            self._print_error(f"File error: {exc}")
        except ParseError as exc:
            self._print_error(f"Parse error: {exc}")
        except InsufficientPointsError as exc:
            self._print_error(f"Insufficient points: {exc}")
        except CollinearPointsError as exc:
            self._print_error(f"Collinear points: {exc}")
        except ExportError as exc:
            self._print_error(f"Export error: {exc}")
        except VoronoiAppError as exc:
            self._print_error(f"Application error: {exc}")

        return EXIT_ERROR

    # ── Private helpers ──────────────────────────────────────────────────────

    def _execute_pipeline(self, args: argparse.Namespace) -> int:
        """Run the pipeline steps in sequence."""
        # Step 1 – Parse points
        point_parser = PointParser()
        points = point_parser.parse_file(args.input)
        self._report_parse_warnings(point_parser.warnings)
        print(f"[INFO] Loaded {len(points)} points from '{args.input}'.")

        # Step 2 – Compute Voronoi
        calculator = VoronoiCalculator()
        result = calculator.compute(points)
        print("[INFO] Voronoi diagram computed successfully.")

        # Step 3 – Render
        if not args.show:
            # Headless mode: use non-interactive Agg backend for export only
            plt.switch_backend("Agg")

        renderer = MatplotlibRenderer(show_axes=not args.no_axes)
        figure = renderer.render(result)

        # Step 4 – Export
        formats: list[str] = list(dict.fromkeys(args.format))  # deduplicate
        for fmt in formats:
            exporter = ExporterFactory.create(fmt)
            output_stem = args.output.removesuffix(f".{fmt}")
            exporter.export(figure, output_stem)
            print(f"[INFO] Exported {fmt.upper()} → {output_stem}.{fmt}")

        # Step 5 – Show interactive window (if requested)
        if args.show:
            plt.show()

        plt.close(figure)
        return EXIT_SUCCESS

    @staticmethod
    def _print_error(message: str) -> None:
        print(f"[ERROR] {message}", file=sys.stderr)

    @staticmethod
    def _report_parse_warnings(warnings: list[str]) -> None:
        for warning in warnings:
            print(f"[WARN]  {warning}", file=sys.stderr)

    @staticmethod
    def _build_arg_parser() -> argparse.ArgumentParser:
        """Build the argparse parser with all supported options."""
        parser = argparse.ArgumentParser(
            prog="voronoi",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                Voronoi Diagram Generator – Phase 2 (SAÉ S6)
                ─────────────────────────────────────────────
                Reads a 2-D point file, computes the Voronoi diagram and
                exports it to SVG and/or PNG.

                Example:
                  python main.py -i data/points.txt -o output/diagram -f svg -f png
                """
            ),
        )

        parser.add_argument(
            "-i", "--input",
            required=True,
            metavar="FILE",
            help="Path to the input point file (comma-separated x,y values).",
        )
        parser.add_argument(
            "-o", "--output",
            default=DEFAULT_OUTPUT_STEM,
            metavar="STEM",
            help=(
                f"Output file stem (without extension).  "
                f"Default: '{DEFAULT_OUTPUT_STEM}'."
            ),
        )
        parser.add_argument(
            "-f", "--format",
            action="append",
            default=None,
            choices=ExporterFactory.supported_formats(),
            metavar="FORMAT",
            help=(
                "Export format: svg or png.  "
                "Can be repeated to export multiple formats.  "
                "Default: svg."
            ),
        )
        parser.add_argument(
            "--show",
            action="store_true",
            help="Display the interactive Matplotlib window after export.",
        )
        parser.add_argument(
            "--no-axes",
            action="store_true",
            dest="no_axes",
            help="Hide axes and grid in the rendered diagram.",
        )

        return parser

    def _normalise_formats(self, args: argparse.Namespace) -> None:
        """Ensure at least one export format is set."""
        if args.format is None:
            args.format = [DEFAULT_FORMAT]
