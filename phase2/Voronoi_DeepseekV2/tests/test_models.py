from src.models import Point

def test_Should_CreatePointWithCoordinates_Given_ValidXY_When_Instantiating():
    p = Point(1.5, 2.5)
    assert p.x == 1.5
    assert p.y == 2.5