# librairies par défaut
import os
import sys
import time
from enum import Enum
from functools import lru_cache


# Librairies graphiques
from PyQt5.QtWidgets import QApplication
import cv2 as cv


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.window_manager as wm
from src.misc.immersion.immersion_window import ImmersionWindow, LOADING_PATH, STILL_PATH, UNLOADING_PATH


# Liste des fenêtres pour le mode immersion et des index de fenêtres à sauter
IMMERSION = []
SKIP_LIST = []


class Mode(Enum):
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
    new_mode: `Mode`
        DEACTIVATED -> Toutes les fenêtres d'immersion sont cachées. Le mode immersion est désactivé
        EMPTY -> Les fenêtres sont visibles (sauf celles à sauter) avec un fond uni
        LOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de chargement -> mode STILL
        STILL -> Les fenêtres sont visibles (sauf celles à sauter) avec le logo du simulateur au centre
        UNLOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de déchargement -> mode EMPTY

    Raises
    ------
    RuntimeError
        Jetée lorsqu'aucune instance de QApplication n'a été initialisée
    """
    # First verify if an instance of QApplication has been initialised
    if QApplication.instance() is None:
        raise RuntimeError("Aucune instance de <PyQt5.QtWidgets.QApplication> n'a été initialisée")

    # First generate the windows if they aren't generated
    if not IMMERSION:
        # FIXME : trouver un moyen de changer le plugin de lecture pour windows media fountation
        # os.environ["QT_MULTIMEDIA_PREFERRED_PLUGINS"] = "windowsmediafoundation"      # Not working
        initial_time = time.perf_counter()
        for screen_index in range(1, wm.screens_count() + 1):
            IMMERSION.append(ImmersionWindow(position=wm.get_screen(screen_index)[0],
                                             size=wm.get_screen(screen_index)[1]))

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
    if new_mode == Mode.EMPTY:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, sans video, ni image, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_empty()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode fenêtres vides (fond unique et version du logiciel).\n")
    elif new_mode == Mode.LOADING:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec la vidéo de chargement, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_loading()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode chargement (vidéo de chargement -> logo du simulateur).\n")
    elif new_mode == Mode.STILL:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec le logo du simulateur centré, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_still()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode simulation (logo du simulateur).\n")
    elif new_mode == Mode.UNLOADING:
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


def change_skip_list(skip_list=(), new_mode=Mode.EMPTY):
    """Fonction permettant de rajouter des écrans à désactiver (et donc à sauter)

    Parameters
    ----------
    skip_list: `tuple[int] | list[int]`
        Liste des écrans à sauter (de 1 à Nécrans). Par défaut aucun
    new_mode: `Mode`
        DEACTIVATED -> Toutes les fenêtres d'immersion sont cachées. Le mode immersion est désactivé
        EMPTY -> Les fenêtres sont visibles (sauf celles à sauter) avec un fond uni
        LOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de chargement -> mode STILL
        STILL -> Les fenêtres sont visibles (sauf celles à sauter) avec le logo du simulateur au centre
        UNLOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de déchargement -> mode EMPTY
    """
    # Réinitialise la liste des SKIP_LIST et rajoute chacun des index écrans
    SKIP_LIST.clear()
    for i in skip_list:
        SKIP_LIST.append(int(i) - 1)
    log.info(f"Mode immersion désactivé pour les écrans : {tuple(index + 1 for index in SKIP_LIST)}")

    # Change le mode de chargement
    change_mode(new_mode)


@lru_cache(maxsize=1)
def loading_duration():
    """Fonction permettant de connaitre la durée de la vidéo de chargement

    Returns
    -------
    loading_duration: `float`
        Durée de la vidéo (0 if video is not found)
    """
    if os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}"):
        cap = cv.VideoCapture(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}")
        return cap.get(cv.CAP_PROP_FRAME_COUNT) / cap.get(cv.CAP_PROP_FPS)
    else:
        return 0.0


@lru_cache(maxsize=1)
def unloading_duration():
    """Fonction permettant de connaitre la durée de la vidéo de chargement

    Returns
    -------
    loading_duration: `float`
        Durée de la vidéo (0 if video is not found)
    """
    if os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}"):
        cap = cv.VideoCapture(f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}")
        return cap.get(cv.CAP_PROP_FRAME_COUNT) / cap.get(cv.CAP_PROP_FPS)
    else:
        return 0.0
