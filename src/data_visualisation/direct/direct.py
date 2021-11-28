# TODO : amélioration logging
# TODO : gestion d'erreurs
# TODO : supporter les axes multiples en asbsicce et revoir la structure de données « plots »

# Librairies par défaut
import sys
import time
import os

# Librairies graphiques
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

from matplotlib.backends.qt_compat \
    import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log

VERSION = "1.0.0"
INITIAL_LOGGING = log.Level.DEBUG


#class DashboardWindow(QtWidgets.QMainWindow):
class DashboardWindow(QMainWindow):
    layout = ""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard graphiques en direct")

        """ 
        Initialisation du log
        """
        initial_time = time.time()
        log.change_log_prefix("Dashboard")
        log.info("Début du chargement du dashboard.\n\n")

        """ 
        Création de la fenêtre
        """
        # Créé le widget parent (la fenêtre)
        self.window = QWidget()

        # Layout contenant la fenêtre principale
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Layout contenant les graphiques
        self.graph_main_layout = QStackedLayout()


        # Initialise le sélecteur de graphe
        self.graph_type_selector = QListWidget()
        graph_type_list = ["ERTMS", "Vitesse et dérivées", "Profil ligne"]
        for i in range(len(graph_type_list)):
            item = QListWidgetItem(graph_type_list[i])
            item.setTextAlignment(Qt.AlignCenter)
            self.graph_type_selector.addItem(item)

        # Écoute le signale du sélecteur pour changer de graphique
        self.graph_type_selector.itemSelectionChanged.connect(self.change_graph_type_display)


        # Ajoute le sélecteur de graphique sur la fenêtre principale
        self.main_layout.addWidget(self.graph_type_selector, 1)


        # main_layout => graph_main_layout => Widget(graph_layout)


        # Rempli le tableau des layout des types de graphiques.
        # Chaque type de graphique (ERTMS, vitesse, ...) a son propre layout
        # et nous les stockons dans un tableau de layout qui lui même sera ajouté
        # à un layout principal des graphiques
        self.graph_layout = []
        # Position en x (ligne) du graphique dans la grille
        self.grid_i_layout = []
        # Position en y (colonne) du graphique dans la grille
        self.grid_j_layout = []
        # Widget container permettant de stocker le layout de type grille
        # (le layout parent QStackedLayout n'accepte que des widgets)
        self.graph_container_of_layout = []


        for i in range(len(graph_type_list)):
            self.graph_container_of_layout.append(QtWidgets.QWidget())

            # Place le container dans le layout grille
            grid_layout_to_add = QGridLayout(self.graph_container_of_layout[i])

            # Ajoute la layout grille à la
            self.graph_layout.append(grid_layout_to_add)
            # Initialise la position (i, j) du premier graphique dans le layout
            self.grid_i_layout.append(0)
            self.grid_j_layout.append(0)


        # Ajoute les layout des types de graphique au layout principal des graphiques
        for i in range(len(self.graph_layout)):
            self.graph_main_layout.addWidget(self.graph_container_of_layout[i])


        # Ajoute les graphiques sur la fenêtre principale
        self.main_layout.addLayout(self.graph_main_layout, 10)

        # Défini le layout principal
        self.window.setLayout(self.main_layout)
        # Indique que le widget principal (la fenêtre) est self.window
        self.setCentralWidget(self.window)


        """ 
        Initialisation des graphiques
        """
        # GRAPHIQUE 1 ERTMS
        # Initialisation des plots du graphique
        ertms_graph_1_data = np.array([[1, 190, 175, 160, 160],
                                     [2, 190, 175, 160, 160],
                                     [3, 190, 175, 160, 140],
                                     [4, 190, 175, 140, 120],
                                     [5, 190, 155, 120, 120],
                                     [6, 190, 135, 120, 120],
                                     [7, 190, 135, 120, 105],
                                     [8, 190, 135, 105, 90],
                                     [9, 190, 90, 85, 75],
                                     [10, 190, 80, 65, 75]])

        # Indique si les courbes doivent être remplies
        ertms_graph_1_is_filled = [True, True, True, True]

        # Couleur de remplissage des courbes
        ertms_graph_1_fill_color = ["#C00000", "#EA9100", "#DFDF00", "#969696"]

        # Initialisation du graphique
        ertms_graph_1 = Graph(self, "ertms", True, "ERTMS - Relevé 1", "Distance (km)", "Vitesse (km/h)", ertms_graph_1_data,
                            False, 250, True, ertms_graph_1_is_filled, ertms_graph_1_fill_color)

        # Test d'ajout de données
        # Déclaration des valeurs à ajouter
        ertms_graph_1_plot_to_add = np.array([[11, 190, 175, 160, 160],
                                             [12, 190, 175, 160, 160],
                                             [13, 190, 175, 160, 140],
                                             [14, 190, 175, 140, 120]])

        # Ajout des valeurs au graphique
        ertms_graph_1.add_values(ertms_graph_1_plot_to_add, False, True)


        # GRAPHIQUE 2 ERTMS
        # Initialisation des plots du graphique
        ertms_graph_2_data = np.array([[1, 190, 175, 160, 160],
                                       [2, 190, 175, 160, 160],
                                       [3, 190, 175, 160, 140],
                                       [4, 190, 175, 140, 120],
                                       [5, 190, 155, 120, 120]])

        # Indique si les courbes doivent être remplies
        ertms_graph_2_is_filled = [True, True, True, True]

        # Couleur de remplissage des courbes
        ertms_graph_2_fill_color = ["#C00000", "#EA9100", "#DFDF00", "#969696"]

        # Initialisation du graphique
        ertms_graph_2 = Graph(self, "ertms", True, "ERTMS - Relevé 2", "Distance (km)", "Vitesse (km/h)",
                              ertms_graph_2_data,
                              False, 250, True, ertms_graph_2_is_filled, ertms_graph_2_fill_color)


        # GRAPHIQUE 1 VITESSE ET ACCELERATION
        vit_et_acc_graph_1_data = np.array([[1, 190],
                                            [2, 191],
                                            [3, 192],
                                            [4, 193],
                                            [5, 193],
                                            [6, 192.5],
                                            [7, 193],
                                            [8, 194],
                                            [9, 195],
                                            [10, 195.2]])

        # Indique si les courbes doivent être remplies
        vit_et_acc_graph_1_is_filled = [False]

        # Couleur de remplissage des courbes
        vit_et_acc_graph_1_fill_color = [""]


        vit_et_acc_graph_1 = Graph(self, "vitesse_et_derive", True, "Vitesse", "Temps (s)", "Vitesse (km/h)", vit_et_acc_graph_1_data,
                            False, 250, True, vit_et_acc_graph_1_is_filled, vit_et_acc_graph_1_fill_color)

        # GRAPHIQUE 2 VITESSE ET ACCELERATION : accélération
        vit_et_acc_graph_2_data = np.array([[1, 0],
                                            [2, 0.01],
                                            [3, 0.01],
                                            [4, 0.01],
                                            [5, 0.01],
                                            [6, 0.005],
                                            [7, 0.01],
                                            [8, 0.01],
                                            [9, 0.01],
                                            [10, 0.003]])

        # Indique si les courbes doivent être remplies
        vit_et_acc_graph_2_is_filled = [False]

        # Couleur de remplissage des courbes
        vit_et_acc_graph_2_fill_color = [""]

        vit_et_acc_graph_2 = Graph(self, "vitesse_et_derive", True, "Accélération longitudinale", "Temps (s)", "Accélération (m/s²)",
                                   vit_et_acc_graph_2_data,
                                   False, 250, True, vit_et_acc_graph_2_is_filled, vit_et_acc_graph_2_fill_color)

        # GRAPHIQUE 3 VITESSE ET ACCELERATION : jerk
        vit_et_acc_graph_3_data = np.array([[1, 0],
                                            [2, 0.001],
                                            [3, 0.001],
                                            [4, 0.001],
                                            [5, 0.001],
                                            [6, 0.0005],
                                            [7, 0.001],
                                            [8, 0.001],
                                            [9, 0.001],
                                            [10, 0.0003]])

        # Indique si les courbes doivent être remplies
        vit_et_acc_graph_3_is_filled = [False]

        # Couleur de remplissage des courbes
        vit_et_acc_graph_3_fill_color = [""]

        vit_et_acc_graph_2 = Graph(self, "vitesse_et_derive", True, "Jerk norme euclidienne", "Temps (s)", "Jerk (m/s³)",
                                   vit_et_acc_graph_3_data,
                                   False, 250, True, vit_et_acc_graph_3_is_filled, vit_et_acc_graph_3_fill_color)







        """
        Log d'application
        """
        # Indique le temps de chargement de l'application
        log.info("Dashboard chargé en " +
                 str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n")


    def add_widget(self, widget_to_add, graph_type):
        """ Ajoute un widget dans le layout
        Parameters
        ----------
        widget_to_add -- widget Qt à ajouter au layout
        """
        # Récupère le type de graphique permettant de placer le graphique dans le bon layout de type grille
        if graph_type == "ertms":
            id_graph_layout = 0

        if graph_type == "vitesse_et_derive":
            id_graph_layout = 1

        # Récupère le nnombre actuel de graphique dans la layout de graphique
        # permettant de savoir si un passage à la ligne pour l'affichage du
        # nouveau graphique est nécessaire ou non
        number_of_graph_in_layout = self.graph_layout[id_graph_layout].count()

        # Si le nombre de graphique est pair, alors on place le nouveau graphique à la ligne suivante
        if number_of_graph_in_layout % 2 == 0 and number_of_graph_in_layout != 0:
            self.grid_i_layout[id_graph_layout] += 1
            self.grid_j_layout[id_graph_layout] = 0

        # S'il n'y a qu'un seul graphique sur la ligne, on met notre graphique à la suite
        if number_of_graph_in_layout % 2 == 1:
            self.grid_j_layout[id_graph_layout] += 1

        # Ajoute le graphique à la case (i, j) définie du layout
        self.graph_layout[id_graph_layout].addWidget(widget_to_add, self.grid_i_layout[id_graph_layout], self.grid_j_layout[id_graph_layout])


    def add_navigation_toolbar(self, concerned_widget):
        """ Ajoute une barre d'outil pour les graphiques
        Parameters
        ----------
        concerned_widget -- graphique auquel rattacher la barre d'outil
        """
        self.addToolBar(NavigationToolbar(concerned_widget, self))


    def change_graph_type_display(self):
        """ Modifie le layout de premier plan changeant ainsi le type de graphique
        """
        # print("Current list item :", self.graph_type_selector.currentRow())
        self.graph_main_layout.setCurrentIndex(self.graph_type_selector.currentRow())



class Graph(DashboardWindow):
    # Paramètres du graphique
    # Titre du graphique
    title = ""

    # Label des axes
    x_label = ""
    y_label = ""

    # Informe de quel type est le graphique (armement, effort-vitesse, ...)
    graph_type = ""

    # Indique si le graphique est purement dynamique (s'actualise de lui-même : exemple une  fonction cos(t)
    # dont la courbe est connue) ou alors nécessite des entrées de valeur pour être actualisé (par exemple un graphique
    # de type nuage de point)
    is_dynamic = False
    # Taux de rafraichissement en ms du graphique si celui-ci est dynamique (si is_dynamic est vrai)
    refresh_rate = 250

    # Données d'initalisation des graphiques.
    # L'ensemble des points est stockée dans une matrice de dimennsion m*n où :
    #   - m représente le nombre de point d'abscisse sur le graphique ;
    #   - n représente le nombre de courbes sur le graphique.
    #
    # D'où un point y(m,n) pour m et n défini représente une ordonnée pour un
    # point d'abscisse à x(m) sur le graphique n.
    #
    #      ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # ┏━━━━┩       Numéro de courbe      ┃
    # ┃ x  │  1  │  2  │  3  │ ... │  n  ┃
    # ┃════╪═════╪═════╪═════╪═════╪═════┃ \
    # ┃ x0 │ y00 │ y01 │ y02 │ ... │ y0n ┃  \
    # ┠────┼─────┼─────┼─────┼─────┼─────┨   \
    # ┃ x1 │ y10 │ y11 │ y12 │ ... │ y1n ┃    \
    # ┠────┼─────┼─────┼─────┼─────┼─────┨     ᐳ Matrice telle qu'elle est implémentée
    # ┃ ┆  │  ┆  │  ┆  │  ┆  │ ... │  ┆  ┃    /
    # ┠────┼─────┼─────┼─────┼─────┼─────┨   /
    # ┃ xm │ ym0 │ ym1 │ ym2 │ ... │ ymn ┃  /
    # ┗━━━━┷━━━━━┷━━━━━┷━━━━━┷━━━━━┷━━━━━┛ /
    #   ˅
    #   Point d'abscisse (cette donnée figure également dans la matrice)
    plots = []

    # Dimensions de la figure
    length = 2
    height = 5

    # Stocke si une courbe est remplie et de quelle couleur
    is_filled = []  # Bool
    fill_color = []  # String

    def __init__(self, window, graph_type, is_visible, graph_title, x_label, y_label, plots,
                 is_dynamic, refresh_rate, has_toolbar, is_filled, fill_color):

        self.window = window
        self.graph_title = graph_title
        self.x_label = x_label
        self.y_label = y_label
        self.graph_type = graph_type
        self.is_dynamic = is_dynamic        # TODO : à implémenter
        self.refresh_rate = refresh_rate    # TODO : à implémenter
        self.has_toolbar = has_toolbar
        self.plots = plots
        self.is_filled = is_filled
        self.fill_color = fill_color

        # Créé le widget self.graph qui est la zone où la figure est tracée
        self.graph = FigureCanvas(Figure(figsize=(self.length, self.height)))

        # Initialise et affiche le graphique si seulement celui-ci est visible
        if is_visible:
            self.window.add_widget(self.graph, self.graph_type)

            # Créé la figure et l'ensemble des tracés graphiques
            self.data_graph_ax = self.graph.figure.subplots()  # Récupère le système d'axe existant sur self.graph

            # Renomme les axes
            self.data_graph_ax.set_xlabel(self.x_label)
            self.data_graph_ax.set_ylabel(self.y_label)
            self.data_graph_ax.set_title(self.graph_title)

            # Ajoute une barre d'outil
            if self.has_toolbar:
                self.window.addToolBar(NavigationToolbar(self.graph, self.window))

            # Affiche le graphique
            self.update_and_draw_graph()


    def get_points(self, plots):
        """ Récupère les points de la matrice de points sous format [[x_graphique_1], [[x_graphique_2],
        ..., [[x_graphique_n]] et [[y_graphique_1], [[y_graphique_2], ..., [[y_graphique_n]]

        Parameters
        ----------
        plots : 'numpy.array'
            Matrice de points à afficher

        Returns
        -------
        x_points_all_curves, y_points_all_curves : '(numpy.array, numpy.array)'
            Vecteurs de points
        """
        # Stocke les données de chaque courbe temporairement
        x_points_one_curve = []
        y_points_one_curve = []

        # Stocke l'ensemble des courbes dans des vecteurs de données x et y
        x_points_all_curves = []
        y_points_all_curves = []

        # Récupère la dimension de la matrice de points
        number_of_rows, number_of_columns = plots.shape

        # Récupère les données de la matrice plots et les stocke dans des vecteurs x_points_all_curves et y_points_all_curves
        for i in range(number_of_columns):  # De "gauche à droite" sur la matrice
            for j in range(number_of_rows):  # De "haut en bas" sur la matrice
                # Si on explore la première colonne, on récupère les points d'abscisse
                if i == 0:
                    x_points_one_curve.append(self.plots[j, 0])

                    # Une fois que la première colonne a été parcourue, on pousse le vecteur de points pour sauvegarde
                    if j == (number_of_rows -1):
                        x_points_all_curves.append(x_points_one_curve)

                # Si on explore une colonne autre que la première colonne, alors on récupère des points en y
                else:
                    y_points_one_curve.append(self.plots[j, i])
                    # Une fois que la colonne a été parcourue, on pousse le vecteur de points pour sauvegarde
                    if j == (number_of_rows - 1):
                        # Passage d'une copie de y_points_one_curve
                        # https://stackoverflow.com/questions/39606601/python-append-a-list-to-another-list-and-clear-the-first-list
                        y_points_all_curves.append(y_points_one_curve[:])
                        # Vide le vecteur temporaire pour passer à la prochaine courbe
                        y_points_one_curve = []

        return x_points_all_curves, y_points_all_curves


    def add_values(self, data, delete_old_data, refresh):
        """ Ajoute des données dans la matrice de points et permet une actualisation du graphique

        Parameters
        ----------
        data : 'numpy.array'
            Matrice de points

        delete_old_data : 'bool'
            True supprime l'excédent d'anciennes données sur le graphique évitant la surcharge du graphique

        refresh : 'bool'
            True rafraichie actualise directemeent le graphique sur la fenpetre
        """
        # TODO : forcer l'actualisation graphique lors de retrait de données

        # Concatène les deux tableaux par colonne en respectant le format de données
        self.plots = np.concatenate((self.plots, data))

        # L'ajoute de nouvelles données augmente la densité de données à afficher,
        # alors si ce paramètre est vrai, on enlève la quantité de données à afficher
        # correspondant à la quantité de nouvelles données
        if delete_old_data:
            number_of_rows, number_of_columns = data.shape
            print("\ndata: ", data.shape)
            print(data)
            print("\nplots: ", self.plots.shape)
            print(self.plots)

            # TODO: supprimer les données avec un step adaptatif et déplacer dans remove_values
            self.plots = np.delete(self.plots, slice(0, number_of_rows, 1), 0)
            print("\nplots deleted: ", self.plots.shape)
            print(self.plots)

        if refresh:
            self.update_and_draw_graph()


    # TODO : méthode remove_values
    def remove_values(self):
        """ Retire des points de la matrice de données
        """
        print("TODO")


    def update_and_draw_graph(self):
        """ Affiche initialement ou actualise l'aperçu graphique du graphique
        """
        # Récupère les donnéees en x et en y des courbes
        x_data, y_data = self.get_points(self.plots)

        # Replotte individuellement chaque courbe et la re-remplie si demandée
        for i in range(len(y_data)):
            # Si le graphique est rempli, on ne trace pas les lignes de limitation de la courbe
            if self.is_filled[i - 1] == True:
                alpha_lines = 0

            # Si le grapique n'est pas rempli, on trace les lignes de limitation de la courbe
            if self.is_filled[i - 1] == False:
                alpha_lines = 1

            # Tracé du graphique
            self.data_graph_line, = self.data_graph_ax.plot(x_data[0], y_data[i], alpha=alpha_lines)

            # Remplissage du graphique
            if self.is_filled[i - 1] == True:
                self.data_graph_ax.fill_between(x_data[0], y_data[i], color=self.fill_color[i])

        # Retrace le graphique
        self.data_graph_line.figure.canvas.draw()


def main():
    # Lance le fichier de log en mode warning pour récupérer les warnings et erreurs critiques
    log.initialise(PROJECT_DIR + "log\\", VERSION, INITIAL_LOGGING)
    log.info("Lancement du dashboard\n\n\n")

    # Vérifie s'il n'y a pas une instance de QApplication en cours d'execution
    qapp = QApplication.instance()
    if not qapp:
        # On passe sys.argv pour activer le contrôle par ligne de commande
        qapp = QApplication(sys.argv)

    # Défini le style de l'application
    qapp.setStyle('Fusion')

    with open("dashboard.qss", "r") as f:
        _style = f.read()
        qapp.setStyleSheet(_style)

    # TODO : supporter le chargement de fichier QML
    # https://doc.qt.io/qtforpython/tutorials/qmlintegration/qmlintegration.html

    app = DashboardWindow()  # app est un Qwidget
    app.show()  # Affichage la fenêtre
    app.resize(1920, 1080)  # Redimensionne la fenêtre
    app.activateWindow()  # Met le focus sur la fenêtre
    app.raise_()  # Place la fenêtre prioritaire

    qapp.exec_()  # Exécute la fenêtre en boucle jusqu'à sa fermeture

    # try:
    #     sys.exit(qapp.exec_())
    # except SystemExit:
    #     print('Closing Window...')


if __name__ == "__main__":
    main()
