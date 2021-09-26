import os.path
import sys
import logging
import traceback
import time

from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine

import log.log as log


class DriverMachineInterface:
    """Classe contenant tous les éléments pour le DMI"""

    # Eléments utiles à la fenêtre et les QWidgets contenus sur celle-ci
    app = None
    engine = None
    win = None

    def __init__(self, data):
        initial_time = time.time()
        log.change_log_prefix("[Initialisation]")
        logging.info("Début du chargement du Driver Machine Interface.\n\n")

        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)
        self.engine = QQmlApplicationEngine()
        self.engine.load("DMI/ETCS/driver_machine_interface.qml")

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile("DMI/ETCS/driver_machine_interface.qml"):
            raise FileNotFoundError("Le fichier .qml pour la fenêtre du DMI n\'a pas été trouvé.")
        elif not self.engine.rootObjects() and os.path.isfile("DMI/ETCS/driver_machine_interface.qml"):
            raise SyntaxError("Le fichier .qml pour la fenêtre du DMI contient des erreurs.")

        # Si le fichier qml a été compris, récupère la fenêtre et initialise les différents boutons et pages
        self.win = self.engine.rootObjects()[0]
        self.win.visibilityChanged.connect(lambda: self.app.quit())

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
                    self.win.setPosition(sg[0], sg[1])
                    self.win.resize(sg[2] - sg[0] + 1, sg[3] - sg[1] + 1)
                else:
                    # Si ce n'est pas en plein écran, récupère les valeurs de l'application d'initialisation
                    # Ces valeurs seront décallés selon la position
                    self.win.setPosition(sg[0] + data[central_dmi_key + "positionX"], sg[1] + data[central_dmi_key + "positionY"])
                    self.win.resize(data[central_dmi_key + "tailleX"], data[central_dmi_key + "tailleY"])

        # Indique le temps de chargement de l'application
        logging.info("Application du DMI chargée en " +
                     str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

        # Lance l'application
        self.win.show()
        self.app.exec()

