# Librairies par défaut
from enum import Enum
import logging


class Level(Enum):
    """Classe contenant les différents niveaux de logs (permet une indépendance du module)"""
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
