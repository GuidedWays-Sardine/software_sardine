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


# Constantes pour l'état  de la fenêtre du mode immersion
RATIO = 0.6     # Ratio entre la taille de des images/vidéos et de la fenêtre d'immersion
#                 Préférer garder < 0.75 pour ne pas que ça dépasse des écrans en 4:3
LOADING_PATH = "loading.wmv"        # Taille identique à image STILL ; image de fin identique à image STILL
STILL_PATH = "logo.png"
UNLOADING_PATH = "unloading.mov"    # Taille identique à image STILL ; image de début identique à image STILL
BACKGROUND_COLOR = "#000000"        # Il est conseillé de mettre du noir pour simuler un écran éteint
TEXT_COLOR = "#2b2b2b"              # Couleur du texte (version du code principalement), gris foncé de préférence

# Liste des fenêtres pour le mode immersion et des index de fenêtres à sauter
IMMERSION = []
SKIP_LIST = []


class ImmersionMode(Enum):
    """Classe contenant les différents modes pour le module d'immersion"""
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
        raise RuntimeError("Aucune instan ce de <PyQt5.QtWidgets.QApplication> n'a été initialisée")

    # First generate the windows if they aren't generated
    if not IMMERSION:
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
        log.info("Changement du mode immersion en mode fenêtre vide (fond unique et version du logiciel).\n")
    elif new_mode == ImmersionMode.LOADING:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec la vidéo de chargement, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_loading()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion en mode chargement (vidéo de chargement -> logo du simulateur).\n")
    elif new_mode == ImmersionMode.STILL:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec le logo du simulateur centré, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_still()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion en mode simulation (logo du simulateur).\n\n")
    elif new_mode == ImmersionMode.UNLOADING:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec l'animation de fermeture, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_unloading()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion en mode déchargement (vidéo de déchargement -> fenêtre vide).\n")
    else:
        # Cache toutes les fenêtres
        for window in IMMERSION:
            window.set_deactivated()
            log.info("Changement du mode immersion en mode fenêtre vide.\n")


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
    log.info(f"Immersion mode now deactivated for screens {SKIP_LIST}")

    # Change le mode de chargement
    change_mode(new_mode)


