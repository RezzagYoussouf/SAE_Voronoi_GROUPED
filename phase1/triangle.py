from point import Point
from segment import Segment

class Triangle():

    def __init__(self, segment1 : Segment, segment2 : Segment, segment3 : Segment):
        self._segment1 = segment1
        self._segment2 = segment2
        self._segment3 = segment3
        self._cercle_circonscrit = None
        self._rayon_cercle_circonscrit = None
    
    def calculer_centre_circonscrit(self):
        #calcule des médiatrices du triangle
        x_mediatrice_AB, y_mediatrice_AB = self._segment1.definir_mediatrice(self._segment1._PointA, self._segment1._PointB)
        x_mediatrice_BC, y_mediatrice_BC = self._segment2.definir_mediatrice(self._segment2._PointA, self._segment2._PointB)
        x_mediatrice_AC, y_mediatrice_AC = self._segment3.definir_mediatrice(self._segment3._PointA, self._segment3._PointB)

        #calcule des pentes des médiatrices
        pente_perpendiculaire_AB = self._segment1.calculer_pente_perpendiculaire(self._segment1._PointA, self._segment1._PointB)
        pente_perpendiculaire_BC = self._segment2.calculer_pente_perpendiculaire(self._segment2._PointA, self._segment2._PointB)
    
        #trouver l'intersection des médiatrices pour obtenir le centre du cercle circonscrit
        m1 = pente_perpendiculaire_AB
        m2 = pente_perpendiculaire_BC
        x1, y1 = x_mediatrice_AB, y_mediatrice_AB
        x2, y2 = x_mediatrice_BC, y_mediatrice_BC

        if m1 is not None and m2 is not None and m1 != m2:
            x_inter = (m1 * x1 - m2 * x2 + y2 - y1) / (m1 - m2)
            y_inter = m1 * (x_inter - x1) + y1
        elif m1 is None:
            # Médiatrice AB est verticale (x = x1)
            x_inter = x1
            y_inter = m2 * (x_inter - x2) + y2
        elif m2 is None:
            # Médiatrice BC est verticale (x = x2)
            x_inter = x2
            y_inter = m1 * (x_inter - x1) + y1
        else:
            return None  #pas d'inter, droites paralleles, donc pas de croisement, pas de cercle circonscrit
        
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
        for premier_segment in mes_segments:
            for deuxieme_segment in autre_segments:
                if premier_segment.est_meme_segment(deuxieme_segment):
                    return premier_segment
        return None
    
    def segment_est_sur_le_bord(self, segment, liste_triangles):
        for autre_triangle in liste_triangles:
            if autre_triangle != self:
                for s2 in [autre_triangle._segment1, autre_triangle._segment2, autre_triangle._segment3]:
                    if segment.est_meme_segment(s2):
                        return False
        return True

    def trouver_sommet_oppose(self, un_autre):
        coordonnes_segment = [self._segment1._PointA, self._segment1._PointB,
                  self._segment2._PointA, self._segment2._PointB,
                  self._segment3._PointA, self._segment3._PointB]
        
        for un_segment in coordonnes_segment:
            if not (un_autre.segment_est_egal(un_segment, un_autre._PointA) or un_autre.segment_est_egal(un_segment, un_autre._PointB)):
                return un_segment #Retourne le point/sommet du triangle qui n'est pas dans le segment partagé
        return None

    def __str__(self):
        return f"Triangle avec segments : {self._segment1}, {self._segment2}, {self._segment3}"