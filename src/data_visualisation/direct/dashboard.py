# Librairies par défaut
import functools
import os
import re
import sys
import time
from abc import ABCMeta, abstractmethod

# Librairies SARDINE
import src.misc.log.log as log

# Librairies graphiques
import numpy as np
from PyQt5.QtCore import *
# from PyQt5.QtCore import QThread as QThread
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import QObject as QObject

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

# Paramétrage du log
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))


VERSION = "1.2.0"
INITIAL_LOGGING = log.Level.DEBUG


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__(flags=Qt.Widget)
        # Initiallisation du logging
        initial_time = time.time()
        log.change_log_prefix("Tableau de bord")
        log.info("Début du chargement du tableau de bord.")

        """
        Déclarations
        """
        self.__window = QWidget(flags=Qt.Widget)  # Widget parent (fenêtre principale)

        initial_category_list = ["ERTMS", "Catégorie 2"]
        self.__graph_selector = GraphCategorySelector(initial_category_list)  # Sélecteur de graphique

        self.__layout = Layout(self.__graph_selector)  # Layouts
        self.__graph = []  # Liste de graphique
        self.__graph_widget = []  # Liste des widgets des graphiques
        self.__graph_title = []  # Liste des titres des graphiques
        self.__toolbar_instance = []  # Liste groupant les instances des barre d'outils personnalisées
        self.__toolbar = []  # Liste groupant les objets de type barre d'outils personnalisées
        self.__number_of_graphs = 0  # Compteur du nombre de graphiqes
        self.__toolbar_toogle_act = []  # Liste des actions du menu d'affichage des barres d'outils

        """
        Initialisations
        """
        self.setWindowTitle("Visualisateur des données du simulateur")

        # Défini le layout principal de la fenêtre
        self.__window.setLayout(self.__layout.get_main_layout())

        # Renseigne le widget principal de la fenêtre
        self.setCentralWidget(self.__window)

        # Initialise le sélecteur de graphique
        self.__init_graph_selector()

        # Ajoute les graphiques
        self.__create_graphs()

        # Initialise le menu
        self.__init_menu_bar()

        # Indique le temps de chargement de l'application
        log.info("Tableau de bord chargé en " +
                 str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.")

    def __init_graph_selector(self):
        """Initialise le widget du sélecteur de graphe"""

        # Génération du sélecteur de graphiques
        self.__graph_selector_widget = self.__graph_selector.get_widget()

        # Ajout du widget au layout principal
        self.__layout.add_widget(self.__graph_selector_widget, "graph_selector", self.__layout.get_main_layout())

    def __create_graphs(self):
        """Créé les graphiques avec leurs barres d'outils"""

        self.__init_graph("test_standard_graph", "Premier graphique", "ERTMS")
        self.__init_graph("test_standard_graph", "", "ERTMS")
        self.__init_graph("test_standard_graph", "", "ERTMS")
        self.__init_graph("test_standard_graph", "", "Catégorie 2")

    def __init_graph(self, graph_type=None, title=None, category=None):
        """Initialise un graphique

        Parameters
        ----------
        graph_type : str
            type du graphique

        title : str
            titre du graphique

        category : str
            catégorie du graphique
        """

        if category is None:
            log.error("Catégorie du graphique non spécifiée lors de son initialisation")
            raise AttributeError("Catégorie du graphique non spécifiée lors de son initialisation")

        if graph_type is None:
            log.error("Type du graphique non spécifiée lors de son initialisation")
            raise AttributeError("Type du graphique non spécifiée lors de son initialisation")

        # INITIALISATION DU GRAPHIQUE
        # Instancie un graphique
        if graph_type == "test_standard_graph":
            self.__graph.append(TestStandardGraph(title))

        elif graph_type == "speed":
            self.__graph.append(SpeedGraph(title))

        else:
            log.error("Type de graphique à initialiser non reconu. Type du graphique : ", graph_type)
            raise AttributeError("Type de graphique à initialiser non recoonu")

        # Stocke le titre du graphique
        self.__graph_title.append(self.__graph[self.__number_of_graphs].get_title())

        # Récupère le widget du graphique
        self.__graph_widget.append(self.__graph[self.__number_of_graphs].get_widget())

        # Ajoute le graphique au layout
        self.__layout.add_widget(self.__graph_widget[self.__number_of_graphs], "graph", None, category)

        # Renseigne le sélecteur de graphique d'une possible nouvelle catégorie de graphique
        self.__graph_selector.add_graph(category)

        # INITIALISATION DE LA BARRE D'OUTILS
        # Instancie une barre d'outils
        self.__toolbar_instance.append(
            CustomNavigationToolBar(self, self.__graph_widget[self.__number_of_graphs], self.__window, True,
                                    self.__graph_title[self.__number_of_graphs], None,
                                    self.__graph[self.__number_of_graphs]))

        # Stocke la barre d'outils dans une liste d'instance des barres d'outils
        self.__toolbar.append(self.__toolbar_instance[self.__number_of_graphs].get_toolbar())

        # Ajoute la barre d'outil à la fenêtre
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.__toolbar[self.__number_of_graphs])

        # Incrémente le nombre de graphiques existants
        self.__number_of_graphs += 1

    def __init_menu_bar(self):
        """Initialise les menus"""

        menubar = self.menuBar()

        # -> Menu "Fichiers"
        file_menu = menubar.addMenu('Fichier')

        # --> Sous-menu "Quitter"
        file_menu_exit_act = QAction('&Exit', self)
        file_menu_exit_act.setShortcut('Ctrl+Q')
        file_menu_exit_act.setStatusTip('Exit application')
        file_menu.addAction(file_menu_exit_act)
        file_menu_exit_act.triggered.connect(self.__quit)  # Écoute le signal d'appui

        # -> Menu "Affichage"
        view_menu = menubar.addMenu('Affichage')
        # --> Sous-menu "Barre d'outils"
        view_toolbars_submenu = QMenu("Barres d\'outils", self)
        view_menu.addMenu(view_toolbars_submenu)

        # ---> Sous-menu de catégorie de graphique
        # self.__toolbar_toogle_act[a][b] = c, où :
        #   - a représente l'indice de la la catégorie du graphique
        #   - b représente un graphique se trouvant dans la catégorie d'indice a
        #   - c représente une action toggle d'un graphique appartenant à la catégorie a (type : QAction)
        #
        # Complète la matrice des QAction. Algorithme informel :
        # Pour i allant de 0 au nombre de graphiques :
        #   Pour j allant du graphique 0 au nombre de graphiques dans la catégorie :
        #       Créer une action de toggle de la barre d'outil du graphique
        #       Remplir la matrice à la case (i, j) avec la QAction
        #       Définir le bouton checkable et définir son état initial
        #       Écouter le signal de check du bouton pour faire apparaître/disapraître la barre d'outils du graphique
        self.__toolbar_toogle_act = []
        for i in range(len(self.__graph_selector.get_categories_list())):
            self.__toolbar_toogle_act.append([])

            # Récupère la liste des catégories de graphiques du sélecteur de graphique
            graph_category = self.__graph_selector.get_categories_list()
            # Récupère le nombre de graphiques dans la catégorie graph_category du sélecteur de grahpique
            nb_graph_in_category = self.__graph_selector.get_nb_graph_in_category(graph_category[i])
            # Créé le sous-menu de la catégorie et la rajoute au menu parent
            view_toolbars_category_submenu = QMenu(graph_category[i], self)
            view_toolbars_submenu.addMenu(view_toolbars_category_submenu)

            for j in range(nb_graph_in_category):
                if len(self.__graph_title) < nb_graph_in_category:
                    log.error(
                        "Les titres des graphiques ne sont pas tous renseignés. Vérifiez le renseignement des titres "
                        "lors de l'nitialisation des graphiques.")
                    raise AttributeError(
                        "Les titres des graphiques ne sont pas tous renseignés. Vérifiez le renseignement des titres "
                        "lors de l'nitialisation des graphiques.")

                else:
                    # Créé l'action de toggle de la barre d'outils
                    graph_toggle_act = QAction(self.__graph_title[j], self)
                    self.__toolbar_toogle_act[i].append(graph_toggle_act)

                    # Ajoute l'action de toggle au sous-menu de la catégorie
                    view_toolbars_category_submenu.addAction(self.__toolbar_toogle_act[i][j])

                    # Rend le bouton toggable et défini son état par défaut
                    self.__toolbar_toogle_act[i][j].setCheckable(True)
                    if self.__toolbar_instance[j].get_visibility:
                        self.__toolbar_toogle_act[i][j].setChecked(True)
                    else:
                        self.__toolbar_toogle_act[i][j].setChecked(False)

                    # Le signal connect n'accepte qu'un argument au type « non-segmenté » en mémoire
                    # (i.e. n'accepte pas les formats de type tableau (str, list, ...). On converti
                    # donc les coordonnées i et j en une chaîne de caracère au format
                    # str(99-i)+str(99-j) où 99 permet de convertir l'indice en un nombre, permettant
                    # d'avoir plus de 10 catégories et/ou graphique sans un traitement compliqué des donnés
                    # au décodage de la chaîne concaténée
                    i_passed = 99 - i
                    j_passed = 99 - j
                    graph_id = int(str(i_passed) + str(j_passed))

                    self.__toolbar_toogle_act[i][j].triggered.connect(
                        functools.partial(self.__toggle_toolbar, graph_id))  # Écoute le signal de toggle

    def __toggle_toolbar(self, graph_id):
        """Affiche ou masque une barre d'outils rattachée à un graphique

        Parameters
        ----------
        graph_id : integer
            id du graphique
        """

        # Converti le code d'indices pour en extraire les indices de catégorie
        # de graphique et d'indice de graphique (== opération inverse d'avant
        # le signal triggered.connect)
        graph_id_str = str(graph_id)
        graph_category = int(99 - int(graph_id_str[0] + graph_id_str[1]))
        graph_index = int(99 - int(graph_id_str[2] + graph_id_str[3]))

        # print("graph_category:", graph_category)
        # print("graph index:", graph_index)

        # Récupère le numéro du graphique à partir des indices
        graph_number = 0

        # Si le signal appartient au graphique de la première catégorie, alors
        # le numéro du graphique correspond à l'indice du graphique
        if graph_category == 0:
            graph_number = graph_index

        # Sinon, pour obtenir le numéro du graphique, les graphiques des catégories
        # précédentes doivent être prises en compte
        else:
            # TODO : tester cette fonction en ayant plusieurs types de graphiques
            for i in range(graph_category):
                if i != range(graph_category):
                    for j in range(len(self.__toggle_toolbar[i])):
                        graph_number += 1
                else:
                    graph_number += graph_index

        # Récupère la visibiltié de la barre d'outils avant toggle
        visibility = self.__toolbar_instance[graph_number].get_visibility()

        # Toggle la visibilité de la barre d'outils
        if visibility:
            self.__toolbar_instance[graph_number].hide_toolbar()
        else:
            self.__toolbar_instance[graph_number].show_toolbar()

    # noinspection PyMethodMayBeStatic
    def __quit(self):
        """Quitte l'application"""

        qApp.quit()
        log.info("Fermeture du dashboard.")


