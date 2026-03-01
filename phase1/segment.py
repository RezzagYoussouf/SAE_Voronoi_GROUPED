from math import sqrt
from phase1.point import Point

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
        return Point1._x == Point2._x and Point1._y == Point2._y #a_changer?
    
    def est_meme_segment(self, autre_segment):
        return (self.segment_est_egal(self._PointA, autre_segment._PointA) and self.segment_est_egal(self._PointB, autre_segment._PointB)) or (self.segment_est_egal(self._PointA, autre_segment._PointB) and self.segment_est_egal(self._PointB, autre_segment._PointA))

    def __str__(self):
        return f"Segment entre ({self._PointA._x}, {self._PointA._y}) et ({self._PointB._x}, {self._PointB._y})"

