from point import Point
from triangle import Triangle
from segment import Segment
from itertools import combinations


class Diagramme_Voronoi:
    def __init__(self):
        self.liste_points = []
        self.liste_triangles = []

    def parcourir_donnees(self):
        read_file = open("phase1/data/db.txt", "r")
        for line in read_file:
            line = line.strip()
            if line:  # Ignorer les lignes vides
                separateur = line.split(",")
                x = float(separateur[0])
                y = float(separateur[1])
                point = Point(x, y)
                self.liste_points.append(point)
        read_file.close()
    
    def calculer_delauney(self):
        # Générer toutes les combinaisons possibles de 3 points
        combinaisons = combinations(self.liste_points, 3)
        
        for point_1, point_2, point_3 in combinaisons:

            segment1 = Segment(point_1, point_2)
            segment2 = Segment(point_2, point_3)
            segment3 = Segment(point_1, point_3)
            
            triangle = Triangle(segment1, segment2, segment3)
            
            triangle.calculer_centre_circonscrit()
            triangle.calculer_rayon_circonscrit(point_1)
            
            # Pour eviter d'avoir les meme triangles
            if self.triangle_valide(triangle, point_1, point_2, point_3):
                self.liste_triangles.append(triangle)
    
    def triangle_valide(self, triangle, point_1, point_2, point_3):
        for point in self.liste_points:
            if point != point_1 and point != point_2 and point != point_3:
                if triangle.contient_point(point):
                    return False
        return True