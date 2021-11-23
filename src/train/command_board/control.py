import os
import sys
import traceback
import threading
import time
from enum import Enum, unique


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.train.command_board.functions as func


@unique
class Actions(Enum):
    """Enum contenant toutes les actions possibles par le pupitre"""
    # FEATURE : ajouter les différentes actions en suivant la structure NOM_ACTION = (func.fonction,) relié à functions.py
    LEVER_PANTHO = (func.lever_panto,)
    MANIP_DE_TRACTION = (func.manip_de_traction,)

    # Fonction permettant de facilement appeler la fonction associée à la valeur de l'Enum
    def __call__(self, *args, **kwargs):
        self.value[0](*args, **kwargs)
