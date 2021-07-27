import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

class InitialisationWindow:
    """Classe contenant tous les éléments pour la fenêtre d'initialisation simulateur"""

    # Eléments utiles à la fenêtre et les QWidgets contenus sur celle-ci
    app = None
    engine = None
    win = None

    def __init__(self):
        """initialise toutes les fenêtre du programme d'initialisation du simulateur sardine"""
        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)
        self.engine = QQmlApplicationEngine()
        self.engine.load('initialisation/initialisation_window.qml')

        # Lance l'application
        self.win = self.engine.rootObjects()[0]
        self.win.show()
        self.app.exec()
