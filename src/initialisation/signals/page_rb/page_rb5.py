import logging
import os
import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


class PageRB5:
    """Class de la page de settings 5"""

    index = 5   # Attention dans les tableaux l'index comment à 0 donc index_tab = index - 1
    page = None
    current_button = None
    screen_count = 0
    screen_index = []
    screen_default = {"Liste 1": {"écran1": [True, 640, 480],
                                  "écran2": [False, 0, 0]
                                  },
                      "Liste 2": {"écran3": [True, 640, 900]}
                      }
    screen_settings = {}
    category_active = ""
    visible_screen_names = []
    visible_screen_activable = []
    visible_screen_minimum_wh = []

    def __init__(self, application, page, index, current_button):
        # Stocke les informations nécessaires au fonctionnement de la page
        self.index = index
        self.page = page
        self.current_button = current_button
        self.current_button.setProperty("text", "Écrans")

        # Récupère le nombre d'écrans présents
        self.screen_count = QDesktopWidget().screenCount()
        self.screen_index = [None] * self.screen_count
        logging.info("[page_rb5] : " + str(self.screen_count) + " écrans détectés.\n")

        # Charge autant de fenêtres que besoins
        for screen_index in range(0, self.screen_count):
            application.engine.load('initialisation/graphics/page_rb/page_rb5/screen_index.qml')
            self.screen_index[screen_index] = application.engine.rootObjects()[len(application.engine.rootObjects()) - 1]
            self.screen_index[screen_index].hide()

        # Change les informations sur chaque pages
        screen_dimensions = []
        for screen_index in range(0, self.screen_count):
            sg = QDesktopWidget().screenGeometry(screen_index).getCoords()
            self.screen_index[screen_index].setPosition(sg[0], sg[1])
            screen_dimensions.append([sg[2] + 1, sg[3] + 1])
            window = self.screen_index[screen_index].findChild(QObject, "screen_index")
            window.setProperty("text", str(screen_index + 1))

        # Crée une liste avec la liste des écrans (Aucun + tous les nombres de 1 au nombre d'écrans
        screen_list = ["Aucun"]
        for index in range(1, len(screen_dimensions) + 1):
            screen_list.append(str(index))

        # Envoie liste des fenètre et de leurs dimensions à la graphique de la page*
        self.page.setProperty("screenList", screen_list)
        self.page.setProperty("screenSize", screen_dimensions)

        # Définit le fonctionnement de base des boutons supérieurs et inférieurs
        # Aucun des boutons ne sera fonctionnel et aucune page ne sera chargée
        if len(self.screen_default.keys()) != 0:
            # Change le nom de la catégorie pour la première catégorie d'écrans (pour initialiser une page)
            self.category_active = list(self.screen_default.keys())[0]
            self.page.findChild(QObject, "category_title").setProperty("text", self.category_active)
            self.change_visible_screens()
            if len(self.screen_default.keys()) > 1:
                # S'il y a plus d'une catégorie d'écrans, rend les boutons supérieurs de catégories fonctionnels
                left_button = self.page.findChild(QObject, "left_category_button")
                left_button.clicked.connect(lambda l=left_button: self.on_left_category_button_clicked(l))
                right_button = self.page.findChild(QObject, "right_category_button")
                right_button.setProperty("isActivable", True)
                right_button.clicked.connect(lambda r=right_button: self.on_right_category_button_clicked(r))

            # Rend fonctionnel les boutons inférieurs
        else:
            # Dans le cas où la liste des écrans à paramétrer est nulle
            self.page.findChild(QObject, "category_title").setProperty("isDarkGrey", True)
            raise NameError("Aucun écran à paramétrer. Le dictionnaire \"screen_default\" est vide.")



        # Définit la page comme complète
        application.is_completed[4] = True

    def on_page_opened(self, application):
        for screen_index in self.screen_index:
            screen_index.show()

        #TODO : fonction pour mettre à jour les écrans visibles

    def on_page_closed(self, application):
        for screen_index in self.screen_index:
            screen_index.hide()

    def on_left_category_button_clicked(self, left_category_button):
        category_title = self.page.findChild(QObject, "category_title")
        try:
            # Récupère l'index et le nom du nouvel élément
            new_index = list(self.screen_default.keys()).index(category_title.property("text")) - 1
            self.category_active = list(self.screen_default.keys())[new_index]
        except (IndexError, KeyError):
            # Si le nouvel élément n'a pas été trouvé, désactive le bouton et laisse un message d'erreur
            logging.debug("La catégorie d'écran n'a pas été trouvée.\n")
            left_category_button.setProperty("isActivable: false")
        else:
            # Si nouvel élément trouvé, change le titre de la catégorie.
            category_title.setProperty("text", self.category_active)

            # Appelle la fonction pour changer les écrans visibles
            self.change_visible_screens()

            # Rend le bouton de droite actif, et si première catégorie rend celui de gauche inactif
            self.page.findChild(QObject, "right_category_button").setProperty("isActivable", True)
            if new_index == 0:
                left_category_button.setProperty("isActivable", False)

    def on_right_category_button_clicked(self, right_category_button):
        category_title = self.page.findChild(QObject, "category_title")
        try:
            # Récupère l'index et le nom du nouvel élément
            new_index = list(self.screen_default.keys()).index(self.category_active) + 1
            self.category_active = list(self.screen_default.keys())[new_index]
        except (IndexError, KeyError):
            # Si le nouvel élément n'a pas été trouvé, désactive le bouton et laisse un message d'erreur
            logging.debug("La catégorie d'écran n'a pas été trouvée.\n")
            right_category_button.setProperty("isActivable: false")
        else:
            # Si nouvel élément trouvé, change le titre de la catégorie.
            category_title.setProperty("text", self.category_active)

            # Appelle la fonction pour changer les écrans visibles
            self.change_visible_screens()

            # Rend le bouton de gauche actif, et si dernière catégorie rend celui de droite inactif
            self.page.findChild(QObject, "left_category_button").setProperty("isActivable", True)
            if new_index == len(self.screen_default.keys()) - 1:
                right_category_button.setProperty("isActivable", False)

    def change_visible_screens(self):
        # Essaye de récupérer le dictionnaire des écrans de la catégorie sélectionnée
        try:
            category_screen_dict = self.screen_default[self.category_active]
        except KeyError:
            logging.error("Aucune catégorie d'écrans au nom de : " + self.category_active + ".\n")
        else:
            #Récupère les clés (nom des écrans) du dictionnaire récupéré (pour optimisation)
            category_screen_list = list(category_screen_dict.keys())

            # Vide les liste qui seront envoyés à la partie graphique
            self.visible_screen_names = []
            self.visible_screen_activable = []
            self.visible_screen_minimum_wh = []

            # S'il y a plus de 4 écrans dans la catégorie, montre les 4 premiers sinon les montre tous
            for index in range(0, len(category_screen_list) if len(category_screen_list) <= 4 else 4):
                screen_data = category_screen_dict[category_screen_list[index]]
                self.visible_screen_names.append(category_screen_list[index])
                # Vérifie si l'écran a bien les 3 éléments nécessaires
                if(len(screen_data)) >= 3:
                    # Si les 3 éléments sont présents, récupère leurs valeurs et les rajoutes
                    self.visible_screen_activable.append(not not screen_data[0])
                    self.visible_screen_minimum_wh.append([int(screen_data[1]), int(screen_data[2])])
                else:
                    # Si les valeurs ne sont pas présentes, laisse un message d'erreur et rajoute des valeurs par défaut
                    logging.warning("Les caractéristiques de " + category_screen_list[index] + " ne sont pas bonnes.\n")
                    self.visible_screen_activable.append(False)
                    self.visible_screen_minimum_wh.append([0, 0])

        # Maintenant que toutes les valeurs ont été récupérés, les ajoutent à la partie graphique
        self.page.setProperty("screenNames", self.visible_screen_names)
        self.page.setProperty("screenActivable", self.visible_screen_activable)
        self.page.setProperty("minimumWH", self.visible_screen_minimum_wh)


#TODO prendre en considération si plusieurs pages
# TODO faire les fonctions pour récupérer les valeurs de la partie graphique
#TODO faire le get_values
#TODO faire le système de traduction
#TODO faire le change_language
