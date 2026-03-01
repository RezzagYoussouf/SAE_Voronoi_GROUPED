import os
from typing import List, Set
from src.domain.models import Point2D
from src.domain.exceptions import ParsingError

class CsvPointParser:
    """Analyse un fichier texte pour en extraire des points 2D."""
    
    SEPARATOR = ","
    MIN_POINTS = 3

    def parse(self, filepath: str) -> List[Point2D]:
        if not os.path.exists(filepath):
            raise ParsingError(f"Le fichier '{filepath}' est introuvable.")
        
        points_set: Set[Point2D] = set()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line_number, line in enumerate(lines, start=1):
            clean_line = line.strip()
            if not clean_line:
                continue  # Ignorer les lignes vides
            
            parts = clean_line.split(self.SEPARATOR)
            if len(parts) != 2:
                raise ParsingError(f"Ligne {line_number} invalide : format attendu 'x,y'.")
            
            try:
                x = float(parts[0].strip())
                y = float(parts[1].strip())
                points_set.add(Point2D(x=x, y=y))
            except ValueError:
                raise ParsingError(f"Ligne {line_number} invalide : coordonnées non numériques.")

        points = list(points_set)
        
        if len(points) < self.MIN_POINTS:
            raise ParsingError(f"Nombre de points uniques insuffisant (minimum {self.MIN_POINTS} requis).")
            
        return points