class Layout:
    """Génère l'ensemble des QLayout essentiels à la gestion de la géométrie des élements graphiques

    Parameters
    ----------
    graph_selector : GraphCategorySelector
        instance principale du sélecteur de graphique

    Methods
    -------
    __init_main_layout()
        initialise le layout principal de la fennêtre

    __init_graphs_layouts()
        initialise les layouts propres aux graphiques

    add_widget(widget, widget_type, layout, graph_category)
        ajoute un widget à un layout

    get_main_layout()
        retourne le layout de plus bas niveau de la fenêtre
    """

    def __init__(self, graph_selector=None):
        self.__main_layout = QHBoxLayout()  # Layout contenant la fenêtre principale
        self.__graph_main_layout = QStackedLayout()  # Layout contenant les graphiques : est un layout « à plusieurs
        # pages »
        self.__list_of_grid_layout = []  # Liste de l'ensemble des layouts de type grille
        self.__container_of_graph_widget = []  # Liste des widgets vides qui permettent de stocker les graphiques

        self.__grid_i_layout = []  # Position en x (ligne) du graphique dans le layout grille
        self.__grid_j_layout = []  # Position en y (colonne) du graphique dans le layout grille

        # Permet d'intercépter les demande de mise en surbrillance des graphiques
        self.__communicate = Communicate()  # Instance de récupération de signaux globaux
        # FIXME : voir si la délcaration de self.__trhead pourrait être décallée ici

        # Récupère le sélecteur de graphique et indique sa présence, ou non
        self.__have_graph_selector = False
        self.__graph_selector = graph_selector
        if graph_selector is not None:
            self.__have_graph_selector = True  # Indique la présence ou non d'un sélecteur de graphique

        # Initialisation du layout principal
        self.__init_main_layout()

        # Initialisation des layouts des graphs
        self.__init_graphs_layouts()

    def __init_main_layout(self):
        """Initialise le layout principal de la fennêtre"""

        self.__main_layout.setContentsMargins(0, 0, 0, 0)

    def __init_graphs_layouts(self):
        """Initialise les layouts propres aux graphiques"""

        # Exécute l'initialisaiton des layouts seulement s'ils n'ont pas encore été initialisés

        # Arborescence des layouts et algorithme, du plus petit objet au plus
        # grand :

        # À chaque graphique devant être affiché est associé « container ».
        # Initialement, ce container n'est qu'un QWidget vide et n'est pas rempli
        # d'un graphique. On note ce container (A)

        # L'ensemble des containers (A) sont ajoutés à un « layout de type grille »
        # permettant de regrouper les graphiques en une grille de graphiques
        # On note ce layout de type grille (B)

        # Il y a autant de (B) qu'il y a de catégories de graphiques. Ainsi, on
        # regroupe l'ensemble de ces (B) en un tableau de layout grille noté (C)
        # Il faut voir (C) comme un widget regroupant les graphiques de chaque
        # catégorie de graphique. On peut voir (C) comme une feuille de papier
        # sur laquelle est imprimée plusieurs graphiques

        # Il faut regrouper les différentes catégories de graphique définies par
        # (C) en un widget qui stocke l'ensemble des catégories. Ce widget est
        # comme un livre contenant plusieurs pages. Alors, on va stocker l'ensemble
        # des (C) dans un layout noté (D)

        # Le « livre des graphiques » (D) est ensuite intégré au layout de la fenêtre
        # principale, noté (E)

        # Initialisation des layouts de chaque catégories
        # Pour i allant de 0 au nombre de catégories dans le sélecteur de graphique

        # Les graphiques ne peuvent être catégorisés ssi il existe un sélecteur de graphique
        if self.__have_graph_selector:
            # Récupère la liste des catégories du sélecteur de graphique
            categories_list = self.__graph_selector.get_categories_list()

            for i in range(len(categories_list)):
                # Le container de graphique est un widget vide
                self.__container_of_graph_widget.append(QtWidgets.QWidget())

                # Place le container du graphique dans le layout grille
                grid_layout_to_add = QGridLayout(self.__container_of_graph_widget[i])

                # Ajoute le layout de grille à un tableau regroupant les layouts de type grille
                self.__list_of_grid_layout.append(grid_layout_to_add)

                # Initialise la position (i, j) du premier graphique dans le layout
                self.__grid_i_layout.append(0)
                self.__grid_j_layout.append(0)

            # Ajoute les layouts des types de graphiques au layout principal des graphiques
            for i in range(len(self.__list_of_grid_layout)):
                self.add_widget(self.__container_of_graph_widget[i], "widget_container", self.__graph_main_layout)

            # Ajoute le layout des graphiques sur le layout de la fenêtre principale
            self.__add_layout(self.__main_layout, self.__graph_main_layout, 10)

    def add_widget(self, widget, widget_type, layout=None, graph_category=None):
        """Ajoute un widget à un layout

        Parameters
        ----------
        widget : Qwidget
            widget

        widget_type : str
            type du widget

        layout : QLayout
            layout sur lequel ajouter le widget

        graph_category : str
            catégorie du sélecteur de graphique dans lequel ajouter un widget de type graphique
        """

        # Si le widget est un graphique
        if widget_type == "graph":
            if graph_category is None:
                log.error(
                    "Erreur d'ajout du widget de type " + str(widget_type) + ". Catégorie de graphique non renseignée")
                raise AttributeError(
                    "Erreur d'ajout du widget de type " + str(widget_type) + ". Catégorie de graphique non renseignée")

            else:
                # Créé une instance du sélecteur de catégorie de graphique pour en récupérer les indices
                # des catégories de graphique
                __graph_selector = GraphCategorySelector(None)

                # Récupère le type de graphique permettant de placer le graphique dans le bon layout de type grille
                index_graph_category = __graph_selector.search_category_index(graph_category)

                # Récupère le nombre actuel de graphiques dans la layout de graphique
                # permettant de savoir si un passage à la ligne pour l'affichage du
                # nouveau graphique est nécessaire ou non
                number_of_graph_in_layout = self.__list_of_grid_layout[index_graph_category].count()

                # Si le nombre de graphique est pair, alors on place le nouveau graphique à la ligne suivante
                if number_of_graph_in_layout % 2 == 0 and number_of_graph_in_layout != 0:
                    self.__grid_i_layout[index_graph_category] += 1
                    self.__grid_j_layout[index_graph_category] = 0

                # S'il n'y a qu'un seul graphique sur la ligne, on met notre graphique à la suite
                if number_of_graph_in_layout % 2 == 1:
                    self.__grid_j_layout[index_graph_category] += 1

                # Ajoute le graphique à la case (i, j) définie du layout
                # self.__list_of_grid_layout[index_graph_category].addWidget(widget,
                # self.__grid_i_layout[index_graph_category],
                # self.__grid_j_layout[index_graph_category])

                # Un widget container (type : QGroupBox) permet de stocker le widget du graphique.
                # Le widget container est donc ajouté à la case (i, j) définie du layout, un layout QVBoxLayout est
                # créé dans ce QGroupBox et le widget de graphique est placé dans le QVBoxLayout
                self.__graph_groupbox_widget = QGroupBox()
                self.__list_of_grid_layout[index_graph_category].addWidget(self.__graph_groupbox_widget,
                                                                           self.__grid_i_layout[index_graph_category],
                                                                           self.__grid_j_layout[index_graph_category])
                self.__graph_groupbox_layout = QVBoxLayout()
                self.__graph_groupbox_widget.setLayout(self.__graph_groupbox_layout)
                self.__graph_groupbox_layout.addWidget(widget, alignment=Qt.AlignTop)  # Ajoute le graphe au
                # layout du container

                # Défini le style par défaut de la bordure QGroupBox
                self.__graph_groupbox_widget.setStyleSheet("border: 1px solid white; margin: 3ex; margin-top: 4ex;")

        elif widget_type == "graph_selector":
            layout.insertWidget(0, widget, 1)
            self.__have_graph_selector = True

        elif widget_type == "widget_container":
            layout.addWidget(widget)

        else:
            log.error("Erreur d'ajout du widget de type " + str(widget_type) + ". Vérifier le type de widget.")
            raise AttributeError

    # noinspection PyMethodMayBeStatic
    def __add_layout(self, mother_layout, child_layout, stretch):
        """Ajoute un layout fils dans un layout parent

        Parameters
        ----------
        mother_layout : QLayout
            layout parent

        child_layout : QLayout
            layout fils
        """

        mother_layout.addLayout(child_layout, stretch)

    def get_main_layout(self):
        """Retourne le layout de plus bas niveau de la fenêtre

        Returns
        -------
        self.__main_layout : QLayout
            layout principal
        """

        return self.__main_layout


