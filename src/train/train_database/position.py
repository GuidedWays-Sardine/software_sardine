# Librairies par défaut python
from enum import Enum


class Position(Enum):
    """Enum des différents positions possibles (pour savoir la position de la voiture dans le train)"""
    FRONT = "front"
    MIDDLE = "middle"
    BACK = "back"
