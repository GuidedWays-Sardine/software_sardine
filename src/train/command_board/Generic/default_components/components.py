# Librairies par défaut
import sys
import os
from enum import Enum


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

# Librairies pour les boutons (pupitre utilisant des cartes arduino)
import src.train.command_board.Generic.default_components.electronics.led as bl
import src.train.command_board.Generic.default_components.electronics.push_button as bpb
import src.train.command_board.Generic.default_components.electronics.switch_button as bsb
import src.train.command_board.Generic.default_components.electronics.potentiometer as bp

# Librairies pour les composants claviers
# FEATURE : faire des composants et une base pour un pupitre clavier

# Librairies pour les composants manettes
# FEATURE : faire des composants et une base pour un pupitre manette


class Buttons(Enum):
    """Enum contenant la liste de tous les composants pupitres disponibles"""
    # Composants électroniques reliés
    LED = bl.LED
    POTENTIOMETER = bp.Potentiometer
    PUSH_BUTTON = bpb.PushButton
    SWITCH_BUTTON = bsb.SwitchButton

    # Fonction permettant d'appeler l'initialisation d'un composant pupitre à partir de sa clé
    def __call__(self, *args, **kwargs):
        self.value(*args, **kwargs)
