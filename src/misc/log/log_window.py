# Librairies par défaut
import sys
import os
import logging
import time
import re


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
        """Fonction permettant d'initialiser la partie graphique du module de registre.
        Ouvre en parallèle la connexion avec les fichiers QML pour recevoir leurs messages"""
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

    def __del__(self):
        """Fonction permettant de supprimer la partie graphique du module de registre.
        S'occupe aussi de fermer la connexion avec les fichiers QML pour éviter toute erreur de segmentation"""
        qInstallMessageHandler(None)
        del self

    @decorators.UIupdate
    @decorators.QtSignal(log_level=Level.WARNING, end_process=False)
    def append_log_message(self, message, log_level) -> None:
        """Fonction permettant d'ajouter un message dans le registre. Le message aura le même format que ceux du fichier
        de registres. Si seul des caractères de nouvelles lignes sont envoyés, des lignes vides seront ajoutées

        Parameters
        ----------
        message: `str`
            message à rajouter sur la fenêtre de registre (le format/préfix de registre y sera ajouté)
        log_level: `Level`
            niveau de registre du message (sera affiché que si le niveau de registre est suffisant)
        """
        # Dans le cas où seul des charactères de retour à la ligne ont été envoyés, laisse des lignes vides
        if re.match("/^(\n)\1*$/", message):
            self.insertPlainText(message)
            return

        # combine le message au format de logging et change la date, le niveau et ajoute un caractère de nouvelle ligne:
        message = "\n" + logging.getLogger().handlers[0].formatter._fmt.replace("%(message)s", message)
        message = message.replace("%(asctime)s", time.strftime("%H:%M:%S")).replace("%(levelname)s", str(log_level)[6:])

        # Vérifie si la scrollbar est en bas (dernier message visible)
        is_scrolled_down = self.verticalScrollBar().value() == self.verticalScrollBar().maximum()

        # S'assure que le niveau de registre envoyé est valide et suffisant pour être indiqué dans la fenêtre de logging
        if isinstance(log_level, Level) and log_level in COLORS and log_level.value >= logging.root.level:
            # Change la couleur selon le niveau de registre et le met en gros si : Level.ERROR ou Level.CRITICAL
            self.setTextColor(COLORS[log_level])
            self.setFontWeight(QFont.Bold if log_level.value >= Level.WARNING.value else QFont.Normal)

            # AJoute le message en fin de registre
            self.insertPlainText(message)

            # Si la scrollbar était tout en bas, la redéplace en bas
            if is_scrolled_down:
                self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    @decorators.UIupdate
    @decorators.QtSignal(log_level=Level.WARNING, end_process=False)
    def set_windowed(self):
        """Fonction permettant de rendre la fenêtre de registre fenêtré avec la barre des titres et déplaçable"""
        # Dans le cas où la fenêtre n'est pas déjà en mode fenêtré
        if not (self.windowFlags() & Qt.WindowTitleHint):
            # Détecte si la fenêtre est visible ou non (enlever ou rajouter la barre des titres cachera la fenêtre)
            is_visible = self.isVisible()

            # Récupère la position et taillede la fenêtre (enlever ou rajouter la barre des titres déplacera la fenêtre)
            log_window_settings = {}
            wm.get_window_geometry(self, log_window_settings, "log window")

            # Change les flags
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint |
                                Qt.Dialog | Qt.WindowTitleHint)

            # Redimensionne la fenêtre (elle prendra la même taille et position que précédemment)
            wm.set_window_geometry(self, log_window_settings, "log window", (640, 128))

            # Si la fenêtre était visible la remontre sinon la cache
            if is_visible:
                self.show()
            else:
                self.hide()

    @decorators.UIupdate
    @decorators.QtSignal(log_level=Level.WARNING, end_process=False)
    def set_frameless(self):
        """Fonction permettant de rendre la fenêtre de registre sans cadre sans la barre des titres et indéplaçable"""
        # Dans le cas où la fenêtre n'est pas déjà en mode fenêtré
        if not (self.windowFlags() & Qt.FramelessWindowHint):
            # Détecte si la fenêtre est visible ou non (enlever ou rajouter la barre des titres cachera la fenêtre)
            is_visible = self.isVisible()

            # Récupère la position et taillede la fenêtre (enlever ou rajouter la barre des titres déplacera la fenêtre)
            log_window_settings = {}
            wm.get_window_geometry(self, log_window_settings, "log window")

            # Change les flags
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)

            # Redimensionne la fenêtre (elle prendra la même taille et position que précédemment)
            wm.set_window_geometry(self, log_window_settings, "log window", (640, 128))

            # Si la fenêtre était visible la remontre sinon la cache
            if is_visible:
                self.show()
            else:
                self.hide()


