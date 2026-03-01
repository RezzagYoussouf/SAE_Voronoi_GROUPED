from typing import List, Set
from .models import Point, ParsingError, InvalidPointError, DuplicatePointError


def parse_points_file(filename: str) -> List[Point]:
    points: List[Point] = []
    seen: Set[Point] = set()
    line_number = 0

    try:
        with open(filename, 'r') as f:
            for line in f:
                line_number += 1
                line = line.strip()
                if not line:
                    continue

                parts = line.split(',')
                if len(parts) != 2:
                    raise ParsingError(
                        f"Ligne {line_number}: format invalide, deux coordonnées attendues."
                    )

                try:
                    x = float(parts[0].strip())
                    y = float(parts[1].strip())
                except ValueError:
                    raise InvalidPointError(
                        f"Ligne {line_number}: coordonnées non numériques."
                    )

                point = Point(x, y)
                if point in seen:
                    raise DuplicatePointError(f"Ligne {line_number}: point dupliqué {point}.")

                points.append(point)
                seen.add(point)

    except FileNotFoundError:
        raise ParsingError(f"Fichier introuvable: {filename}")

    if not points:
        raise ParsingError("Le fichier ne contient aucun point valide.")

    return points