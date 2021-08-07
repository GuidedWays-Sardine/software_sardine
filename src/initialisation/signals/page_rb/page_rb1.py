import logging
import os

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject

class PageRB1:

    def __init__(self, application, page, index, current_button):
        logging.info("page 1 signals")