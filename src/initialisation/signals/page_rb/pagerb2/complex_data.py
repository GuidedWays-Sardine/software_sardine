# Librairies par défaut
import os
import sys
import time
from enum import Enum
from typing import Union


#Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd


class Position(Enum):
    """Enum permettant de savoir si la voiture est une voiture avant ou arrière (utile pour savoir l'image à charger"""
    FRONT = "front"
    MIDDLE = "middle"
    BACK = "back"


class MissionType(Enum):
    """Enum permettant de connaitre le type de mission (pour la génération"""
    PASSENGER = "passenger"
    FREIGHT = "freight"


