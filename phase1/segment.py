from math import sqrt
from main import Point

class Segment:

    def __init__(self,Point1, Point2):
        self._PointA = Point1
        self._PointB = Point2
    

    def return_distance (self,Point1, Point2):
         distance = sqrt((Point2._x - Point1._x)**2 + (Point2._y - Point1._y)**2)
         return distance

    def definir_mediatrice(self,Point1, Point2):

        milieu_x = (Point1._x + Point2._x) / 2
        milieu_y = (Point1._y + Point2._y) / 2

        return milieu_x, milieu_y

    def calculer_pente_perpendiculaire(self, Point1, Point2):

        dx = Point2._x - Point1._x
        dy = Point2._y - Point1._y

        if dy == 0:
            return None  
        pente_perpendiculaire = -dx / dy  # = -1/pente
        return pente_perpendiculaire    
    
    def segment_est_egal(self, Point1, Point2):
        return Point1._x == Point2._x and Point1._y == Point2._y
        

