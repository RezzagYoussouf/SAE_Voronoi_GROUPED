from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from voronoi_app.application.voronoi_service import VoronoiService
from voronoi_app.infrastructure.export_svg import SvgExporter
from voronoi_app.infrastructure.parsing import PointFileParser
from voronoi_app.infrastructure.plotter import MatplotlibRenderer
from voronoi_app.utils.geometry import parse_bounds


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="voronoi_app",
        description="Compute and visualize Voronoi diagram from a file of 2D points (x,y per line).",
    )
    parser.add_argument("--input", required=True, type=Path, help="Input text file containing points.")
    parser.add_argument("--svg", type=Path, default=None, help="Output SVG path.")
    parser.add_argument("--png", type=Path, default=None, help="Output PNG path.")
    parser.add_argument("--show", action="store_true", help="Show interactive Matplotlib window (zoom/pan).")
    parser.add_argument(
        "--bounds",
        type=str,
        default=None,
        help="Optional bounds: 'minx,miny,maxx,maxy'. If omitted, bounds are computed from points.",
    )
    parser.add_argument("--padding", type=float, default=10.0, help="Padding added around points if bounds omitted.")
    parser.add_argument("--no-axes", action="store_true", help="Hide axes in plot.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    point_parser = PointFileParser()
    voronoi_service = VoronoiService()
    svg_exporter = SvgExporter()
    renderer = MatplotlibRenderer()

    parsed = point_parser.parse_file(args.input)

    bounds = parse_bounds(args.bounds) if args.bounds else None
    result = voronoi_service.compute(parsed.points, bounds=bounds, padding=args.padding)

    fig = renderer.render(result, style=None if not args.no_axes else type("S", (), {"show_axes": False})())

    if args.svg is not None:
        svg_exporter.export(result, args.svg)

    if args.png is not None:
        renderer.export_png(fig, args.png)

    if args.show:
        plt.show()
    else:
        plt.close(fig)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())