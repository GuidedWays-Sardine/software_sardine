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
    screen_list = []
    test = None

    def __init__(self, application, page, index, current_button):
        # Stocke les informations nécessaires au fonctionnement de la page
        self.index = index
        self.page = page
        self.current_button = current_button
        self.current_button.setProperty("text", "Écrans")

        # Récupère le nombre d'écrans présents
        self.screen_count = QDesktopWidget().screenCount()
        self.screen_list = [None] * self.screen_count
        logging.info("[page_rb5] : " + str(self.screen_count) + " écrans détectés.\n")

        # Charge autant de fenêtres que besoins
        for screen_index in range(0, self.screen_count):
            application.engine.load('initialisation/graphics/page_rb/page_rb5/screen_index.qml')
            print(len(application.engine.rootObjects()))
            self.screen_list[screen_index] = application.engine.rootObjects()[len(application.engine.rootObjects()) - 1]
            self.screen_list[screen_index].hide()

        # Change les informations sur chaque pages
        for screen_index in range(0, self.screen_count):
            sg = QDesktopWidget().screenGeometry(screen_index).getCoords()
            self.screen_list[screen_index].setPosition(sg[0], sg[1])
            window = self.screen_list[screen_index].findChild(QObject, "screen_index")
            window.setProperty("text", str(screen_index + 1))



        # Définit la page comme complète
        application.is_completed[4] = True

    def on_page_opened(self, application):
        for screen_index in self.screen_list:
            screen_index.show()

    def on_page_closed(self, application):
        for screen_index in self.screen_list:
            screen_index.hide()
