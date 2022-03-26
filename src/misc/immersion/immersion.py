# librairies par défaut
import os
import sys
import time
from enum import Enum


# Librairies graphiques
from PyQt5.QtCore import Qt, QRect, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QFont, QPixmap


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.decorators.decorators as decorators


# Constantes pour l'état  de la fenêtre du mode immersion
VOLUME = 0      # Intensité du volume sur une base 100
RATIO = 1    # Ratio entre la taille de des images/vidéos et de la fenêtre d'immersion
#                 Préférer garder < 0.75 pour ne pas que ça dépasse pour les fenêtre en 4:3 (DMI)

LOADING_PATH = "loading.wmv"        # Taille identique à image STILL ; image de fin identique à image STILL
STILL_PATH = "logo.png"
UNLOADING_PATH = "unloading.mov"    # Taille identique à image STILL ; image de début identique à image STILL

BACKGROUND_COLOR = "#000000"        # Il est conseillé de mettre du noir pour simuler un écran éteint
TEXT_COLOR = "#2b2b2b"              # Couleur du texte (version du code principalement), gris foncé de préférence

# Liste des fenêtres pour le mode immersion et des index de fenêtres à sauter
IMMERSION = []
SKIP_LIST = []


class ImmersionMode(Enum):
    """Enum contenant les différents modes pour le module d'immersion"""
    DEACTIVATED = 0
    EMPTY = 1
    LOADING = 2
    STILL = 3
    UNLOADING = 4


def change_mode(new_mode):
    """Fonction permettant de changer le mode du mode immersion.

    Parameters
    ----------
    new_mode: `ImmersionMode`
        DEACTIVATED -> Toutes les fenêtres d'immersion sont cachées. Le mode immersion est désactivé
        EMPTY -> Les fenêtres sont visibles (sauf celles à sauter) avec un fond uni
        LOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de chargement -> mode STILL
        STILL -> Les fenêtres sont visibles (sauf celles à sauter) avec le logo du simulateur au centre
        UNLOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de déchargement -> mode EMPTY

    Raises
    ------
    RuntimeError
        Jeté lorsqu'aucune instance de QApplication n'a été initialisée
    """
    # First verify if an instance of QApplication has been initialised
    if QApplication.instance() is None:
        raise RuntimeError("Aucune instance de <PyQt5.QtWidgets.QApplication> n'a été initialisée")

    # First generate the windows if they aren't generated
    if not IMMERSION:
        # FIXME : trouver un moyen de changer le plugin de lecture pour windows media fountation
        # os.environ["QT_MULTIMEDIA_PREFERRED_PLUGINS"] = "windowsmediafoundation"      # Not working
        initial_time = time.perf_counter()
        for screen_index in range(QDesktopWidget().screenCount()):
            sg = QDesktopWidget().screenGeometry(screen_index).getCoords()
            IMMERSION.append(ImmersionWindow(position=(sg[0], sg[1]),
                                             size=(sg[2] - sg[0] + 1, sg[3] - sg[1] + 1)))

        # Indique le temps de chargement des fenêtre d'immersions
        log.info(f"Initialisation de {len(IMMERSION)} fenêtres d'immersions en " +
                 f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.")

        # Indique pour l'image et les vidéos de chargement/déchargement si le chemin indiqué est valide
        if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{STILL_PATH}"):
            log.warning(f"image statique du module immersion introuvable:\n\t" +
                        f"{PROJECT_DIR}src\\misc\\immersion\\{STILL_PATH}")
        if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}"):
            log.warning(f"vidéo de chargement du module immersion introuvable:\n\t" +
                        f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}")
        if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}"):
            log.warning(f"vidéo de déchargement du module immersion introuvable:\n\t" +
                        f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}")

    # Now find what immersion mode was sent and change the behavior of the immersion mode depending on it
    if new_mode == ImmersionMode.EMPTY:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, sans video, ni image, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_empty()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode fenêtres vides (fond unique et version du logiciel).\n")
    elif new_mode == ImmersionMode.LOADING:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec la vidéo de chargement, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_loading()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode chargement (vidéo de chargement -> logo du simulateur).\n")
    elif new_mode == ImmersionMode.STILL:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec le logo du simulateur centré, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_still()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode simulation (logo du simulateur).\n")
    elif new_mode == ImmersionMode.UNLOADING:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec l'animation de fermeture, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_unloading()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode déchargement (vidéo de déchargement -> fenêtre vide).\n")
    else:
        # Cache toutes les fenêtres
        for window in IMMERSION:
            window.set_deactivated()
            log.info("Changement du mode immersion : mode désactivé.\n")


