# Librairies par défaut
import sys
import os
import logging
import time


# Librairies graphiques
from PyQt5.QtWidgets import QTextEdit, QScrollBar, QApplication, QFrame
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, qInstallMessageHandler

# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
from src.misc.log.log_levels import Level
import src.misc.decorators as decorators
import src.misc.window_manager as wm


CRITICAL_COLOR = "#a94826"
ERROR_COLOR = "#ff4844"
WARNING_COLOR = "#cb772f"
INFO_COLOR = "#a9b7c6"
DEBUG_COLOR = "#808080"
BACKGROUND_COLOR = "#2b2b2b"


COLORS = {Level.CRITICAL: QColor(CRITICAL_COLOR),
          Level.ERROR: QColor(ERROR_COLOR),
          Level.WARNING: QColor(WARNING_COLOR),
          Level.INFO: QColor(INFO_COLOR),
          Level.DEBUG: QColor(DEBUG_COLOR)}


INSTANCE = []


class LogWindow(QTextEdit):
    __scrollbar = None
    __font = None

    def __init__(self):
        # Initialiser le QTextEdit (qui apparaitra dans une fenêtre)
        super().__init__()

        # Defines default tags and hides the window
        self.setMinimumSize(640, 128)
        self.setWindowTitle("Fenêtre de registre")
        self.setStyleSheet(f"background: {BACKGROUND_COLOR}; ")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint |
                            Qt.Dialog | Qt.WindowTitleHint)     # Par défaut : en fenêtré
        self.setFrameStyle(QFrame.NoFrame)
        self.setTextInteractionFlags(Qt.NoTextInteraction)

        # Change the scrollbar to be slimmer and with correct colors
        self.__scrollbar = QScrollBar()
        self.__scrollbar.setStyleSheet("width: 8;")
        self.setVerticalScrollBar(self.__scrollbar)

        # Change la taille et la police d'écriture
        self.__font = QFont()
        self.__font.setPixelSize(16)
        self.__font.setFamily("Courier")
        self.setFont(self.__font)

        # Indique la fonction a appeler lorsqu'une fonction est initialisée
        from src.misc.log.log import _qt_message_handler
        os.environ["QT_DEBUG_PLUGINS"] = "1"
        qInstallMessageHandler(_qt_message_handler)

        # Cache la fenêtre
        self.hide()

    @decorators.UIupdate
    @decorators.QtSignal(log_level=Level.WARNING, end_process=False)
    def append_log_message(self, message, log_level):
        # combine le messafe au format de logging et change la date, le niveau et ajoute un caractère de nouvelle ligne:
        message = logging.getLogger().handlers[0].formatter._fmt.replace("%(message)s", message) + "\n"
        message = message.replace("%(asctime)s", time.strftime("%H:%M:%S")).replace("%(levelname)s", str(log_level)[6:])

        # S'assure que le niveau de registre envoyé est valide et suffisant pour être indiqué dans la fenêtre de logging
        if isinstance(log_level, Level) and log_level in COLORS and log_level.value >= logging.root.level:
            # Change la couleur selon le niveau de registre et le met en gros si : Level.ERROR ou Level.CRITICAL
            self.setTextColor(COLORS[log_level])
            self.setFontWeight(QFont.Bold if log_level.value >= Level.WARNING.value else QFont.Normal)

            # AJoute le message en fin de registre
            self.insertPlainText(message)

    @decorators.UIupdate
    @decorators.QtSignal(log_level=Level.WARNING, end_process=False)
    def set_windowed(self):
        # Dans le cas où la fenêtre n'est pas déjà en mode fenêtré
        if not (self.windowFlags() & Qt.WindowTitleHint):
            # Détecte si la fenêtre est visible ou non (enlever ou rajouter la barre des titres cachera la fenêtre)
            is_visible = self.isVisible()

            # Récupère la position et taillede la fenêtre (enlever ou rajouter la barre des titres déplacera la fenêtre)
            log_window_settings = {}
            wm.get_window_position(self, log_window_settings, "log window")

            # Change les flags
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint |
                                Qt.Dialog | Qt.WindowTitleHint)

            # Redimensionne la fenêtre (elle prendra la même taille et position que précédemment)
            wm.set_window_position(self, log_window_settings, "log window", (640, 128))

            # Si la fenêtre était visible la remontre sinon la cache
            if is_visible:
                self.show()
            else:
                self.hide()

    @decorators.UIupdate
    @decorators.QtSignal(log_level=Level.WARNING, end_process=False)
    def set_frameless(self):
        # Dans le cas où la fenêtre n'est pas déjà en mode fenêtré
        if not (self.windowFlags() & Qt.FramelessWindowHint):
            # Détecte si la fenêtre est visible ou non (enlever ou rajouter la barre des titres cachera la fenêtre)
            is_visible = self.isVisible()

            # Récupère la position et taillede la fenêtre (enlever ou rajouter la barre des titres déplacera la fenêtre)
            log_window_settings = {}
            wm.get_window_position(self, log_window_settings, "log window")

            # Change les flags
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)

            # Redimensionne la fenêtre (elle prendra la même taille et position que précédemment)
            wm.set_window_position(self, log_window_settings, "log window", (640, 128))

            # Si la fenêtre était visible la remontre sinon la cache
            if is_visible:
                self.show()
            else:
                self.hide()

    def __del__(self):
        qInstallMessageHandler(None)
        del self


