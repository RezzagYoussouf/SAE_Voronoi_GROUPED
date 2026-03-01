import numpy as np
from scipy.spatial import Voronoi, QhullError
from typing import List
from src.domain.models import Point2D
from src.domain.exceptions import CalculationError

class VoronoiDiagramCalculator:
    """Encapsule la logique métier du calcul du diagramme."""
    
    def compute(self, points: List[Point2D]) -> Voronoi:
        try:
            # Transformation des modèles du domaine pour la librairie (numpy)
            coords = np.array([[p.x, p.y] for p in points])
            return Voronoi(coords)
        except QhullError as e:
            raise CalculationError(f"Erreur mathématique (points colinéaires ou superposés ?) : {e}")
        except Exception as e:
            raise CalculationError(f"Erreur inattendue lors du calcul : {e}")