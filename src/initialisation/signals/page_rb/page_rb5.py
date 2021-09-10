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

        # Définit la page comme complète
        application.is_completed[4] = True

    def on_page_opened(self, application):
        for screen_index in self.screen_index:
            screen_index.show()

    def on_page_closed(self, application):
        for screen_index in self.screen_index:
            screen_index.hide()
