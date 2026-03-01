from typing import List
import numpy as np
from scipy.spatial import Voronoi as ScipyVoronoi
from .models import Point, VoronoiResult


class VoronoiCalculator:
    def compute(self, points: List[Point]) -> VoronoiResult:
        arr = np.array([[p.x, p.y] for p in points])
        vor = ScipyVoronoi(arr)

        result = VoronoiResult(
            points=points,
            vertices=vor.vertices,
            regions=vor.regions,
            point_region=vor.point_region
        )

        self._compute_finite_regions(result, vor)
        return result

    def _compute_finite_regions(self, result: VoronoiResult, vor: ScipyVoronoi):
        vertices = vor.vertices
        finite_regions = []
        used_vertices = set()

        for region in vor.regions:
            if not region or -1 in region:
                continue
            finite_regions.append(region)
            used_vertices.update(region)

        if not used_vertices:
            result.finite_regions = []
            result.finite_vertices = np.array([])
            return

        used_vertices = sorted(used_vertices)
        index_map = {old: new for new, old in enumerate(used_vertices)}
        finite_vertices = vertices[used_vertices]

        reindexed_regions = []
        for region in finite_regions:
            reindexed_regions.append([index_map[v] for v in region])

        result.finite_regions = reindexed_regions
        result.finite_vertices = finite_vertices