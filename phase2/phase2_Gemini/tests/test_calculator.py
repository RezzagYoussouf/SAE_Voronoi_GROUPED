import pytest
from scipy.spatial import Voronoi
from src.core.calculator import VoronoiDiagramCalculator
from src.domain.exceptions import CalculationError
from src.domain.models import Point2D

class TestVoronoiDiagramCalculator:
    
    def test_Should_ReturnVoronoiObject_Given_ValidPoints_When_Computed(self):
        # Arrange
        calculator = VoronoiDiagramCalculator()
        points = [Point2D(0, 0), Point2D(0, 1), Point2D(1, 0), Point2D(1, 1)]
        
        # Act
        result = calculator.compute(points)
        
        # Assert
        assert isinstance(result, Voronoi)
        assert len(result.points) == 4

    def test_Should_RaiseCalculationError_Given_CollinearPoints_When_Computed(self):
        # Arrange
        calculator = VoronoiDiagramCalculator()
        points = [Point2D(1, 1), Point2D(2, 2), Point2D(3, 3)]
        
        # Act & Assert
        with pytest.raises(CalculationError) as context:
            calculator.compute(points)
        assert "mathématique" in str(context.value).lower()