def change_skip_list(skip_list=(), new_mode=ImmersionMode.EMPTY):
    """Fonction permettant de rajouter des écrans à désactiver (et donc à sauter)

    Parameters
    ----------
    skip_list: `tuple | list`
        Liste des écrans à sauter (de 0 à Nécrans - 1). Par défaut aucun
    new_mode: `ImmersionMode`
        DEACTIVATED -> Toutes les fenêtres d'immersion sont cachées. Le mode immersion est désactivé
        EMPTY -> Les fenêtres sont visibles (sauf celles à sauter) avec un fond uni
        LOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de chargement -> mode STILL
        STILL -> Les fenêtres sont visibles (sauf celles à sauter) avec le logo du simulateur au centre
        UNLOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de déchargement -> mode EMPTY
    """
    # Réinitialise la liste des SKIP_LIST et rajoute chacun des index écrans
    SKIP_LIST.clear()
    for i in skip_list:
        SKIP_LIST.append(int(i))
    log.info(f"Mode immersion désactivé pour les écrans : {tuple(index + 1 for index in SKIP_LIST)}")

    # Change le mode de chargement
    change_mode(new_mode)


class ImmersionWindow(QMainWindow):
    """Classe permettant de générer une fenêtre d'immersion"""
    # Liste des différents composants de la fenêtre
    __version_text = None

    __load_mediaplayer = None
    __load_video = None

    __unload_mediaplayer = None
    __unload_video = None

    __imageviewer = None
    __image = None

    def __init__(self, position, size):
        """Fonction permettant d'initialiser une fenêtre d'immersion

        Parameters
        ----------
        position: `tuple`
            Liste des positions de la fenêtre (x, y)
        size: `tuple`
            Liste des dimensions de la fenêtre (w, h)
            """
        # Initialise la fenêtre
        super().__init__()
        self.hide()

        # Commence par la fenêtre en elle-même
        # Tags pour enlever les bordures et rendre la fenêtre incliquable (pour éviter qu'elle cache d'autres modules)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
        # Défini la taille et la position des écran pour remplir l'écran en entire
        height = int(RATIO * size[1])
        self.setGeometry(int(position[0]),
                         int(position[1]),
                         int(size[0]),
                         int(size[1]))
        # Change the background color to the one indicated in the BACKGROUD_COLOR constant
        self.setStyleSheet(f"QMainWindow {{background: '{BACKGROUND_COLOR}';}}")

        # Continue par le joueur de vidéo de chargement (si la vidéo de chargement est trouvée)
        if os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}"):
            # Crée un joueur de vidéo et une vidéo, et les lies ensemble
            self.__load_mediaplayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)
            self.__load_video = QVideoWidget(self)
            self.__load_mediaplayer.setVideoOutput(self.__load_video)
            # Change la taille et position pour centrer la vidéo et mettre sa taille selon le ration en constante
            video_ratio = self.__load_video.width() / self.__load_video.height()
            self.__load_video.setGeometry(QRect(int((size[0] - height * video_ratio) / 2),
                                                int((size[1] - height) / 2),
                                                int(height * video_ratio),
                                                int(height)))
            # Change la vidéo pour la vidéo de chargement
            self.__load_mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(f"{PROJECT_DIR}\\src\\misc\\immersion\\{LOADING_PATH}")))
            # Définit le volume du son comme celui indiqué
            self.__load_mediaplayer.setVolume(min(max(VOLUME, 0), 100))
            # Cache la vidéo par défaut
            self.__load_video.hide()

        # Continue par le joueur de vidéo de fermeture (si la vidéo de fermeture est trouvée)
        if os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}"):
            # Crée un joueur de vidéo et une vidéo, et les lies ensemble
            self.__unload_mediaplayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)
            self.__unload_video = QVideoWidget(self)
            self.__unload_mediaplayer.setVideoOutput(self.__unload_video)
            # Change la taille et position pour centrer la vidéo et mettre sa taille selon le ration en constante
            video_ratio = self.__unload_video.width() / self.__unload_video.height()
            self.__unload_video.setGeometry(QRect(int((size[0] - height * video_ratio) / 2),
                                                  int((size[1] - height) / 2),
                                                  int(height * video_ratio),
                                                  int(height)))
            # Change la vidéo pour la vidéo de chargement
            self.__unload_mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(f"{PROJECT_DIR}\\src\\misc\\immersion\\{UNLOADING_PATH}")))
            # Définit le volume du son comme celui indiqué
            self.__unload_mediaplayer.setVolume(min(max(VOLUME, 0), 100))
            # Cache la vidéo par défaut
            self.__unload_video.hide()

        # Continue par l'image du logo (pour le mode still) si l'image existe
        if os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{STILL_PATH}"):
            # Crée un regardeur d'image et une image
            self.__imageviewer = QLabel(self)
            self.__image = QPixmap(f"{PROJECT_DIR}src\\misc\\immersion\\{STILL_PATH}")
            # Change la taille de l'image pour être identique à celle de la vidéo
            self.__imageviewer.setGeometry(QRect(int((size[0] - height * self.__image.width() / self.__image.height())/2),
                                                 int((size[1] - height)/2),
                                                 int(height * self.__image.width() / self.__image.height()),
                                                 int(height)))
            self.__imageviewer.setPixmap(self.__image.scaled(self.__imageviewer.size(), Qt.KeepAspectRatio))
            # Cache l'image par défaut
            self.__imageviewer.hide()

            # Ajouter un texte avec la version du code dans le coins en bas à droite
            self.__version_text = QLabel(log.VERSION, self)
            self.__version_text.setStyleSheet(f"QLabel {{color : {TEXT_COLOR}; }}")
            self.__version_text.setFont(QFont("Verdana", 12))
            # Le place dans le coins en bas à droite (Le Qt.AlignRight et Qt.AlignBottom ne fonctionnent pas)
            width = self.__version_text.fontMetrics().boundingRect(self.__version_text.text()).width()
            height = self.__version_text.fontMetrics().boundingRect(self.__version_text.text()).height()
            self.__version_text.setGeometry(QRect(size[0] - width, size[1] - height,
                                                  width, height))

    @decorators.UIupdate
    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def set_loading(self):
        """Fonction permettant de lancer la vidéo de chargement, puis de se mettre en mode ImmersionMode.STILL"""
        # Si la vidéo de chargement n'existe pas, passe directement en mode still
        if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}"):
            self.set_still()
            return

        # Cache toutes vidéos et images et joue la vidéo de chargement
        if self.__load_mediaplayer is not None:
            self.__load_mediaplayer.stop()
            self.__load_video.show()
            self.__load_mediaplayer.play()
        if self.__unload_mediaplayer is not None:
            self.__unload_video.hide()
            self.__unload_mediaplayer.stop()
        if self.__image is not None:
            self.__imageviewer.hide()
        self.show()

    @decorators.UIupdate
    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def set_unloading(self):
        """Fonction permettant de lancer la vidéo de chargement, puis de se mettre en mode ImmersionMode.STILL"""
        # Si la vidéo de déchargement n'existe pas, passe directement en mode empty
        if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}"):
            self.set_empty()
            return

        # Cache toutes vidéos et images et joue la vidéo de déchargement
        if self.__unload_mediaplayer is not None:
            self.__unload_mediaplayer.stop()
            self.__unload_video.show()
            self.__unload_mediaplayer.play()
        if self.__load_mediaplayer is not None:
            self.__load_video.hide()
            self.__load_mediaplayer.stop()
        if self.__image is not None:
            self.__imageviewer.hide()
        self.show()

    @decorators.UIupdate
    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def set_still(self):
        """Fonction permettant de vider la fenêtre d'immersion"""
        # Si le logo n'existe pas, passe en mode empty
        if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{STILL_PATH}"):
            self.set_empty()
            return

        # Arrête les vidéo si elles tourne, cache les vidéo, montre l'image et la fenêtre
        if self.__load_mediaplayer is not None:
            self.__load_video.hide()
            self.__load_mediaplayer.stop()
        if self.__unload_mediaplayer is not None:
            self.__unload_video.hide()
            self.__unload_mediaplayer.stop()
        if self.__image is not None:
            self.__imageviewer.show()
        self.show()

    @decorators.UIupdate
    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def set_empty(self):
        """Fonction permettant de vider la fenêtre d'immersion"""
        # Arrête la vidéo si elle tourne, cache la vidéo et l'image et montre la fenêtre
        if self.__load_mediaplayer is not None:
            self.__load_video.hide()
            self.__load_mediaplayer.stop()
        if self.__unload_mediaplayer is not None:
            self.__unload_video.hide()
            self.__unload_mediaplayer.stop()
        if self.__image is not None:
            self.__imageviewer.hide()
        self.show()

    @decorators.UIupdate
    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def set_deactivated(self):
        """Fonction permettant de vider la fenêtre d'immersion"""
        # Arrête la vidéo si elle tourne et cache la fenêtre, la vidéo et l'image
        if self.__load_mediaplayer is not None:
            self.__load_video.hide()
            self.__load_mediaplayer.stop()
        if self.__unload_mediaplayer is not None:
            self.__unload_video.hide()
            self.__unload_video.stop()
        if self.__image is not None:
            self.__imageviewer.hide()
        self.hide()


def main():
    # Create the application, a thread to do the actions and starts the application
    log.initialise(save = False)
    app = QApplication(sys.argv)
    change_mode(ImmersionMode.EMPTY)

    import threading
    worker_thread = threading.Thread(target=worker)
    worker_thread.start()

    app.exec()


def worker():
    change_mode(ImmersionMode.LOADING)
    time.sleep(7)
    change_mode(ImmersionMode.STILL)
    time.sleep(3)
    change_skip_list((1,), ImmersionMode.UNLOADING)
    time.sleep(4)
    change_mode(ImmersionMode.EMPTY)
    time.sleep(3)
    change_mode(ImmersionMode.DEACTIVATED)
    time.sleep(3)
    exit(1)


if __name__ == "__main__":
    main()
