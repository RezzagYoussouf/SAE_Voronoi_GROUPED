from main import Point
from segment import Segment

class Triangle():

    def __init__(self, segment1 : Segment, segment2 : Segment, segment3 : Segment):
        self._segment1 = segment1
        self._segment2 = segment2
        self._segment3 = segment3
        self._cercle_circonscrit = None
        self._rayon_cercle_circonscrit = None
    
    def calculer_centre_circonscrit(self):
        # Calculer les médiatrices des côtés du triangle
        x_mediatrice_AB, y_mediatrice_AB = self._segment1.definir_mediatrice(self._segment1._PointA, self._segment1._PointB)
        x_mediatrice_BC, y_mediatrice_BC = self._segment2.definir_mediatrice(self._segment2._PointA, self._segment2._PointB)
        x_mediatrice_AC, y_mediatrice_AC = self._segment3.definir_mediatrice(self._segment3._PointA, self._segment3._PointB)

        # Calculer les pentes des médiatrices
        pente_perpendiculaire_AB = self._segment1.calculer_pente_perpendiculaire(self._segment1._PointA, self._segment1._PointB)
        pente_perpendiculaire_BC = self._segment2.calculer_pente_perpendiculaire(self._segment2._PointA, self._segment2._PointB)

        # Trouver l'intersection des médiatrices pour obtenir le centre du cercle circonscrit
        # Droite 1 : y = pente1 * (x - x1) + y1  (médiatrice de AB passant par son milieu)
        # Droite 2 : y = pente2 * (x - x2) + y2  (médiatrice de BC passant par son milieu)
        m1 = pente_perpendiculaire_AB
        m2 = pente_perpendiculaire_BC
        x1, y1 = x_mediatrice_AB, y_mediatrice_AB
        x2, y2 = x_mediatrice_BC, y_mediatrice_BC

        if m1 is not None and m2 is not None and m1 != m2:
            # Cas général : deux pentes définies
            x_inter = (m1 * x1 - m2 * x2 + y2 - y1) / (m1 - m2)
            y_inter = m1 * (x_inter - x1) + y1
            coordonnées_intersection = (x_inter, y_inter) #Utile pour avoir le centre du cercle circonscrit du triangle
        elif m1 is None:
            # Médiatrice AB est verticale (x = x1)
            x_inter = x1
            y_inter = m2 * (x_inter - x2) + y2
        elif m2 is None:
            # Médiatrice BC est verticale (x = x2)
            x_inter = x2
            y_inter = m1 * (x_inter - x1) + y1
        else:
            return None  # Droites parallèles, pas d'intersection
        
        # Sauvegarder le point d'intersection (centre du cercle circonscrit)
        self._cercle_circonscrit = Point(x_inter, y_inter)
        return self._cercle_circonscrit
    
    def calculer_rayon_circonscrit(self, sommet : Point):
        if self._cercle_circonscrit is None:
            self.calculer_centre_circonscrit()
        self._rayon_cercle_circonscrit = self._cercle_circonscrit.return_distance(sommet)
        return self._rayon_cercle_circonscrit
    
    def contient_point(self, point : Point):
        if self._cercle_circonscrit is None:
            self.calculer_centre_circonscrit()
        if self._rayon_cercle_circonscrit is None:
            self.calculer_rayon_circonscrit(self._segment1._PointA)  

        distance_au_centre = self._cercle_circonscrit.return_distance(point)
        return distance_au_centre <= self._rayon_cercle_circonscrit #retourne True si il est dans le cercle circonscrit, False sinon
    
    def partage_un_segment(self, un_autre_triangle):
        mes_segments = [self._segment1, self._segment2, self._segment3]
        autre_segments = [un_autre_triangle._segment1, un_autre_triangle._segment2, un_autre_triangle._segment3]
        for s1 in mes_segments:
            for s2 in autre_segments:
                if s1.segment_est_egal(s1._PointA, s2._PointA) and s1.segment_est_egal(s1._PointB, s2._PointB):
                    return s1
                if s1.segment_est_egal(s1._PointA, s2._PointB) and s1.segment_est_egal(s1._PointB, s2._PointA):
                    return s1
        return None