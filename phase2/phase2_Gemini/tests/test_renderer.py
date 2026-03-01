import os
from tempfile import NamedTemporaryFile
import numpy as np
from scipy.spatial import Voronoi
from src.presentation.renderer import MatplotlibRenderer

class TestMatplotlibRenderer:
    
    def test_Should_CreateSvgFile_Given_VoronoiDiagram_When_Exported(self):
        # Arrange
        renderer = MatplotlibRenderer()
        pts = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        vor_diagram = Voronoi(pts)
        
        temp_file = NamedTemporaryFile(delete=False, suffix=".svg")
        out_path = temp_file.name
        temp_file.close() # Libère le fichier (Windows lock)
        
        try:
            # Act
            renderer.export(vor_diagram, out_path)
            
            # Assert
            assert os.path.exists(out_path)
            assert os.path.getsize(out_path) > 0
            
            with open(out_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "<svg" in content
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)