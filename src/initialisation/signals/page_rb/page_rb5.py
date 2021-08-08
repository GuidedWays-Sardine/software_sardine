import logging
import os
import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject




class PageRB5:

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

        # Définit la page comme complète
        application.is_completed[4] = True

