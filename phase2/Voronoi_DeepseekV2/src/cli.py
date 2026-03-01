import argparse
import sys
import os
import matplotlib.pyplot as plt
from .parser import parse_points_file
from .calculator import VoronoiCalculator
from .renderer import render_voronoi, save_figure
from .models import VoronoiError


def main():
    parser = argparse.ArgumentParser(description="Générateur de diagramme de Voronoï")
    parser.add_argument('input', help="Fichier de points (format: x,y par ligne)")
    parser.add_argument('--output', '-o', default='voronoi_output', help="Nom de base du fichier de sortie (sans extension)")
    parser.add_argument('--format', '-f', choices=['png', 'svg'], default='png', help="Format d'export (png ou svg)")
    parser.add_argument('--noshow', action='store_true', help="Ne pas afficher la fenêtre (utile avec --output)")

    args = parser.parse_args()

    try:
        points = parse_points_file(args.input)
        calculator = VoronoiCalculator()
        result = calculator.compute(points)
        fig = render_voronoi(result, show_labels=True)

        if args.output:
            # Créer le dossier output s'il n'existe pas
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, args.output + '.' + args.format)
            save_figure(fig, output_path)
            print(f"Diagramme exporté : {output_path}")
        if not args.noshow:
            plt.show()
        else:
            plt.close(fig)

    except VoronoiError as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue: {e}", file=sys.stderr)
        sys.exit(1)