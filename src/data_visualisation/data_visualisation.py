# Librairies par défaut
import sys
import os
import time


# Librairies graphiques


# librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


class DataVisualisation:
    # stocke toutes tes données à sauvegarder ici, ou dans le sous module save (penser que la sauvegarde ne sera peut-être pas activée)

    def __init__(self, simulation, data):
        time.time()
        log.info("Début de l'initialisation du module de visualisation des données.\n")
        # Initialise à partir des données les visualisations en direct ainsi que les sauvegardes

    def run(self):
        log.info("Lancement du module")
        # Faire une fonction qui rend toutes les fenêtres visible et qui lance les différentes boucles sur des threads différents (mise à jour des courbes en direct et enregistrement des données)

    # normalement pas besoins de fonction update ici, elle sera à mettre dans les fichiers save et direct


def main():
    log.initialise(PROJECT_DIR + 'log\\', "1.1.0", log.Level.DEBUG)

    # Crée une micro simulation (avec juste le DMI)
    from PyQt5.QtWidgets import QApplication

    class A:
        # Il faudra rajouter une instance de la base de donnée train et ligne quand celles-ci existeront
        app = None
        curves = None

    simulation = A()
    simulation.app = QApplication(sys.argv)
    simulation.app.setQuitOnLastWindowClosed(True)

    # Ici la base de données contenant les informations sur les positions et tailles des fenêtres (à définir une fois tes premères données récupérées
    data = {}

    #Initialise, lance et montre le dmi
    simulation.curves = DataVisualisation(simulation, data)
    # N'hésites pas à lancer un thread ici pour faire des changements de valeurs et voir ce que ça change sur les courbes
    simulation.curves.run()
    simulation.app.exec()

if __name__ == "__main__":
    main()
