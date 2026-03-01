import pytest  
from phase1.point import Point
from phase1.segment import Segment

#Méthode AAA -> structure en  Arrange, Act, Assert
#Méthode should_return_correct_when...() : test autodescriptif

def test_should_return_correct_when_segment_is_valid():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    segment = Segment(p1, p2)

    #act
    pointA = segment._PointA
    pointB = segment._PointB

    #assert
    assert pointA == p1
    assert pointB == p2


def test_should_return_correct_distance():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    segment = Segment(p1, p2)
    
    #act
    distance = segment.return_distance(p1, p2)
    
    #assert
    assert distance == 5.0

def test_should_return_correct_when_distance_is_zero():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(0, 0)
    segment = Segment(p1, p2)

    #act
    distance = segment.return_distance(p1, p2)

    #assert
    assert distance == 0.0

def test_should_return_correct_when_distance_is_float():
    #arrange
    p1 = Point(1.5, 2.5)
    p2 = Point(4.5, 6.5)
    segment = Segment(p1, p2)

    #act
    distance = segment.return_distance(p1, p2)

    #assert
    assert distance == 5.0 

def test_should_return_correct_when_distance_is_negative():
    #arrange
    p1 = Point(-1, -1)
    p2 = Point(-4, -5)
    segment = Segment(p1, p2)

    #act
    distance = segment.return_distance(p1, p2)

    #assert
    assert distance == 5.0

def test_definir_mediatrice_should_return_correct_midpoint():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(4, 4)
    segment = Segment(p1, p2)

    #act
    milieu_x, milieu_y = segment.definir_mediatrice(p1, p2)

    #assert
    assert milieu_x == 2.0
    assert milieu_y == 2.0

def test_definir_mediatrice_should_return_correct_with_negative_coordinates():
    #arrange
    p1 = Point(-2, -2)
    p2 = Point(2, 2)
    segment = Segment(p1, p2)

    #act
    milieu_x, milieu_y = segment.definir_mediatrice(p1, p2)

    #assert
    assert milieu_x == 0.0
    assert milieu_y == 0.0

def test_should_return_correct_pente_perpendiculaire_when_diagonal_positive():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(4, 4)  
    segment = Segment(p1, p2)
    
    #act
    pente_perpendiculaire = segment.calculer_pente_perpendiculaire(p1, p2)
    
    #assert
    assert pente_perpendiculaire == -1.0

def test_should_return_correct_pente_perpendiculaire_when_diagonal_negative():
    #arrange
    p1 = Point(0, 0)
    p2 = Point(-4, -4)  
    segment = Segment(p1, p2)
    
    #act
    pente_perpendiculaire = segment.calculer_pente_perpendiculaire(p1, p2)
    
    #assert
    assert pente_perpendiculaire == -1.0

def test_should_return_correct_pente_perpendiculaire_when_dy_is_zero():
    #arrange
    p1 = Point(0, 5)
    p2 = Point(10, 5)  # Ligne horizontale
    segment = Segment(p1, p2)
    
    #act
    pente_perpendiculaire = segment.calculer_pente_perpendiculaire(p1, p2)
    
    #assert
    assert pente_perpendiculaire is None




def test_should_return_correct_when_points_equal():
    #arrange
    p1 = Point(3, 4)
    p2 = Point(3, 4)
    segment = Segment(p1, p2)
    
    #act
    result = segment.segment_est_egal(p1, p2)
    
    #assert
    assert result is True


def test_should_return_correct_when_x_different():
    #arrange
    p1 = Point(3, 4)
    p2 = Point(5, 4)
    segment = Segment(p1, p2)
    
    #act
    result = segment.segment_est_egal(p1, p2)
    
    #assert
    assert result is False


def test_should_return_correct_when_y_different():
   
    #arrange
    p1 = Point(3, 4)
    p2 = Point(3, 7)
    segment = Segment(p1, p2)
    
    #act
    result = segment.segment_est_egal(p1, p2)
    
    #assert
    assert result is False


def test_segment_est_egal_should_return_true_with_zero():

    #arrange
    p1 = Point(0, 0)
    p2 = Point(0, 0)
    segment = Segment(p1, p2)
    
    #act
    result = segment.segment_est_egal(p1, p2)
    
    #assert
    assert result is True


def test_should_return_correct_with_same_points():
    #arrange
    p1 = Point(3, 4)
    p2 = Point(5, 6)
    segment1 = Segment(p1, p2)
    segment2 = Segment(p1, p2)
    
    #act
    result = segment1.est_meme_segment(segment2)
    
    #assert
    assert result is True

def test_should_return_correct_with_different_points():
    #arrange
    p1 = Point(3, 4)
    p2 = Point(5, 6)
    p3 = Point(7, 8)
    segment1 = Segment(p1, p2)
    segment2 = Segment(p1, p3)
    
    #act
    result = segment1.est_meme_segment(segment2)
    
    #assert
    assert result is False








