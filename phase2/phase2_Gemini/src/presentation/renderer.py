import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d, Voronoi

class MatplotlibRenderer:
    """Gère l'affichage interactif et l'export des diagrammes."""
    
    def __init__(self):
        self.figure_size = (8, 6)
        self.point_size = 10
        
    def render_interactive(self, voronoi_diagram: Voronoi, title: str = "Diagramme de Voronoï"):
        """Ouvre une fenêtre permettant de zoomer/panner."""
        fig = plt.figure(figsize=self.figure_size)
        ax = fig.add_subplot(111)
        ax.set_title(title)
        
        voronoi_plot_2d(voronoi_diagram, ax=ax, show_vertices=False, point_size=self.point_size)
        plt.tight_layout()
        plt.show()

    def export(self, voronoi_diagram: Voronoi, output_path: str):
        """Sauvegarde le rendu en image ou vectoriel."""
        fig = plt.figure(figsize=self.figure_size)
        ax = fig.add_subplot(111)
        
        voronoi_plot_2d(voronoi_diagram, ax=ax, show_vertices=False, point_size=self.point_size)
        plt.tight_layout()
        
        try:
            # Déduit le format à partir de l'extension (ex: .svg, .png)
            plt.savefig(output_path, format=output_path.split('.')[-1])
        finally:
            plt.close(fig)  # Sécurité pour libérer la mémoire