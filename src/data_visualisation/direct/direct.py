# Ici à toi de voir la structure que tu fais. Tu peux tout décomposer et suivre une structure init, run et update.
# Fait attention de bien vérouiller les cadenas des classes quand tu accèdes à des données (sous faute d'erreur, mais à voir quand cette base de donnée existera)
# N'hésites pas à renomer le fichier si tu trouves un meilleur nom
#N'oublie pas que ce module peut être activé mais pas le module save


# Librairies par défaut
import sys
import time
import os

# Librairies graphiques
import numpy as np
from PyQt5.QtWidgets import QApplication
from matplotlib.backends.qt_compat \
import QtCore, QtWidgets

if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log

VERSION = "1.0.0"
INITIAL_LOGGING = log.Level.DEBUG


# class classeHéritée(classeParente):
class DashboardWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # Relation d'héritage

        initial_time = time.time()
        log.change_log_prefix("Dashboard")
        log.info("Début du chargement du dashboard.\n\n")

        # Lance le dashboard et cherche pour le fichier QML avec tous les éléments de la fenêtre du dashboard
        self.app = QApplication(sys.argv)
        # self.engine = QQmlApplicationEngine()
        # self.engine.load(PROJECT_DIR + "src\\data_visualisation\\direct\\graphics\\dashboard.qml")

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        # if not self.engine.rootObjects() and not os.path.isfile(PROJECT_DIR + "src\\data_visualisation\\direct\\graphics\\dashboard.qml"):
        #     raise FileNotFoundError("Le fichier .qml pour la fenêtre de dashboard n\'a pas été trouvé.")
        # elif not self.engine.rootObjects() and os.path.isfile(PROJECT_DIR + "src\\data_visualisation\\direct\\graphics\\dashboard.qml"):
        #     raise SyntaxError("Le fichier .qml pour la fenêtre de dashboard contient des erreurs.")

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)  # layout permettant d'organiser les widgets verticalement

        # Créé le canvas avec barre d'outil pour le premier graphique
        static_canvas = FigureCanvas(Figure(figsize=(5, 2)))
        layout.addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))

        # Créé le canvas avec barre d'outil pour le second graphique
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 2)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        # Créé le canvas avec barre d'outil pour le troisième graphique
        dataset_canvas = FigureCanvas(Figure(figsize=(5, 2)))
        layout.addWidget(dataset_canvas)
        self.addToolBar(NavigationToolbar(dataset_canvas, self))

        # Tracé du premier graphe
        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501) # Vecteur de temps
        self._static_ax.plot(t, np.tan(t), ".")

        # Tracé du second graphe
        self._dynamic_ax = dynamic_canvas.figure.subplots()
        t = np.linspace(0, 10, 101)
        self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._timer = dynamic_canvas.new_timer(250)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()

        # Tracé du troisième graphe
        # Ensemble de données
        distance = np.linspace(0, 1, 10)
        speed_red = np.array([190, 190, 190, 190, 190, 190, 190, 190, 190, 190])
        speed_orange = np.array([175, 175, 175, 175, 155, 135, 135, 135, 90, 80])
        speed_yellow = np.array([160, 160, 160, 140, 120, 120, 120, 105, 85, 65])
        speed_grey = np.array([160, 160, 140, 120, 120, 120, 105, 90, 75, 75])

        # Créé la figure et l'ensemble des tracés graphiques
        self._data_set_ax = dataset_canvas.figure.subplots()

        # Renomme les axes
        self._data_set_ax.set_xlabel("Distance")
        self._data_set_ax.set_ylabel("Speed")

        # Initialise les courbes
        self._data_set_ax.plot(distance, speed_red, color='k')
        self._data_set_ax.plot(distance, speed_orange, color='k')
        self._data_set_ax.plot(distance, speed_grey, color='k')
        self._data_set_ax.plot(distance, speed_yellow, color='k')

        # Remplie la surface sous les courbes d'une couleur
        self._data_set_ax.fill_between(distance, speed_red, color='#C00000')
        self._data_set_ax.fill_between(distance, speed_orange, color='#EA9100')
        self._data_set_ax.fill_between(distance, speed_yellow, color='#DFDF00')
        self._data_set_ax.fill_between(distance, speed_grey, color='#969696')

        # Indique le temps de chargement de l'application
        log.info("Dashboard chargé en " +
            str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n")


    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # Décale la courbe de la sinusoïde
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()


def main():
    # Lance le fichier de log en mode warning pour récupérer les warnings et erreurs critiques
    log.initialise(PROJECT_DIR + "log\\", VERSION, INITIAL_LOGGING)
    log.info("Lancement du dashboard\n\n\n")

    # Vérifie s'il n'y a pas une instance de QApplication en cours d'execution
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = DashboardWindow()
    app.show() # Affichage la fenêtre
    app.resize(1920, 1080) # Redimensionne la fenêtre
    app.activateWindow() # Met le foxus sur le Dashbboard
    app.raise_() # Place le widget prioritaire
    qapp.exec_() # Exécute la fenêtre en boucle jusqu'à sa fermeture


if __name__ == "__main__":
    main()