# En charge du widget de sélection de type de graphique
class GraphCategorySelector:
    """Génère un sélecteur de catégorie de graphique

    Attributes
    ----------
    initial_categories : list
        liste des catégories pré-éxistantes

    Methods
    -------
    __init_categories_indices(initial_categories)
        génère un dictionnaire corrélant les catégories à des indices d'identifiant

    __init_widget()
        initialise le menu de sélection du type de graphique

    __init_signal()
        initialise le signal d'écoute de changement de catégorie

    __set_active_index()
        actualise l'indice de catégorie active

    search_category_index()
        renvoi l'entier i de la catégorie de graphique du sélecteur de graphique auquel un graphique se rattache

    get_active_index()
        retourne l'indice de catégorie active du sélecteur

    get_categories_list()
        retourne la liste des actégories de graphique

    get_categories_indices()
        retourne le dctionnaire des catégories des graphiques associant leurs indices

    get_widget()
        retourne le widget du sélecteur de type de graphique

    add_graph(graph_category)
        ajoute un graphique au sélecteur de graphique en créant automatiquement une catégorie si la catégorie du
        graphique n'existe pas dans le sélecteur de graphique

    remove_graph(graph_category)
        retire un graphique au sélecteur de graphique en supprimant automatiquement une catégorie si la catégorie du
        graphique n'est attachée à aucun graphique

    get_nb_graph_in_category(category)
        retourne le nombre de graphiques présents dans une catégorie de graphiques
    """

    __nb_graph_in_category = {}  # {"Nom de la catégorie" : nombre de graphiques dans la catégorie}
    __nb_instance = 0  # Nombre d'instances de cette classe
    __categories_list = []  # Liste de str des catégories
    __categories_indices = {}  # Dictionnaire des catégories des graphiques dans le sélecteur de graphique

    # associant leurs indices

    def __init__(self, initial_categories=None):
        self.__active_index = 0  # Indice de la page active
        self.__widget = QListWidget()  # Widget du sélecteur

        # Initialise les catégories du sélecteur par rapport aux graphiques existants
        self.__init_categories_indices(initial_categories)

        # Initialise le widget
        self.__init_widget()

        # Initialise le signal lor de l'actualisation du widget
        self.__init_signal()

        GraphCategorySelector.__nb_instance += 1

    # noinspection PyMethodMayBeStatic
    def __init_categories_indices(self, initial_categories=None):
        """Génère un dictionnaire corrélant les catégories à des indices d'identifiant

        Parameters
        ----------
        initial_categories : list
            liste des catégories pré-éxistantes
        """

        # Supprime l'ancien contenu
        GraphCategorySelector.__categories_list = []
        GraphCategorySelector.__categories_indices.clear()

        # Si le nombre d'instance est nul, alors l'initialisation du sélecteur de graphique
        # nécessite au moins une catégorie à être renseignée
        if GraphCategorySelector.__nb_instance == 0 and initial_categories is not None:
            GraphCategorySelector.__categories_list = initial_categories  # Liste des catégories initiales
            GraphCategorySelector.__nb_graph_in_category = {GraphCategorySelector.__categories_list[i]: 0 for i in
                                                            range(len(GraphCategorySelector.__categories_list))}

        elif GraphCategorySelector.__nb_instance == 0 and initial_categories is None:
            log.error(
                "Lors de l'initialisation du sélecteur de graphique, veuillez renseigner au moins une catégorie de "
                "graphique")
            raise AttributeError

        else:
            GraphCategorySelector.__categories_list = list(GraphCategorySelector.__nb_graph_in_category.keys())

        # Dictionnaire des catégories
        # Combine la liste du sélecteur à des indices de catégories
        temp_dict_keys = list(GraphCategorySelector.__nb_graph_in_category.keys())
        GraphCategorySelector.__categories_indices = {temp_dict_keys[i]: i for i in
                                                      range(len(GraphCategorySelector.__nb_graph_in_category))}

    def __init_widget(self):
        """Initialise le menu de sélection du type de graphique"""
        # Ajoute les items au sélecteur
        for i in range(len(self.__categories_list)):
            item = QListWidgetItem(self.__categories_list[i])
            item.setTextAlignment(Qt.AlignCenter)
            self.__widget.addItem(item)

    def __init_signal(self):
        """Initialise le signal d'écoute de changement de catégorie"""
        # Écoute le signal de changement de catégorie et appelle la fonction de
        # changement d'indice actif si la catégorie a été changée
        self.__widget.itemSelectionChanged.connect(self.__set_active_index)

    def __set_active_index(self):
        """Actualise l'indice de catégorie active"""
        # print("Current list item:", self.graph_type_selector.currentRow())
        # self.graph_main_layout.setCurrentIndex(self.graph_type_selector.currentRow())
        self.__active_index = self.__widget.currentRow()

    # noinspection PyMethodMayBeStatic
    def search_category_index(self, desired_category):
        """Renvoi l'entier i de la catégorie de graphique du sélecteur de graphique auquel un graphique se rattache

        Parameters
        ----------
        desired_category : str
            nom de la catégorie de graphique

        Returns
        -------
        index : int
            indice de la catégorie de graphique dans le sélecteur
        """
        try:
            index = GraphCategorySelector.__categories_indices[desired_category]
        except KeyError:
            log.critical("Catégorie de graphique incorrecte. Catégorie entrée : " + desired_category)
            sys.exit(KeyError("KeyError : catégorie de graphique incorrecte. Catégorie entrée : " + desired_category))
        else:
            return index

    def get_active_index(self):
        """Retourne l'indice de catégorie active du sélecteur

        Returns:
        --------
        self.__active_index : int
            indice de la catégorie active
        """
        return self.__active_index

    # noinspection PyMethodMayBeStatic
    def get_categories_list(self):
        """Retourne la liste des actégories de graphique

        Returns:
        --------
        self.__categories_list : list[str]
            liste des catégories
        """
        return GraphCategorySelector.__categories_list

    # noinspection PyMethodMayBeStatic
    def get_categories_indices(self):
        """Retourne le dctionnaire des catégories des graphiques associant leurs indices

        Returns:
        --------
        self.__categories_dict : dict[str: int]
            dictionnaire des catégories
        """
        return GraphCategorySelector.__categories_indices

    def get_widget(self):
        """Retourne le widget du sélecteur de type de graphique

        Returns:
        --------
        self.__widget : QListWidget
            widget du sélecteur de graphique
        """
        return self.__widget

    def add_graph(self, graph_category):
        """Ajoute un graphique au sélecteur de graphique en créant automatiquement une catégorie si la catégorie du
        graphique n'existe pas dans le sélecteur de graphique

        Parameters
        ----------
        graph_category : str
            catégorie du graphique
        """
        # Cherche dans le dictionnaire de catégories pour la catégorie de graphique renseignée
        # Si la catégorie existe déjà, on incrémente le nombre de graphiques dans la catégorie
        if graph_category in GraphCategorySelector.__nb_graph_in_category:
            GraphCategorySelector.__nb_graph_in_category[graph_category] += 1
        # Si la catégorie n'existe pas, on la créé et on indique un graphique présent
        else:
            GraphCategorySelector.__nb_graph_in_category[graph_category] = 1

        # Met à jour la liste des catégories et le dictionnaire des indices de catégories
        self.__init_categories_indices()

    def remove_graph(self, graph_category):
        """Retire un graphique au sélecteur de graphique en supprimant automatiquement une catégorie si la catégorie du
        graphique n'est attachée à aucun graphique

        Parameters
        ----------
        graph_category : str
            catégorie du graphique
        """

        # Cherche pour la catégorie renseignée par le graphique dans le dictionnaire des catégories
        # Si les catégories correspondent, le graphique peut être retiré
        if graph_category in GraphCategorySelector.__nb_graph_in_category:
            # S'il restait deux graphiques dans la catégorie avant supression
            # d'un des deux graphiques, la catégorie peut toujours exister
            if GraphCategorySelector.__nb_graph_in_category[graph_category] >= 2:
                GraphCategorySelector.__nb_graph_in_category[graph_category] -= 1
            # Sinon, la catégorie est supprimée
            elif GraphCategorySelector.__nb_graph_in_category[graph_category] == 1:
                GraphCategorySelector.__nb_graph_in_category.pop(graph_category)

            # Met à jour la liste des catégories et le dictionnaire des indices de catégories
            self.__init_categories_indices()

        else:
            log.error(
                "La catégorie du graphgique à retirer du sélecteur de graphique est incorrecte. Vérifiez le nom de la "
                "catégorie associée au graphique.")
            raise AttributeError()

    # noinspection PyMethodMayBeStatic
    def get_nb_graph_in_category(self, category):
        """Retourne le nombre de graphiques présents dans une catégorie de graphiques

        Parameters
        ----------
        category : str
            catégorie de graphique

        Returns
        -------
        nb_graphs : integer
            nombre de graphiques dans la catégorie
        """
        nb_graphs = -1

        try:
            nb_graphs = GraphCategorySelector.__nb_graph_in_category[category]

        except AttributeError:
            pass

        return nb_graphs