def __initialise_log_window():
    if QApplication.instance() is not None and not len(INSTANCE):
        INSTANCE.append(LogWindow())
    else:
        from src.misc.log.log import warning
        warning("Une QApplication doit être initialisé afin de pouvoir générer la fenêtre de logging." +
                "Fenêtre de registre désactivée pour la simulation")


def add_log_window_message(message, log_level):
    # Si la fenêtre de registre n'a pas été initialisée, tente de l'initialiser
    if not INSTANCE:
        __initialise_log_window()

    # Si le fichier de registre a été initialisé et que la fenêtre est initialisée et activée
    if INSTANCE and logging.getLogger().hasHandlers():
        INSTANCE[0].append_log_message(message, log_level)


def set_log_window_frameless(visible=None):
    # Si la fenêtre de registre n'a pas été initialisée, tente de l'initialiser
    if not INSTANCE:
        __initialise_log_window()

    # Si le fichier registre a été initialisé et que la fenêtre est initialisée et activée
    if INSTANCE and logging.getLogger().hasHandlers():
        INSTANCE[0].set_frameless()

        # Si le mode de visibilité doit être changé, le change
        if visible is not None:
            change_log_window_visibility(visible)


def set_log_window_windowed(visible=None):
    # Si la fenêtre de registre n'a pas été initialisée, tente de l'initialiser
    if not INSTANCE:
        __initialise_log_window()

    # Si le fichier registre a été initialisé et que la fenêtre est initialisée et activée
    if INSTANCE and logging.getLogger().hasHandlers():
        INSTANCE[0].set_frameless()

        # Si le mode de visibilité doit être changé, le change
        if visible is not None:
            change_log_window_visibility(visible)


@decorators.UIupdate
@decorators.QtSignal(log_level=Level.WARNING, end_process=False)
def change_log_window_visibility(visible=True):
    # Si la fenêtre de registre n'a pas été initialisée, tente de l'initialiser
    if not INSTANCE:
        __initialise_log_window()

    # Si la fenêtre de registres est initialisée, cache ou montre la fenêtre
    if INSTANCE and visible:
        INSTANCE[0].show()
    elif INSTANCE and not visible:
        INSTANCE[0].hide()


def resize_log_window(settings, key, visible=None):
    # Si la fenêtre de registre n'a pas été initialisée, tente de l'initialiser
    if not INSTANCE:
        __initialise_log_window()

    # redimensionne la fenêtre
    if INSTANCE:
        wm.set_window_position(INSTANCE[0], settings, key, (640, 128))

        if visible is not None:
            change_log_window_visibility(visible)


def get_log_window_settings(settings, key):
    # Si la fenêtre de registre n'a pas été initialisée, tente de l'initialiser
    if not INSTANCE:
        __initialise_log_window()

    # Récupère la position de la fenêtre
    if INSTANCE:
        wm.get_window_position(INSTANCE[0], settings, key)
