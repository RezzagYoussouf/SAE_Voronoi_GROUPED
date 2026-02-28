import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')
from scipy.spatial import Voronoi
from src.renderer import (
    bounding_box,
    voronoi_finite_polygons_2d,
    render_voronoi,
    save_figure,
)
from src.models import Point
from src.calculator import VoronoiCalculator

def test_Should_ReturnCorrectBounds_Given_TwoPoints_When_CallingBoundingBox():
    points = [Point(0, 0), Point(2, 3)]
    xmin, xmax, ymin, ymax = bounding_box(points, margin=0.1)
    assert xmin == pytest.approx(-0.2)
    assert xmax == pytest.approx(2.2)
    assert ymin == pytest.approx(-0.3)
    assert ymax == pytest.approx(3.3)

def test_Should_ReturnDefaultBounds_Given_EmptyList_When_CallingBoundingBox():
    xmin, xmax, ymin, ymax = bounding_box([])
    assert xmin == 0
    assert xmax == 1
    assert ymin == 0
    assert ymax == 1

def test_Should_ReturnFinitePolygons_Given_PointsWithFiniteRegions_When_CallingVoronoiFinitePolygons2D():
    points = np.array([[0, 0], [2, 0], [2, 2], [0, 2], [1, 1]])
    vor = Voronoi(points)
    regions, vertices = voronoi_finite_polygons_2d(vor)
    assert len(regions) == len(points)
    assert len(vertices) > 0

def test_Should_ReturnFinitePolygons_Given_PointsWithoutFiniteRegions_When_CallingVoronoiFinitePolygons2D():
    points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    vor = Voronoi(points)
    regions, vertices = voronoi_finite_polygons_2d(vor)
    assert len(regions) == len(points)
    assert len(vertices) >= 4

def test_Should_ReturnFigure_Given_ValidVoronoiResult_When_RenderingWithLabels():
    points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]
    calc = VoronoiCalculator()
    result = calc.compute(points)
    fig = render_voronoi(result, show_labels=True)
    assert fig is not None
    import matplotlib.pyplot as plt
    plt.close(fig)

def test_Should_CreateFile_Given_FigureAndPath_When_SavingFigure(tmp_path):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    filepath = tmp_path / "test.png"
    save_figure(fig, str(filepath))
    assert filepath.exists()
    plt.close(fig)

def test_Should_UseAutoRadius_Given_RadiusNone_When_CallingVoronoiFinitePolygons2D():
    points = np.array([[0, 0], [2, 0], [2, 2], [0, 2], [1, 1]])
    vor = Voronoi(points)
    regions, vertices = voronoi_finite_polygons_2d(vor, radius=None)
    assert len(regions) == len(points)

def test_Should_HandleRandomPoints_Given_VariousConfigurations_When_CallingVoronoiFinitePolygons2D():
    np.random.seed(42)
    points = np.random.rand(20, 2)
    vor = Voronoi(points)
    regions, vertices = voronoi_finite_polygons_2d(vor)
    assert len(regions) == len(points)
    assert len(vertices) > 0

def test_Should_ReturnFigure_Given_ValidVoronoiResult_When_RenderingWithoutLabels():
    points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]
    calc = VoronoiCalculator()
    result = calc.compute(points)
    fig = render_voronoi(result, show_labels=False)
    assert fig is not None
    import matplotlib.pyplot as plt
    plt.close(fig)