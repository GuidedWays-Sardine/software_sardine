# Librairies par défaut
import os
import sys
from enum import Enum


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.train.command_board.Generic.actions.electric as electric
import src.train.command_board.Generic.actions.pneumatic as pneumatic
import src.train.command_board.Generic.actions.traction as traction


class Actions(Enum):
    """Enum contenant la liste de toutes les fonctions pupitres (tous types) implémentés"""
    # FEATURE : ajouter toutes les fonctions implémentés avec leur clé ici

    # Fonction permettant d'appeler l'action pupitre à partir de sa clé
    def __call__(self, *args, **kwargs):
        self.value(*args, **kwargs)