class Graph(metaclass=ABCMeta):
    """Classe abstraite des classes de graphiques. Génère les graphiques

    Attributes
    ----------
    visibility : bool
        visibilité du graphique sur la fenêtre

    data : list
        liste des données à lire dans la base de données

    Methods
    -------
    _init_widget()
        initialise le widget du graphique

    _add_values()
        ajoute une série de données au graphique

    _remove_values()
        retire une série de données au graphique

    _reformate_data_matrix_to_graph_plot()
        converti le format de stockage des données sous forme matricielle en un format lisible par Matplotlib

    _read_data_from_database()
        récupère les données depuis la base de données

    _draw_graph(fill_color=[])
        affiche ou actualise la série de données dans le graphique

    get_widget()
        retourne le widget du graphique

    get_visibility()
        retourne la visibilité du graphique

    set_visibility(visibility)
        défini la visibilité du graphique

    get_title()
        renvoi le titre du graphique
    """

    _visibility = None
    _graph = None

    def __init__(self, title, visibility=True, data=None):
        self._title = title  # Titre du graphique
        self._visibility = visibility  # Visibilité du graphique
        self._plots = None  # Données sous forme matricielle
        self._database_data_list = np.array([])  # Liste de chaînes de caractères des données à récupérer de la BDD

        # Créé le widget de graphique
        self._init_widget()

        # Créé la figure Matplotlib et la grille de tracé
        self._graph_ax = self._graph.figure.subplots()

        # Lis les données de la BDD si présence de donénes (i.e. non en mode de graphique auto-généré)
        if data is not None:
            self._read_data_from_database(data)

    @classmethod
    def _init_widget(cls):
        """Initialise le widget du graphique"""

        # Dimensions de la figure
        length = 2
        height = 5

        cls._graph = FigureCanvas(Figure(figsize=(length, height)))

    @abstractmethod
    def _add_values(self, data, delete_old_data, refresh):
        """Ajoute une série de données au graphique"""

        raise NotImplementedError

    @abstractmethod
    def _remove_values(self):
        """Retire une série de données au graphique"""

        raise NotImplementedError

    @abstractmethod
    def _reformate_data_matrix_to_graph_plot(self):
        """Converti le format de stockage des données sous forme matricielle en un format lisible par Matplotlib"""

        raise NotImplementedError

    @abstractmethod
    def _read_data_from_database(self, data):
        """Récupère les données de la base de données et les met sous forme de matrice de points

        Parameters
        ----------
        data : list[str]
            données à récupérer dans la base de données
        """

        raise NotImplementedError

    @classmethod
    def _draw_graph(cls, fill_color=None):
        """Affiche ou actualise la série de données dans le graphique

        Paramters
        ---------
        fill_color : list[str]
            couleur de remplissage sous la courbe en format HTML
        """

        # Récupère les donnéees en x et en y des courbes
        if fill_color is None:
            fill_color = []
        x_data, y_data = cls._reformate_data_matrix_to_graph_plot()
        return x_data, y_data

    @classmethod
    def get_widget(cls):
        """Retourne le widget du graphique

        Returns
        -------
        self._graph
            widget du graphique
        """

        return cls._graph

    @classmethod
    def get_visibility(cls):
        """Retourne la visibilité du graphique

        Returns
        -------
        self._visibility
            visibilité du graphique"""

        return cls._visibility

    @classmethod
    def set_visibility(cls, visibility):
        """Défini la visibilité du graphique

        Parameters
        ----------
        visibility : bool
            visibilité du graphique"""

        if visibility:
            cls._visibility = False

        else:
            cls._visibility = True


