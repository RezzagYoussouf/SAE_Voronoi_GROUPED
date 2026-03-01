class VoronoiAppError(Exception):
    """Exception de base pour l'application."""
    pass

class ParsingError(VoronoiAppError):
    """Déclenchée lors d'une erreur de parsing du fichier."""
    pass

class CalculationError(VoronoiAppError):
    """Déclenchée lors d'une erreur mathématique du calcul de Voronoï."""
    pass