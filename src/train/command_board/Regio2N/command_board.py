# Librairies par défaut
import sys
import os
import time


# Librairie de commande pupitre
import pyfirmata.pyfirmata as pyfirmata


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
from src.train.command_board.control import Actions, Control


class CommandBoard(Control):
    pass # TODO : me remplacer par le code
    # Surcharger les fonctions : initialise_physical_buttons(self) ; get_buttons_state(self) ; read_specific_values(self)


def main():
    # Lance un fichier de registre
    log.initialise(PROJECT_DIR + "log", "1.1.0", log.Level.DEBUG)
    log.info("Lancement des essais du pupitre léger")

    # TODO : initialiser une instance de la base de donnée train et appeler son constructeur afin de tester le pupitre avec différents matériels roulants

    # TODO : appeler la fonction d'initialisation du pupitre

    # TODO : lancer le pupitre

