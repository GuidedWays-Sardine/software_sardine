# Librairies par défaut
import sys
import os
import time
import threading


# Librairie de commande pupitre
import pyfirmata.pyfirmata as pyfirmata


# Librairies graphiques
from PyQt5.QtWidgets import QApplication


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd
from src.train.command_board.control import Actions, Control


class CommandBoard(Control):
    pass # TODO : me remplacer par le code
    # Surcharger les fonctions : initialise_physical_buttons(self) ; get_buttons_state(self) ; read_specific_values(self)


def main():
    # Lance un fichier de registre
    log.initialise(log_level=log.Level.DEBUG, save=False)
    log.info(f"Lancement des essais du pupitre léger.\n")

    # Crée une instance d'une application  et d'une base de données
    application = QApplication(sys.argv)
    traindatabase = None        # TODO : remplacer par la vrai base de données

    # Génère une instance du pupitre et la lance
    settings = sd.SettingsDictionary()
    settings.open(f"{PROJECT_DIR}\\src\\train\\command_board\\Regio2N\\Regio2N.board")
    command_board = CommandBoard(settings, application)
    command_board.run()

    update_thread = threading.Thread(target=update, args=(command_board, traindatabase))
    update_thread.start()
    update_thread.join()
    exit(0)


def update(command_board, train_database):
    i = 0
    DELAY = 0.25
    while i < 100:
        command_board.update(train_database)
        time.sleep(DELAY)

if __name__ == "__main__":
    main()