def __initialise_log_window():
    """Fonction (privée) permettant d'initialiser une instance de LogWindow si aucune n'a été initialisée."""
    if QApplication.instance() is not None and not len(INSTANCE):
        INSTANCE.append(LogWindow())
    else:
        from src.misc.log.log import error
        error("Une QApplication doit être initialisé afin de pouvoir générer la fenêtre de logging." +
              "Fenêtre de registre désactivée pour la simulation")


def __add_log_window_message(message, log_level):
    """Fonction (privée) permettant d'ajouter un message de registre sur la fenêtre LogWindow active.
    Si seul des caractères de nouvelles lignes sont envoyés, des lignes vides seront ajoutées.

    Parameters
    ----------
    message: `str`
        message à rajouter sur la fenêtre de registre (le format/préfix de registre y sera ajouté)
    log_level: `Level`
        niveau de registre du message (sera affiché que si le niveau de registre est suffisant)
    """
    # Si le fichier de registre a été initialisé et que la fenêtre est initialisée et activée
    if INSTANCE and logging.getLogger().hasHandlers():
        INSTANCE[0].append_log_message(message, log_level)


def log_window_frameless(visible=None):
    """Fonction permettant de rendre la fenêtre de registre fenêtré avec la barre des titres et déplaçable.

    Parameters
    ----------
    visible: `bool | None`
        Est ce que la visibilité de la fenêtre doit être changée ? (None pour aucune modification sinon changé)
    """
    # Si le fichier registre a été initialisé et que la fenêtre est initialisée et activée
    if INSTANCE and logging.getLogger().hasHandlers():
        INSTANCE[0].set_frameless()

        # Si le mode de visibilité doit être changé, le change
        if visible is not None:
            log_window_visibility(visible)


def log_window_windowed(visible=None):
    """Fonction permettant de rendre la fenêtre de registre sans cadre sans la barre des titres et indéplaçable"
    Si seul des caractères de nouvelles lignes sont envoyés, des lignes vides seront ajoutées.

    Parameters
    ----------
    visible: `bool | None`
        Est ce que la visibilité de la fenêtre doit être changée ? (None pour aucune modification sinon changé)
    """
    # Si le fichier registre a été initialisé et que la fenêtre est initialisée et activée
    if INSTANCE and logging.getLogger().hasHandlers():
        INSTANCE[0].set_windowed()

        # Si le mode de visibilité doit être changé, le change
        if visible is not None:
            log_window_visibility(visible)


@decorators.UIupdate
@decorators.QtSignal(log_level=Level.WARNING, end_process=False)
def log_window_visibility(visible=True) -> None:
    """Fonction permettant de changer la visibilité de la fenêtre.

    Parameters
    ----------
    visible: `bool`
        Indique si la fenêtre doit être visible ou non.
    """
    # Si la fenêtre de registres est initialisée, cache ou montre la fenêtre
    if INSTANCE and visible:
        INSTANCE[0].show()
    elif INSTANCE and not visible:
        INSTANCE[0].hide()


def set_log_window_geometry(settings, key, visible=None):
    """Fonction permettant de redimenssioner la fenêtre de registre.

    Parameters
    ----------
    settings: `sd.SettingsDictionary | dict[str, Any]`
        Dictionaire de paramètres contenant les informations sur la fenêtre. Les paramètres suivant doivent apparaitre :
        key.screen_index, key.x, key.y, key.w, key.h -> avec key le paramètre key envoyé
    key: `str`
        Clé à partir de laquelle, les paramètres écrans seront lus.
    visible: `bool | None`
        Est ce que la visibilité de la fenêtre doit être changée ? (None pour aucune modification sinon changé)

    """
    # redimensionne la fenêtre
    if INSTANCE:
        wm.set_window_geometry(INSTANCE[0], settings, key, (640, 128))

        if visible is not None:
            log_window_visibility(visible)


def get_log_window_geometry(settings, key):
    """Fonction permettant de redimenssioner la fenêtre de registre

    Parameters
    ----------
    settings: `sd.SettingsDictionary | dict`
        Dictionaire de paramètres où les informations seront stockées. Les paramètres seront sous la forme :
        key.screen_index, key.x, key.y, key.w, key.h -> avec key le paramètre key envoyé
    key: `str`
        Clé avec laquelle les dimensions seront enregistrées.
    """
    # Récupère la position de la fenêtre
    if INSTANCE:
        wm.get_window_geometry(INSTANCE[0], settings, key)
