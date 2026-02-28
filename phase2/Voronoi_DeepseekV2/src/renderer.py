import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import numpy as np
from scipy.spatial import Voronoi
from .models import VoronoiResult


def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions by adding points at infinity.
    """
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = np.max(np.linalg.norm(vor.points - center, axis=1)) * 2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge
            t = vor.points[p2] - vor.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.array([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        new_regions.append(new_region.tolist())

    return new_regions, np.array(new_vertices)


def bounding_box(points, margin=0.1):
    if not points:
        return 0, 1, 0, 1
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    dx = (xmax - xmin) * margin or 0.1
    dy = (ymax - ymin) * margin or 0.1
    return xmin - dx, xmax + dx, ymin - dy, ymax + dy


def render_voronoi(result: VoronoiResult, show_labels=True, figsize=(10, 8)) -> Figure:
    points_array = np.array([[p.x, p.y] for p in result.points])
    vor = Voronoi(points_array)

    # Convertir toutes les régions en polygones finis avec un rayon plus grand (x5)
    # On peut passer le radius explicitement, par exemple 5 fois la distance max
    center = vor.points.mean(axis=0)
    max_dist = np.max(np.linalg.norm(vor.points - center, axis=1))
    radius = max_dist * 5  # <-- vous avez modifié ici
    regions, vertices = voronoi_finite_polygons_2d(vor, radius=radius)

    fig, ax = plt.subplots(figsize=figsize)

    # Palette de couleurs distinctes (autant que de points)
    cmap = plt.cm.tab20
    n_points = len(result.points)
    colors = [cmap(i % 20) for i in range(n_points)]

    # Tracer chaque région avec sa couleur
    for i, region in enumerate(regions):
        polygon = vertices[region]
        ax.fill(polygon[:, 0], polygon[:, 1],
                facecolor=colors[i], edgecolor='black', linewidth=0.8, alpha=0.5)

    # Tracer les points générateurs
    xs = [p.x for p in result.points]
    ys = [p.y for p in result.points]
    ax.scatter(xs, ys, color='red', s=40, zorder=5, label='Points générateurs')

    # Étiquettes (A, B, C, ...)
    if show_labels:
        letters = [chr(65 + i) for i in range(n_points)]
        for i, (x, y) in enumerate(zip(xs, ys)):
            ax.annotate(letters[i], (x, y), xytext=(5, 5),
                        textcoords='offset points', fontsize=12, color='black')

    # Ajouter une légende indiquant les cellules de Voronoï
    legend_patches = []
    for i in range(n_points):
        if i < 26:
            point_label = chr(65 + i)  # A, B, C, ...
        else:
            point_label = str(i + 1)   # au-delà de Z on utilise des nombres
        patch = mpatches.Patch(color=colors[i], label=f"Cellule de {point_label}", alpha=0.5)
        legend_patches.append(patch)

    # Placer la légende à l'extérieur du graphique (à droite)
    ax.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1),
              loc='upper left', borderaxespad=0., ncol=2, fontsize=8,
              title="Points")

    # Limites
    xmin, xmax, ymin, ymax = bounding_box(result.points)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Diagramme de Voronoï')
    ax.grid(True, linestyle='--', alpha=0.7)

    return fig


def save_figure(fig: Figure, filename: str, dpi=300):
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    print(f"Figure sauvegardée sous : {filename}")