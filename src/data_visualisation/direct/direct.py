# Ici à toi de voir la structure que tu fais. Tu peux tout décomposer et suivre une structure init, run et update.
# Fait attention de bien vérouiller les cadenas des classes quand tu accèdes à des données (sous faute d'erreur, mais à voir quand cette base de donnée existera)
# N'hésites pas à renomer le fichier si tu trouves un meilleur nom
#N'oublie pas que ce module peut être activé mais pas le module save


# Librairies par défaut
import os.path
import sys
import traceback
import time

# Librairies graphiques
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
from src.initialisation.signals import right_buttons as rb
from src.initialisation.signals import bottom_buttons as bb


class DashboardWindow:
    """Classe contenant tous les éléments pour la fenêtre d'initialisation simulateur"""
    # Eléments utiles à la fenêtre et les QWidgets contenus sur celle-ci
    app = None
    engine = None
    win = None
    bottom_buttons = None
    right_buttons = None

    def __init__(self):
        """initialise toutes les fenêtre du programme d'initialisation du simulateur sardine

        Raises
        ------
        FileNotFoundError
            Soulevé quand le fichier .qml de la fenêtre du dashboard n'est pas trouvée
        SyntaxError
            Soulevé quand le fichier .qml de la fenêtre du dashboard a une erreur de syntaxe et n'est pas lisible
        """
        initial_time = time.time()
        log.change_log_prefix("Dashboard")
        log.info("Début du chargement du dashboard.\n\n")

        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre du dashboard
        self.app = QApplication(sys.argv)
        #self.app.setQuitOnLastWindowClosed(True)
        self.engine = QQmlApplicationEngine()
        self.engine.load(PROJECT_DIR + "src\\data_visualisation\\direct\\graphics\\dashboard.qml")

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile(PROJECT_DIR + "src\\data_visualisation\\direct\\graphics\\dashboard.qml"):
            raise FileNotFoundError("Le fichier .qml pour la fenêtre de dashboard n\'a pas été trouvé.")
        elif not self.engine.rootObjects() and os.path.isfile(PROJECT_DIR + "src\\data_visualisation\\direct\\graphics\\dashboard.qml"):
            raise SyntaxError("Le fichier .qml pour la fenêtre de dashboard contient des erreurs.")

        # Si le fichier qml a été compris, récupère la fenêtre et initialise les différents boutons et pages
        self.win = self.engine.rootObjects()[0]
        #self.win.aboutToQuit()
        #self.win.visibilityChanged.connect(lambda: self.app.quit()) # FIXME : ferme l'application quand celle-ci est mise en plein écran
        #self.bottom_buttons = bb.BottomButtons(self)
        #self.right_buttons = rb.RightButtons(self)


        # Indique le temps de chargement de l'application
        log.info("Application de dashboard chargée en " +
            str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

        # Montre le dashboard, indique que l'application doit se quitter quand celle-ci est fermée et Lance l'application
        self.win.show()
        #self.win.closed.connect(lambda: self.app.quit())
        self.app.exec()

        # Quand l'application est fermée, cache la fenêtre de dashboard et ses fenêtres annexes
        self.win.hide()


def main():
    log.initialise(PROJECT_DIR + "log", "1.1.0", log.Level.DEBUG)

    #Lance l'application d'initialisation
    application = DashboardWindow()


if __name__ == "__main__":
    main()
