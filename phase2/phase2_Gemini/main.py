import argparse
import sys
from src.io.parser import CsvPointParser
from src.core.calculator import VoronoiDiagramCalculator
from src.presentation.renderer import MatplotlibRenderer
from src.domain.exceptions import VoronoiAppError

def main():
    parser = argparse.ArgumentParser(description="Générateur de Diagrammes de Voronoï")
    parser.add_argument("input_file", help="Fichier texte contenant les points (ex: points.txt)")
    parser.add_argument("--export-svg", dest="svg_output", help="Chemin d'export SVG (ex: out.svg)")
    parser.add_argument("--export-png", dest="png_output", help="Chemin d'export PNG (ex: out.png)")
    parser.add_argument("--no-gui", action="store_true", help="Désactive l'affichage interactif")
    
    args = parser.parse_args()

    # Injection des dépendances simple
    file_parser = CsvPointParser()
    calculator = VoronoiDiagramCalculator()
    renderer = MatplotlibRenderer()

    try:
        print(f"[*] Analyse du fichier : {args.input_file}")
        points = file_parser.parse(args.input_file)
        print(f"[*] {len(points)} points valides récupérés.")

        print("[*] Calcul du diagramme...")
        voronoi_result = calculator.compute(points)

        if args.svg_output:
            print(f"[*] Export SVG vers : {args.svg_output}")
            renderer.export(voronoi_result, args.svg_output)
        
        if args.png_output:
            print(f"[*] Export PNG vers : {args.png_output}")
            renderer.export(voronoi_result, args.png_output)

        if not args.no_gui:
            print("[*] Affichage de l'interface graphique (Fermer la fenêtre pour quitter)...")
            renderer.render_interactive(voronoi_result)

        print("[*] Succès.")

    except VoronoiAppError as e:
        print(f"\n[ERREUR FONCTIONNELLE] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERREUR CRITIQUE] {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()