class ImmersionWindow(QMainWindow):
    """Classe permettant de générer une fenêtre d'immersion"""
    # Informations sur la position et la taille de la fenêtre
    position = ()
    size = ()

    # Liste des différents composants de la fenêtre
    version = None
    mediaplayer = None
    video = None
    imageviewer = None
    image = None

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
        self.position = position
        self.size = size

        # Commence par la fenêtre en elle-même
        # Tags pour enlever les bordures et rendre la fenêtre incliquable (pour éviter qu'elle cache d'autres modules)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
        # Défini la taille et la position des écran pour remplir l'écran en entire
        self.setGeometry(int(position[0]),
                         int(position[1]),
                         int(size[0]),
                         int(size[1]))
        # Change the background color to the one indicated in the BACKGROUD_COLOR constant
        self.setStyleSheet(f"QMainWindow {{background: '{BACKGROUND_COLOR}';}}")

        # Continue par le joueur de vidéo
        # Crée un joueur de vidéo et une vidéo, et les lies ensemble
        self.mediaplayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self.video = QVideoWidget(self)
        self.mediaplayer.setVideoOutput(self.video)
        # Change la taille et position pour centrer la vidéo et mettre sa taille selon le ration en constante
        width = int(RATIO * size[0])
        height = int(RATIO * size[1])
        self.video.setGeometry(int((size[0] - width)/2),
                               int((size[1] - height)/2),
                               width,
                               height)
        # Cache la vidéo par défaut
        self.video.hide()

        # Continue par l'image du logo (pour le mode still)
        # Crée un regardeur d'image et une image
        self.imageviewer = QLabel(self)
        self.image = QPixmap(f"{PROJECT_DIR}src\\misc\\immersion\\{STILL_PATH}")
        # Change la taille de l'image pour être identique à celle de la vidéo (en prennant en compte le ratio de l'image
        self.imageviewer.setGeometry(QRect(int((size[0] - height * self.image.width() / self.image.height())/2),
                                           int((size[1] - height)/2),
                                           int(height * self.image.width() / self.image.height()),
                                           int(height)))
        self.imageviewer.setPixmap(self.image.scaled(self.imageviewer.size(), Qt.KeepAspectRatio))
        # Cache l'image par défaut
        self.imageviewer.hide()

        # Ajouter un texte avec la version du code dans le coins en bas à droite
        self.version = QLabel(log.VERSION, self)
        self.version.setStyleSheet(f"QLabel {{color : {TEXT_COLOR}; }}")
        self.version.setFont(QFont("Verdana", 12))
        # Le place dans le coins en bas à droite (Le Qt.AlignRight et Qt.AlignBottom ne fonctionnent pas)
        width = self.version.fontMetrics().boundingRect(self.version.text()).width()
        height = self.version.fontMetrics().boundingRect(self.version.text()).height()
        self.version.setGeometry(QRect(size[0] - width, size[1] - height,
                                       width, height))

    def set_loading(self):
        """Fonction permettant de lancer la vidéo de chargement, puis de se mettre en mode ImmersionMode.STILL"""
        # Si la vidéo de chargement n'existe pas, passe directement en mode still
        if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}"):
            self.set_still()
            return

        # Déconnecte tous les signaux du mediaplayer pour éviter d'appeler un signal lors du lancement de la vidéo
        self.mediaplayer.disconnect()

        # Charge la vidéo de chargement, redimenssione le mediaplayer à la vidéo, le monde et lance la vidéo
        self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(f"{PROJECT_DIR}\\src\\misc\\immersion\\{LOADING_PATH}")))
        height = int(RATIO * self.size[1])      # Prend la hauteur comme référence (la largeur dépendra du ratio vidéo)
        self.mediaplayer.setGeometry(QRect(int((self.size[0] - height * self.video.width() / self.video.height())/2),
                                           int((self.size[1] - height)/2),
                                           int(height * self.video.width() / self.video.height()),
                                           int(height)))
        self.video.show()
        self.mediaplayer.play()

        # Connecte le signal de fin de vidéo à la fonction pour faire apparaitre l'image
        self.mediaplayer.stateChanged.connect(self.set_still)

    def set_unloading(self):
        """Fonction permettant de lancer la vidéo de chargement, puis de se mettre en mode ImmersionMode.STILL"""
        # Si la vidéo de déchargement n'existe pas, passe directement en mode empty
        if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}"):
            self.set_empty()
            return

        # Déconnecte tous les signaux du mediaplayer pour éviter d'appeler un signal lors du lancement de la vidéo
        self.mediaplayer.disconnect()

        # Charge la vidéo de déchargement, redimenssione le mediaplayer à la vidéo, le monde et lance la vidéo
        self.mediaplayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(f"{PROJECT_DIR}\\src\\misc\\immersion\\{UNLOADING_PATH}")))
        height = int(RATIO * self.size[1])      # Prend la hauteur comme référence (la largeur dépendra du ratio vidéo)
        self.mediaplayer.setGeometry(QRect(int((self.size[0] - height * self.video.width() / self.video.height()) / 2),
                                           int((self.size[1] - height) / 2),
                                           height * self.video.width() / self.video.height(),
                                           height))
        self.video.show()
        self.mediaplayer.play()

        # Connecte le signal de fin de vidéo à la fonction pour faire apparaitre l'image
        self.mediaplayer.stateChanged.connect(self.set_empty)

    def set_still(self):
        """Fonction permettant de vider la fenêtre d'immersion"""
        # Si le logo n'existe pas, passe en mode empty
        if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{STILL_PATH}"):
            self.set_empty()
            return

        # Arrête la vidéo si elle tourne, cache la vidéo, montre l'image et la fenêtre
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        self.video.hide()
        self.imageviewer.show()
        self.show()

    def set_empty(self):
        """Fonction permettant de vider la fenêtre d'immersion"""
        # Arrête la vidéo si elle tourne, cache la vidéo et l'image et montre la fenêtre
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        self.video.hide()
        self.imageviewer.hide()
        self.show()

    def set_deactivated(self):
        """Fonction permettant de vider la fenêtre d'immersion"""
        # Arrête la vidéo si elle tourne et cache la fenêtre, la vidéo et l'image
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        self.hide()
        self.video.hide()
        self.imageviewer.hide()


def main():
    # Create the application, a thread to do the actions and starts the application
    app = QApplication(sys.argv)
    change_mode(ImmersionMode.EMPTY)

    import threading
    worker = threading.Thread(target = actions)
    worker.start()

    app.exec()


def actions():
    # FIXME : PAS THREAD SAFE!!!!!!!!!!!!!!!!!
    time.sleep(1)
    change_mode(ImmersionMode.STILL)
    time.sleep(1)
    change_skip_list([1], ImmersionMode.EMPTY)
    time.sleep(1)
    change_mode(ImmersionMode.LOADING)


if __name__ == "__main__":
    main()
