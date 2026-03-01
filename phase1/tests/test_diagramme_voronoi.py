from phase1.diagramme_voronoi import Diagramme_Voronoi
from phase1.point import Point

def test_should_return_true_when_triangle_valid_is_given():
    #Arrange
    diagramme_voronoi = Diagramme_Voronoi()
    diagramme_voronoi.liste_points = [Point(0,0), Point(3,4), Point(5,9)]

    #Act
    diagramme_voronoi.calculer_delauney()

    #Assert
    assert len(diagramme_voronoi.liste_triangles) == 1

def test_should_return_false_when_triangle_is_not_valid():
    #Arrange
    diagramme_voronoi = Diagramme_Voronoi()
    diagramme_voronoi.liste_points = [Point(3,4), Point(3,4), Point(5,9), Point(5,9)]

    #Act
    diagramme_voronoi.calculer_delauney()

    #Assert
    assert len(diagramme_voronoi.liste_triangles) == 0