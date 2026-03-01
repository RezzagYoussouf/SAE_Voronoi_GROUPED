import pytest
from src.models import Point


@pytest.fixture
def sample_points():
    return [
        Point(2, 4),
        Point(5.3, 4.5),
        Point(18, 29),
        Point(12.5, 23.7)
    ]