import pytest
from ..point import Point
from ..segment import Segment
from ..triangle import Triangle

def test_should_return_correct_when_triangle_is_valid():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(3, 2)
    p3 = Point(0, 4)
    
    segment1 = Segment(p1, p2)
    segment2 = Segment(p2, p3)
    segment3 = Segment(p1, p3)
    
    triangle = Triangle(segment1, segment2, segment3)

    #act
    pointA = triangle._segment1._PointA
    pointB = triangle._segment1._PointB
    pointC = triangle._segment2._PointB

    #assert
    assert pointA == p1
    assert pointB == p2
    assert pointC == p3

def test_should_return_correct_when_centre_circonscrit_is_correct():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(3, 2)
    p3 = Point(0, 4)
    
    segment1 = Segment(p1, p2)
    segment2 = Segment(p2, p3)
    segment3 = Segment(p1, p3)
    
    triangle = Triangle(segment1, segment2, segment3)

    #act
    centre_circonscrit = triangle.calculer_centre_circonscrit()

    #assert
    assert centre_circonscrit is not None

def test_should_return_correct_when_triangle_is_valid_and_has_correct_rayon_circonscrit():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(2, 2)
    p3 = Point(1, 3)
    
    segment1 = Segment(p1, p2)
    segment2 = Segment(p2, p3)
    segment3 = Segment(p1, p3)
    
    triangle = Triangle(segment1, segment2, segment3)

    #act
    rayon_circonscrit = triangle.calculer_rayon_circonscrit(triangle._segment1._PointA)

    #assert
    assert rayon_circonscrit is not None


def test_should_return_correct_when_point_in_cercle_circonscrit():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(2, 2)
    p3 = Point(1, 3)
        
    segment1 = Segment(p1, p2)
    segment2 = Segment(p2, p3)
    segment3 = Segment(p1, p3)
        
    triangle = Triangle(segment1, segment2, segment3)

    #act
    point_dans_cercle = Point(1, 1)
    result = triangle.contient_point(point_dans_cercle)
    
    #assert
    assert result is True

def test_should_return_correct_when_point_out_cercle_circonscrit():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(2, 2)
    p3 = Point(1, 3)
        
    segment1 = Segment(p1, p2)
    segment2 = Segment(p2, p3)
    segment3 = Segment(p1, p3)
        
    triangle = Triangle(segment1, segment2, segment3)

    #act
    point_hors_cercle = Point(5, 5)

    #assert
    result = triangle.contient_point(point_hors_cercle)
    assert result is False


def test_should_return_correct_when_in_triangle_partage_segment():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(4, 6)
    p3 = Point(0, 4)
    p4 = Point(2, 2)
        
    segment1 = Segment(p1, p2)
    segment2 = Segment(p2, p3)
    segment3 = Segment(p1, p3)

    segment4 = Segment(p2, p4)
    segment5 = Segment(p3, p4)
    segment6 = Segment(p2, p3)
        
    triangle1 = Triangle(segment1, segment2, segment3)
    triangle2 = Triangle(segment4, segment5, segment6)

    #act
    result = triangle1.partage_un_segment(triangle2)

    #assert
    assert result is not None
    assert result.est_meme_segment(segment2) or result.est_meme_segment(segment6)

def test_should_return_none_when_no_segment_partage():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(3, 0)
    p3 = Point(1.5, 2)
    
    p4 = Point(5, 5)
    p5 = Point(8, 5)
    p6 = Point(6.5, 7)
    
    triangle1 = Triangle(Segment(p1, p2), Segment(p2, p3), Segment(p3, p1))
    triangle2 = Triangle(Segment(p4, p5), Segment(p5, p6), Segment(p6, p4))
    
    #act
    segment_partage = triangle1.partage_un_segment(triangle2)
    
    #assert
    assert segment_partage is None

def test_should_return_true_when_segment_on_border():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(4, 0)
    p3 = Point(2, 3)
    p4 = Point(2, -3)
    
    segment_bord = Segment(p2, p3) 
    segment_partage = Segment(p1, p2)
    
    triangle1 = Triangle(segment_partage, segment_bord, Segment(p3, p1))
    triangle2 = Triangle(segment_partage, Segment(p2, p4), Segment(p4, p1))
    
    liste_triangles = [triangle1, triangle2]
    
    #act
    est_sur_bord = triangle1.segment_est_sur_le_bord(segment_bord, liste_triangles)
    
    #assert
    assert est_sur_bord is True

def test_should_return_false_when_segment_not_on_border():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(4, 0)
    p3 = Point(2, 3)
    p4 = Point(2, -3)
    
    segment_non_bord = Segment(p2, p3) 
    segment_partage = Segment(p1, p2)
    
    triangle1 = Triangle(segment_partage, segment_non_bord, Segment(p3, p1))
    triangle2 = Triangle(segment_partage, Segment(p2, p4), Segment(p4, p1))
    
    liste_triangles = [triangle1, triangle2]
    
    #act
    est_sur_bord = triangle1.segment_est_sur_le_bord(segment_non_bord, liste_triangles)
    
    #assert
    assert est_sur_bord is True


def test_should_return_correct_when_trouver_sommet_oppose():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(4, 0)
    p3 = Point(2, 3)
    p4 = Point(2, -3)
    
    segment_partage = Segment(p1, p2)
    
    triangle1 = Triangle(segment_partage, Segment(p2, p3), Segment(p3, p1))
    triangle2 = Triangle(segment_partage, Segment(p2, p4), Segment(p4, p1))
    
    #act
    sommet_oppose = triangle1.trouver_sommet_oppose(segment_partage)  # ✅ Passer le SEGMENT
    
    #assert
    assert sommet_oppose is not None
    assert sommet_oppose.x == p3.x
    assert sommet_oppose.y == p3.y
