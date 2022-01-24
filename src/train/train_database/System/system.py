# Librairies par défaut python
import sys
import os
from enum import Enum


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

import src.train.train_database.System.Traction.traction as traction
import src.train.train_database.System.Freinage.freinage as freinage
import src.train.train_database.System.Coache.coache as coache
import src.train.train_database.System.Electric_system

class Position(Enum):
    """Enum permettant de savoir si la voiture est une voiture avant ou arrière (utile pour savoir l'image à charger"""
    FRONT = "front"
    MIDDLE = "middle"
    BACK = "back"


class MissionType(Enum):
    """Enum permettant de connaitre le type de mission (pour la génération"""
    PASSENGER = "passenger"
    FREIGHT = "freight"

class System:

    traction = traction
    freinage = freinage
    coache = coache

    def __init__(self):
        self.freinage = freinage.Freinage()
        self.traction = traction.Traction()
        self.coache = coache.Coache()

