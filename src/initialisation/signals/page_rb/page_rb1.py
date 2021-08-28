import logging
import os

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject

class PageRB1:

    index = 1   # Attention dans les tableaux l'index comment à 0 donc index_tab = index - 1
    page = None
    current_button = None

    def __init__(self, application, page, index, current_button):
        self.index = index
        self.page = page
        self.current_button = current_button

        application.is_completed[0] = True
