import os.path
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
        """initialise toutes les fenêtre du programme d'initialisation du simulateur sardine

        Raises
        ------
        FileNotFoundError
            Soulevé quand le fichier .qml de la fenêtre d'initialisation n'est pas trouvé
        SyntaxError
            Soulevé quand le fichier .qml de la fenêtre d'initialisation a une erreur de syntaxe et n'est pas lisible
        """
        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)
        self.engine = QQmlApplicationEngine()
        self.engine.load('initialisation/initialisation_window.qml')

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile('initialisation/initialisation_window.qml'):
            raise FileNotFoundError('Le fichier .qml pour la fenêtre d\'initialisation n\'a pas été trouvé')
        elif not self.engine.rootObjects() and os.path.isfile('initialisation/initialisation_window.qml'):
            raise SyntaxError('Le fichier .qml pour la fenêtre d\'initialisation contient des erreurs.')

        # Lance l'application
        self.win = self.engine.rootObjects()[0]
        self.win.show()
        self.app.exec()
