"""
Entry point for the Voronoi Diagram application – Phase 2.
SAÉ S6 – BUT3 Informatique, Spécialité Développement d'Applications.

Run:
    python main.py --help
    python main.py -i data/points.txt -o output/diagram -f svg -f png
"""

import sys
import os

# Allow running from the phase2/ directory without installing the package.
sys.path.insert(0, os.path.dirname(__file__))

from src.cli.cli_runner import CLIRunner

if __name__ == "__main__":
    runner = CLIRunner()
    sys.exit(runner.run())