class StandardGraph(Graph):
    """Génère les graphiques standards de graphiques continus à n courbes sous forme de nuage de points reliés

    Attributes
    ----------
    title : str
        titre du graphique

    x_label : str
        label de l'axe d'abscisse

    y_label : str
        label de l'axe des ordonnées

    visibility : bool
        visibilité du graphique sur la fenêtre

    data : list
        liste des données à lire dans la base de données

    Methods
    -------
    _read_data_from_database(data)
        récupère les données de la base de données et les met sous forme de matrice de points

    _reformate_data_matrix_to_graph_plot()
        converti le format de stockage des données sous forme matricielle en un format lisible par Matplotlib

    _draw_graph()
        affiche ou actualise la série de données dans le graphique

    _add_values(data, delete_old_data, refresh)
        ajoute une série de données au graphique

    _remove_values()
        retire une série de données au graphique
    """

    # L'ensemble des points est stockée dans une matrice de dimensions m*n où :
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

    def __init__(self, title, x_label, y_label, visibility, data=None):
        super().__init__(title, visibility)

        self._title = title
        self._x_label = x_label  # Label de l'axe d'abscisse
        self._y_label = y_label  # Label de l'axe des ordonnées
        self.__fill_color = []  # Couleur de remplissage des graphiques

        # Renomme les axes et ajoute un titre
        self._graph_ax.set_title(self._title)
        self._graph_ax.set_xlabel(self._x_label)
        self._graph_ax.set_ylabel(self._y_label)

    def _add_values(self, data, delete_old_data, refresh):
        """ Ajoute des données dans la matrice de points et permet une actualisation du graphique

        Parameters
        ----------
        data : numpy.array
            matrice de points à ajouter

        delete_old_data : bool la valeur True supprime l'excédent d'anciennes données sur le graphique évitant
        d'afficher une trop grande série de données

        refresh : bool
            la valeur True force l'actualisation (visuelle) du graphique
        """
        # TODO : forcer l'actualisation graphique lors de retrait de données

        # Concatène les deux tableaux par colonne en respectant le format de données
        self._plots = np.concatenate((self._plots, data))

        # L'ajoute de nouvelles données augmente la densité de données à afficher,
        # alors si ce paramètre est vrai, on enlève la quantité de données à afficher
        # correspondant à la quantité de nouvelles données
        if delete_old_data:
            number_of_rows, number_of_columns = data.shape

            self._plots = np.delete(self._plots, slice(0, number_of_rows, 1), 0)

        if refresh:
            self._draw_graph()

    # TODO : méthode _remove_values
    def _remove_values(self):
        """Retire des points de la matrice de données"""

        pass

    def _reformate_data_matrix_to_graph_plot(self):
        """ Reformatte les données de la matrice de points des graphiques en format [[x_graphique_1],
        [[x_graphique_2], ..., [[x_graphique_n]] et [[y_graphique_1], [[y_graphique_2], ..., [[y_graphique_n]]
        interprétable par la fonction de tracé

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
        number_of_rows, number_of_columns = self._plots.shape

        # Récupère les données de la matrice plots et les stocke dans des vecteurs x_points_all_curves et
        # y_points_all_curves
        for i in range(number_of_columns):  # De "gauche à droite" sur la matrice
            for j in range(number_of_rows):  # De "haut en bas" sur la matrice
                # Si on explore la première colonne, on récupère les points d'abscisse
                if i == 0:
                    x_points_one_curve.append(self._plots[j, 0])

                    # Une fois que la première colonne a été parcourue, on pousse le vecteur de points pour sauvegarde
                    if j == (number_of_rows - 1):
                        x_points_all_curves.append(x_points_one_curve)

                # Si on explore une colonne autre que la première colonne, alors on récupère des points en y
                else:
                    y_points_one_curve.append(self._plots[j, i])
                    # Une fois que la colonne a été parcourue, on pousse le vecteur de points pour sauvegarde
                    if j == (number_of_rows - 1):
                        # Passage d'une copie de y_points_one_curve
                        # https://stackoverflow.com/questions/39606601/python-append-a-list-to-another-list-and-clear-the-first-list
                        y_points_all_curves.append(y_points_one_curve[:])
                        # Vide le vecteur temporaire pour passer à la prochaine courbe
                        y_points_one_curve = []

        return x_points_all_curves, y_points_all_curves

    def _read_data_from_database(self, data):
        # TODO : méthode _read_data_from_database
        """Récupère les données de la base de données et les met sous forme de matrice de points

        Parameters
        ----------
        data : list[str]
            données à récupérer dans la base de données
        """

        pass
        # Par exemple, en utilisant self.database_data_list, récupérer data

    def _draw_graph(self, fill_color=None):
        """Affiche ou actualise la série de données dans le graphique

        Parameters
        ----------
        fill_color : list[str]
            couleur de remplissage sous la courbe en format HTML
        """

        data_graph_line = None

        if fill_color is None:
            fill_color = []
        x_data, y_data = self._reformate_data_matrix_to_graph_plot()

        # Replotte individuellement chaque courbe et la re-remplie si demandée
        for i in range(len(y_data)):
            # Vérifie le code HTML de la couleur. valid_color est vrai si code HTML valide, faux sinon
            # via https://stackoverflow.com/questions/30241375/python-how-to-check-if-string-is-a-hex-color-code
            valid_color = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', fill_color[i])

            # Si le grapique n'est pas rempli, on trace les lignes de limitation de la courbe
            if not valid_color:
                alpha_lines = 1

            # Sinon, on ne trace pas les lignes de limitation de la courbe
            elif valid_color:
                alpha_lines = 0

            else:
                alpha_lines = 0

            # Tracé du graphique
            self._data_graph_line, = self._graph_ax.plot(x_data[0], y_data[i], alpha=alpha_lines)

            # print("Couleur d'indice " + str(i) + " (" + str(fill_color[i] + ") : valid_color = " + str(bool(
            # valid_color))))

            # Remplissage du graphique
            if str(bool(valid_color)) == "True":  # re.search renvoie un booléen casté en str. Pourquoi pas !
                self._graph_ax.fill_between(x_data[0], y_data[i], color=fill_color[i])

        # Retrace le graphique
        self._data_graph_line.figure.canvas.draw()

    def get_title(self):
        """Retourne le titre du graphique

        Returns
        -------
        self._title : str
            titre du graphique
        """

        return self._title


class PositionGraph(StandardGraph):
    """Graphique des courbes de restriction de vitesse d'ERTMS/EVC

        Attributes
        ----------
        title : str
            titre du graphique

        x_label : str
            label de l'axe d'abscisse

        y_label : str
            label de l'axe des ordonnées

        data : list
            liste des données à lire dans la base de données

        visibility : bool
            visibilité du graphique sur la fenêtre
        """

    def __init__(self, title="ERTMS",
                 x_label="Temps (s)",
                 y_label="Vitesse (km/h)",
                 data=None,
                 visibility=True
                 ):
        # data = ["ertms"]

        super().__init__(title, x_label, y_label, visibility, data)

        if data is None:
            data = []
        self._draw_graph()


class ERTMSGraph(StandardGraph):
    """Graphique des courbes de restriction de vitesse d'ERTMS/EVC

        Attributes
        ----------
        title : str
            titre du graphique

        x_label : str
            label de l'axe d'abscisse

        y_label : str
            label de l'axe des ordonnées

        data : list
            liste des données à lire dans la base de données

        visibility : bool
            visibilité du graphique sur la fenêtre
        """

    def __init__(self, title="ERTMS",
                 x_label="Temps (s)",
                 y_label="Vitesse (km/h)",
                 data=None,
                 visibility=True
                 ):
        # data = ["ertms"]

        super().__init__(title, x_label, y_label, data)

        if data is None:
            data = []
        self._draw_graph()


class SpeedGraph(StandardGraph):
    """Graphique de vitesse générique

        Attributes
        ----------
        title : str
            titre du graphique

        x_label : str
            label de l'axe d'abscisse

        y_label : str
            label de l'axe des ordonnées

        data : list
            liste des données à lire dans la base de données

        visibility : bool
            visibilité du graphique sur la fenêtre
        """

    def __init__(self, title="Speed",
                 x_label="Temps (s)",
                 y_label="Vitesse (km/h)",
                 data=None,
                 visibility=True
                 ):
        # data = ["speed"]

        super().__init__(title, x_label, y_label, visibility, data)

        if data is None:
            data = []
        self._draw_graph()


class AccelerationGraph(StandardGraph):
    """Graphique d'accélération générique

        Attributes
        ----------
        title : str
            titre du graphique

        x_label : str
            label de l'axe d'abscisse

        y_label : str
            label de l'axe des ordonnées

        data : list
            liste des données à lire dans la base de données

        visibility : bool
            visibilité du graphique sur la fenêtre
        """

    def __init__(self, title="Accéleration",
                 x_label="Temps (s)",
                 y_label="Accélération (m/s²)",
                 data=None,
                 visibility=True
                 ):
        # data = ["acceleration"]

        super().__init__(title, x_label, y_label, visibility, data)

        if data is None:
            data = []
        self._draw_graph()


class JerkGraph(StandardGraph):
    """Graphique d'à-coup générique

        Attributes
        ----------
        title : str
            titre du graphique

        x_label : str
            label de l'axe d'abscisse

        y_label : str
            label de l'axe des ordonnées

        data : list
            liste des données à lire dans la base de données

        visibility : bool
            visibilité du graphique sur la fenêtre
        """

    def __init__(self, title="À-coup",
                 x_label="Temps (s)",
                 y_label="À-coup (m/s³)",
                 data=None,
                 visibility=True
                 ):
        # data = ["a-coup"]

        super().__init__(title, x_label, y_label, visibility, data)

        if data is None:
            data = []
        self._draw_graph()


class TestStandardGraph(StandardGraph):
    """Graphique standard de test utilisant une série de données personnalisée et n'utilisant pas la base de données

        Attributes
        ----------
        title : str
            titre du graphique

        x_label : str
            label de l'axe d'abscisse

        y_label : str
            label de l'axe des ordonnées

        visibility : bool
            visibilité du graphique sur la fenêtre

        Methods
        -------
        __init_test_data()
            génère le set de données du graphique standard de test
        """

    def __init__(self, title="Démonstration de graphique standard",
                 x_label="Label de l'axe d'abscisse",
                 y_label="Label de l'axe des ordonnées",
                 visibility=True
                 ):
        super().__init__(title, x_label, y_label, True)

        # Initialise la série de données
        self.__init_test_data()

        self._draw_graph(self.__fill_color)

    def __init_test_data(self):
        # Génération manuelle de données
        self._plots = np.array([[1, 190, 175, 160, 160],
                                [2, 190, 175, 160, 160],
                                [3, 190, 175, 160, 140],
                                [4, 190, 175, 140, 120],
                                [5, 190, 155, 120, 120],
                                [6, 190, 135, 120, 120],
                                [7, 190, 135, 120, 105],
                                [8, 190, 135, 105, 90],
                                [9, 190, 90, 85, 75],
                                [10, 190, 80, 65, 75]])

        self.__fill_color = ["#C00000", "#EA9100", "#DFDF00", "#969696"]


class CustomNavigationToolBar(NavigationToolbar):
    """Génère une barre d'outil rattachée à un graphique

    Attributes
    ----------
    dashboard_class : QMainWindow
        classe de la fenêtre du dashboard

    graph_widget : QWidget
        widget du graphique

    window : QWidget
        widget de la fenêtre principale

    visibility : boolean
        visibilité de la barre d'outils

    graph_title : str
        titre du graphique

    hidden_tools : list[str]
        liste des outils à retirer de la barre d'outils

    Methods
    -------
    __remove_tools()
        supprime des outils de la liste d'outils de la barre d'outils

    __add_identifier_label()
        ajoute un label à la barre d'outils

    __get_toolbar()
        retourne la barre d'outils (customisée)

    hide_toolbar()
        masque la barre d'outils

    show_toolbar()
        affiche la barre d'outils

    get_visibility()
        récupère l'état d'affichage de la barre d'outil
    """

    def __init__(self, dashboard_class=None, graph_widget=None, window=None, visibility=True, graph_title=None,
                 hidden_tools=None, communicate=None):

        self.__toolbar = ""
        self.__dashboard_class = dashboard_class
        self.__graph_widget = graph_widget
        self.__graph_title = graph_title
        self.__hidden_tools = hidden_tools
        self.__visibility = visibility
        self.__communicate = communicate

        if self.__hidden_tools is not None:
            self.__remove_tools()

        if self.__graph_widget is not None and window is not None:
            self.__toolbar = NavigationToolbar(self.__graph_widget, window)

        # if self.__communicate is not None:
        self.__add_identifier_label()  # Ajoute un label permettant d'identifier le graphe auquel se rattache
        # la barre d'outils

        if self.__visibility is not None and not self.__visibility:
            self.hide_toolbar()

    def __remove_tools(self):
        """Supprime des outils de la liste d'outils de la barre d'outils"""

        if self.__hidden_tools is not None:
            # Récupère la liste des items dans la ToolBar sous forme de liste de tuples
            self.toolitems = list(self.toolitems)

            # Affiche les items présents dans la toolbar originelle avant modifications
            # print(*self.toolitems, sep="\n")

            # Si un élement se trouve dans la liste hidden_tools,
            # Chercher cet élement correspondant dans self.toolitems et supprimer le tuple associé
            # Si l'élement à supprimer est introuvable dans self.toolitems, logguer l'erreur et ne rien supprimer
            for i in range(len(self.__hidden_tools)):
                # Recherche de l'index du tuple à supprimer
                # via https://stackoverflow.com/questions/6518291/using-index-on-multidimensional-lists/6518412
                try:
                    # Récupère le tuple à supprimer
                    x = [x for x in self.toolitems if self.__hidden_tools[i] in x][0]

                    # Récupère l'index du tuple à supprimer
                    index = self.toolitems.index(x)

                    # Vérifie que le tuple à supprimer correspond à ce qui doit être supprimé
                    if self.__hidden_tools[i] == self.toolitems[index][0]:
                        self.toolitems.pop(index)

                except (IndexError, ValueError):
                    log.error("Impossible de supprimer l'élement « " + str(self.__hidden_tools[i][0]) + "» de la "
                                                                                                        "barre de "
                                                                                                        "navigation "
                                                                                                        "du "
                                                                                                        "graphique. "
                                                                                                        "Vérifiez le "
                                                                                                        "nom de "
                                                                                                        "l'élement à "
                                                                                                        "supprimer")
                    continue

    def __add_identifier_label(self):
        """Ajoute un bouton d'identification du graphique à la barre d'outils permettant de mettre un graphique
        en surbrillance quand le bouton est pressé"""

        if self.__graph_title is not None:
            # https://www.geeksforgeeks.org/pyqt5-qaction/
            self.__graph_label = QAction(self.__graph_title, self.__dashboard_class)
            self.__toolbar.addAction(self.__graph_label)

    def get_toolbar(self):
        """Retourne la barre d'outils (customisée)
        Returns
        -------
        self.__toolbar : QToolBar
            barre d'outils
        """

        return self.__toolbar

    def hide_toolbar(self):
        """Masque la barre d'outils"""

        self.__toolbar.setVisible(False)
        self.__visibility = False

    def show_toolbar(self):
        """Affiche la barre d'outils"""

        self.__toolbar.setVisible(True)
        self.__visibility = True

    def get_visibility(self):
        """Récupère l'état d'affichage de la barre d'outils

        Returns
        -------
        self.__visibility : boolean
            visibilité de la barre d'outils"""

        return self.__visibility

    def _init_toolbar(self):
        pass


