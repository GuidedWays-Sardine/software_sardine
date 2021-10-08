import os.path
import sys
import logging
import traceback
import time

from PyQt5.QtWidgets import QDesktopWidget, QMainWindow
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtQml import QQmlApplicationEngine

import log.log as log


class DriverMachineInterface:
    """Classe contenant tous les éléments pour le DMI"""

    # Eléments utiles à la fenêtre et les QWidgets contenus sur celle-ci
    black_screens = None
    engine = None
    dmi_window = None

    pages = {}

    def __init__(self, simulation, data):
        initial_time = time.time()
        log.change_log_prefix("[Initialisation DMI ETCS]")
        logging.info("Début du chargement du Driver Machine Interface.\n\n")

        # Commencer par charger suffisament d'écrans noirs (pour couvrir les écrans si nécessaire   # TODO : bouger ça dans la simulation
        # Todo : ajouter une fonction pour fermer toute les fenêtres si une est fermée.
        try:
            if data["EcransEteints"]:
                self.black_screens = []
                for screen_index in range(0, QDesktopWidget().screenCount()):
                    sg = QDesktopWidget().screenGeometry(screen_index).getCoords()
                    self.black_screens.append(QMainWindow())
                    self.black_screens[screen_index].setWindowFlag(Qt.FramelessWindowHint)
                    self.black_screens[screen_index].setGeometry(sg[0], sg[1], sg[2] - sg[0] + 1, sg[3] - sg[1] + 1)
                    self.black_screens[screen_index].setStyleSheet("QMainWindow {background: 'black';}")
                    self.black_screens[screen_index].hide()
        except KeyError:
            logging.debug("Pas de paramètres EcranEteints.\n")

        # crée un self.engine pour le chargement de la fenêtre du DMI et essaye de charger le DMI
        self.engine = QQmlApplicationEngine()
        self.engine.load("DMI/ETCS/driver_machine_interface.qml")

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile("DMI/ETCS/driver_machine_interface.qml"):
            raise FileNotFoundError("Le fichier .qml pour la fenêtre du DMI ETCS n\'a pas été trouvé.")
        elif not self.engine.rootObjects() and os.path.isfile("DMI/ETCS/driver_machine_interface.qml"):
            raise SyntaxError("Le fichier .qml pour la fenêtre du DMI ETCS contient des erreurs.")

        # Si le fichier qml a été compris, récupère la fenêtre et la cache le temps que tous les modules finissent de charger
        self.dmi_window = self.engine.rootObjects()[0]
        self.dmi_window.hide()
        self.dmi_window.visibilityChanged.connect(lambda: simulation.app.quit())

        # Recherche la liste des fichiers et dossiers présents dans le dossier DMI/ETCS/graphics
        folders = os.listdir("DMI/ETCS/graphics")

        # Pour chaque sections graphiques du DMI ayant un dossier associé (A à G dans DMI/ETCS/graphics)
        for folder in ["A", "B", "C", "D", "E", "F", "G"]:
            # Initialise la liste des éléments graphiques disponibles
            self.pages[folder] = {}

            # Si le dossier existe bien, regarde chaque fichiers présents à l'intérieur de celui-ci
            if folder in folders:
                files = os.listdir("DMI/ETCS/graphics/" + folder)
                for file in (f for f in files if f.endswith(".qml")):   # S'assure que les fichiers son bien en .qml
                    engine = QQmlApplicationEngine()
                    page_path = "DMI/ETCS/graphics/" + folder + file    # Par rapport au main.py
                    engine.load(page_path)                              # permet d'essayer de charger la page

                    # Si la page a été correctement chargée
                    if engine.rootObjects():
                        # Si c'est le premier élément de la section correctement chargé, le rend visible
                        if len(self.pages[folder]) == 0:
                            # Récupère le DMI_stackview (attention objectName en minuscule) et change la page active
                            section = self.dmi_window.findChild(QObject, folder.lower())
                            section.set_active_page(engine.rootObjects()[0])

                        # Dans tous les cas, rajoute la page dans le dictionaire (pour la trouver dans le futur
                        self.pages[folder][file] = engine

                        # TODO : appeler l'initialisation des signaux similairement à celle présente dans right_buttons
                        # Chaque initialisation doit prendre la simulation, la DMI (self) et l'engine de sa page
                        # Ne pas oublier la structure de récupération d'exceptions
                        # si initialisation fonctionnelle, écraser self.page[folder][file]

                    # Dans le cas où la page n'est pas valide laisse un warning
                    logging.debug("La page : " + file + " du dossier" + folder + " contient des erreurs.\n")

                # Vérifie qu'au moins un fichier graphique a été correctement chargé
                if len(self.pages[folder]) == 0:
                    logging.warning("Aucun fichier graphique correctement chargé dans" + folder +
                                    ". La section restera vide.\n")

            # Dans le cas où le fichier n'existe pas
            else:
                logging.warning("Aucun dossier graphique : " + folder + ". La section restera vide.\n")

        # Récupère les données reliées à la taille et la position de l'écran du DMI central
        central_dmi_key = "SARDINE simulator.Central DMI."
        try:
            # Tente de récuper l'index et si celui-ci n'a pas été trouvé, jette une erreur et crash le programme
            screen_index = data[central_dmi_key + "IndexEcran"]
        except KeyError:
            raise KeyError("Pas de valeurs : " + central_dmi_key + "\n\t\tL'écran DMI central n'a pas pu être chargé.\n")
        else:
            # Si l'index de l'écran n'est pas bon, jette une erreur, sinon récupère ses dimensions
            if screen_index == 0 or screen_index > QDesktopWidget().screenCount():
                raise ValueError("Aucun écran sélectionné pour le DMI central, la simulation ne peut pas se lancer.\n")
            else:
                # Récupères les informations de l'écran récupéré et vérifie si l'application est en plein écran ou non
                sg = QDesktopWidget().screenGeometry(screen_index - 1).getCoords()
                if data[central_dmi_key + "PleinEcran"]:
                    # Si c'est en plein écran, récupère les valeurs de l'écran
                    self.dmi_window.setPosition(sg[0], sg[1])
                    self.dmi_window.resize(sg[2] - sg[0] + 1, sg[3] - sg[1] + 1)
                else:
                    # Si ce n'est pas en plein écran, récupère les valeurs de l'application d'initialisation
                    # Ces valeurs seront décallés selon la position
                    self.dmi_window.setPosition(sg[0] + data[central_dmi_key + "positionX"], sg[1] + data[central_dmi_key + "positionY"])
                    self.dmi_window.resize(data[central_dmi_key + "tailleX"], data[central_dmi_key + "tailleY"])

        # Indique le temps de chargement de l'application
        logging.info("Application du DMI chargée en " +
                     str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")


    def run(self):
        # Si les autres écrans doivent êtres éteints, les éteints
        if self.black_screens is not None:
            for screen in self.black_screens:
                screen.show()

        # Montre la fenêtre générale du DMI
        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.dmi_window.show()
