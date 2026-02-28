from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

class Point:

    def __init__(self, x, y, name=None):
        self._x = x
        self._y = y
        self._name = name
    
    def return_distance (self,autre_point):
         distance = sqrt((autre_point.x - self._x)**2 + (autre_point.y - self._y)**2)
         return distance
    
    def definir_mediatrice(self,autre_point):

        milieu_x = (self._x + autre_point.x) / 2
        milieu_y = (self._y + autre_point.y) / 2

        return milieu_x, milieu_y
    
    def determiner_triangle(self):

        liste_points = [(2,4),(5.3,4.5),(18,29), (12.5,23.7)]
        nbr_de_ = 0
        #A changer pour la complexité 
        for point in liste_points:
            p = Point(point[0], point[1], "Point1")
            print(point)
            #nbr_de_points += point
            #if nbr_de_points == 2 :
                #p.definir_mediatrice(self,p)

            #print(f"Point: ({p.x}, {p.y})")

    ##a = 2(x2 − x1),
    ##b = 2(y2 − y1),
    ##c = x^2 1 + y1^2 − x2^2 − y2^2 .
    
    ##def determiner_zone_voronoi(self, )
    def determiner_triangle_while(self):
         i = 0
         liste_points = [(2,4),(5.3,4.5),(18,29), (12.5,23.7)]
         point_A = Point(liste_points[i][0], liste_points[i][1]) #PointA
         point_B = Point(liste_points[i+1][0], liste_points[i+1][1]) #PointB
         point_C = Point(liste_points[i+2][0], liste_points[i+2][1]) #PointC
         point_D = Point(liste_points[i+3][0], liste_points[i+3][1]) #PointD
         x_mediatrice_AB, y_mediatrice_AB = point_A.definir_mediatrice(point_B)
         mediatrice_AB = Point(x_mediatrice_AB,y_mediatrice_AB)
         x_mediatrice_BC, y_mediatrice_BC = point_B.definir_mediatrice(point_C)
         mediatrice_BC = Point(x_mediatrice_BC,y_mediatrice_BC)
         x_mediatrice_AC, y_mediatrice_AC = point_A.definir_mediatrice(point_C)
         mediatrice_AC = Point(x_mediatrice_AC,y_mediatrice_AC)
         x_mediatrice_AD, y_mediatrice_AD = point_A.definir_mediatrice(point_D)
         mediatrice_AD = Point(x_mediatrice_AD,y_mediatrice_AD)
         x_mediatrice_BD, y_mediatrice_BD = point_B.definir_mediatrice(point_D)
         mediatrice_BD = Point(x_mediatrice_BD,y_mediatrice_BD)
         x_mediatrice_DC, y_mediatrice_DC = point_D.definir_mediatrice(point_C)
         mediatrice_DC = Point(x_mediatrice_DC,y_mediatrice_DC)
    
        
         pente_perpendiculaire_AC = point_A.calculer_pente_perpendiculaire(point_C)
         pente_perpendiculaire_AB = point_A.calculer_pente_perpendiculaire(point_B)
         print(f"pente perpendiculaire AB = {pente_perpendiculaire_AB}")
         pente_perpendiculaire_BC = point_B.calculer_pente_perpendiculaire(point_C)
         pente_perpendiculaire_AD = point_A.calculer_pente_perpendiculaire(point_D)
         pente_perpendiculaire_BD = point_B.calculer_pente_perpendiculaire(point_D)
         pente_perpendiculaire_DC = point_D.calculer_pente_perpendiculaire(point_C)

         resultats = {}
         resultats["point_A"] = point_A
         resultats["point_B"] = point_B
         resultats["point_C"] = point_C
         resultats["point_D"] = point_D
         resultats["mediatrice_AB"] = mediatrice_AB
         resultats["mediatrice_BC"] = mediatrice_BC
         resultats["mediatrice_AC"] = mediatrice_AC
         resultats["mediatrice_AD"] = mediatrice_AD
         resultats["mediatrice_BD"] = mediatrice_BD
         resultats["mediatrice_DC"] = mediatrice_DC
         resultats["pente_perpendiculaire_DC"] = pente_perpendiculaire_DC
         resultats["pente_perpendiculaire_AC"] = pente_perpendiculaire_AC
         resultats["pente_perpendiculaire_AB"] = pente_perpendiculaire_AB
         resultats["pente_perpendiculaire_BC"] = pente_perpendiculaire_BC
         resultats["pente_perpendiculaire_AD"] = pente_perpendiculaire_AD
         resultats["pente_perpendiculaire_BD"] = pente_perpendiculaire_BD


         print(f" Les coordonnées de la médiatrice_AB sont {mediatrice_AB.x, mediatrice_AB.y} , et celle de la mediatrice_BC sont {mediatrice_BC.x,mediatrice_BC.y}")
         print(f"Coordonnées du point A = {point_A.x, point_A.y}")
         print(f"Coordonnées du point B = {point_B.x, point_B.y}")
         print(f"Coordonnées du point C = {point_C.x, point_C.y}")
         print(f"coordonnées mediatrice A_C = {mediatrice_AC.x, mediatrice_AC.y}")
         print(f"coordonnées mediatrice D_C = {mediatrice_DC.x, mediatrice_DC.y}")
        

         return resultats
         
         

              
    def creer_point(self, x, y, name=None):
        return Point(x, y, name)
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @y.setter
    def y(self, value):
        self._y = value
    def calculer_coefficients_mediatrice(self,autre_point):
        a = 2 * (autre_point.x - self._x)
        b = 2 * (autre_point.y - self._y)
        c = self._x**2 + self._y**2 - autre_point.x**2 - autre_point.y**2
        return a, b, c
    
    def calculer_pente_perpendiculaire(self, autre_point):
        dx = autre_point.x - self._x
        dy = autre_point.y - self._y
        if dy == 0:
            return None  
        pente_perpendiculaire = -dx / dy  # = -1/pente
        return pente_perpendiculaire
    
    def __str__(self):
        return f"Point({self._x}, {self._y})"
    def dessiner():
        fig = plt.figure()
        plt.show()


if __name__ == "__main__":
        point1 = Point(0, 0, "Point1")
        point1.determiner_triangle_while()