class Communicate(QObject):
    pass
    # TODO doc
    # highlight_graph = pyqtSignal(str)


class Worker(QThread):
    # TODO doc
    def __init__(self, parent=None, communicate=Communicate()):
        super(Worker, self).__init__(parent)
        self.__communicate = communicate
        # self.__toolbar_instance = CustomNavigationToolBar(None, None, None, None, None, None,
        # communicate=self.__communicate)

    def run(self):
        pass
        # TODO doc
        # self.__toolbar_instance.highlight_graph()


def main():
    init_logging()
    log.info("Lancement du tableau de bord.")

    qapp = init_qapplication()
    init_app_style(qapp)

    dashboard = DashboardWindow()
    dashboard.show()
    dashboard.resize(1920, 1080)
    dashboard.activateWindow()  # Met le focus sur la fenêtre
    dashboard.raise_()  # Place la fenêtre prioritaire

    qapp.exec_()  # Exécute l'instance qApplication en boucle jusqu'à sa fermeture


def init_logging():
    """Initialise le logging"""

    # Lance le fichier de log en mode warning pour récupérer les warnings et erreurs critiques
    log.initialise(PROJECT_DIR + "log\\", VERSION, INITIAL_LOGGING)


def init_qapplication():
    """Initialise la QApplication

    Returns
    -------
    qapp : QApplication
        gère le flux de contrôle et les paramètres principaux de l'application graphique
    """

    # Vérifie s'il n'y a pas une instance de QApplication en cours d'execution
    qapp = QApplication.instance()
    if not qapp:
        # On passe sys.argv pour activer le contrôle par ligne de commande
        qapp = QApplication(sys.argv)

    return qapp


def init_app_style(qapp):
    # Défini le style de l'application
    qapp.setStyle('Fusion')

    try:
        with open("dashboard.qss", "r") as f:
            _style = f.read()
            qapp.setStyleSheet(_style)
    except FileNotFoundError:
        log.error("Impossible de charger le style QSS du tableau de bord.")


if __name__ == "__main__":
    main()
