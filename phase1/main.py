from math import sqrt


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
         x_mediatrice_AB, y_mediatrice_AB = point_A.definir_mediatrice(point_B)
         mediatrice_AB = Point(x_mediatrice_AB,y_mediatrice_AB)
         x_mediatrice_BC, y_mediatrice_BC = point_B.definir_mediatrice(point_C)
         mediatrice_BC = Point(x_mediatrice_BC,y_mediatrice_BC)
         x_mediatrice_AC, y_mediatrice_AC = point_A.definir_mediatrice(point_C)
         mediatrice_AC = Point(x_mediatrice_AC,y_mediatrice_AC)


         print(f" Les coordonnées de la médiatrice_AB sont {mediatrice_AB.x, mediatrice_AB.y} , et celle de la mediatrice_BC sont {mediatrice_BC.x,mediatrice_BC.y}")
         print(f"Coordonnées du point A = {point_A.x, point_A.y}")
         print(f"Coordonnées du point B = {point_B.x, point_B.y}")
         print(f"Coordonnées du point C = {point_C.x, point_C.y}")
         print(f"coordonnées mediatrice A_C = {mediatrice_AC.x, mediatrice_AC.y}")
         
         

              
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

if __name__ == "__main__":
        point1 = Point(2, 4, "Point1")
        mediat_x, mediat_y = point1.definir_mediatrice(Point(5.3, 4.5, "Point2"))
        print(f"Mediatrice: ({mediat_x}, {mediat_y})")
        point1.determiner_triangle_while()

    
