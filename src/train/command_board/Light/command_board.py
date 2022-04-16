# Librairies par défaut
import sys
import os
import time
import threading


# Librairies graphiques
from PyQt5.QtWidgets import QApplication


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.settings_dictionary as sd
from src.train.command_board.Generic.controls.electronics.control import Control


class CommandBoard(Control):
    """instance du pupitre lourd"""
    pass


def main():
    # Lance un fichier de registre
    log.initialise(log_level=log.Level.DEBUG, save=False)
    log.info(f"Lancement des essais du pupitre léger.\n")

    # Crée une instance d'une application  et d'une base de données
    application = QApplication(sys.argv)
    traindatabase = None        # TODO : remplacer par la vrai base de données

    # Génère les paramètres nécessaires aux essais
    settings = sd.SettingsDictionary()
    settings["sardine simulator.virtual buttons.screen_index"] = 1
    settings["sardine simulator.virtual buttons.x"] = 1440
    settings["sardine simulator.virtual buttons.y"] = 0
    settings["sardine simulator.virtual buttons.w"] = 480
    settings["sardine simulator.virtual buttons.h"] = 1080

    command_board_settings = sd.SettingsDictionary()
    command_board_settings.open(f"{PROJECT_DIR}\\src\\train\\command_board\\Light\\Light.board")

    # Génère une instance du pupitre et la lance
    command_board = CommandBoard(traindatabase, settings, command_board_settings, application)
    command_board.run()

    # lance le thread de la mise à jour graphique
    update_thread = threading.Thread(target=update, args=(command_board,))
    update_thread.start()
    update_thread.join()


def update(command_board):
    """Fonction d'essai permettant de mettre à jour les entrées du pupitre"""
    i = 0
    while i < 100:
        # Imprime les entrées lues, met à jour et attends avant de faire la mise à jour suivante
        command_board.update()
        time.sleep(0.25)


if __name__ == "__main__":
    main()
