# librairies par défaut
import os
import sys
import time
from enum import Enum
from functools import lru_cache
import threading


# Librairies graphiques
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import cv2 as cv


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.window_manager as wm
from src.misc.immersion.immersion_window import ImmersionWindow, LOADING_PATH, STILL_PATH, UNLOADING_PATH
import src.misc.decorators as decorators


# Liste des fenêtres pour le mode immersion et des index de fenêtres à sauter
IMMERSION = []
SKIP_LIST = []      # Index de 0 à Nécrans - 1


class Mode(Enum):
    """Enum contenant les différents modes pour le module d'immersion"""
    DEACTIVATED = 0
    EMPTY = 1
    LOADING = 2
    STILL = 3
    UNLOADING = 4


@decorators.UniqueCall
def initialise_immersion_windows() -> None:
    """Initialise toutes les fenêtres d'immersion"""
    initial_time = time.perf_counter()
    try:
        # Initialise chacune des fenêtres (selon le nombre, la taille et la position des écrans)
        for screen_index in range(1, wm.screens_count() + 1):
            IMMERSION.append(ImmersionWindow(position=wm.get_screen(screen_index)[0],
                                             size=wm.get_screen(screen_index)[1]))
    except Exception as error:
        # Si une erreur est trouvé lors de l'initialisation du module immersion, laisse un message de registre
        log.error("Erreur lors de l'initialisation des fenêtres d'imersion. Module désactivé pour la simulation.",
                  exception=error, prefix="Chargement module immersion")
        IMMERSION.clear()
    else:
        # Si les fenêtres ont été chargées correctement,indique le temps de chargement des fenêtre d'immersion
        log.info(f"Initialisation de {len(IMMERSION)} fenêtre{'s' * (len(IMMERSION) > 1)} d'immersion en " +
                 f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.",
                 prefix="Chargement module immersion")

    # Indique pour l'image et les vidéos de chargement/déchargement si le chemin indiqué est valide
    if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{STILL_PATH}"):
        log.warning(f"image statique du module immersion introuvable:\n\t" +
                    f"{PROJECT_DIR}src\\misc\\immersion\\{STILL_PATH}", prefix="Chargement module immersion")
    if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}"):
        log.warning(f"vidéo de chargement du module immersion introuvable:\n\t" +
                    f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}", prefix="Chargement module immersion")
    if not os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}"):
        log.warning(f"vidéo de déchargement du module immersion introuvable:\n\t" +
                    f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}", prefix="Chargement module immersion")


def change_mode(new_mode, function=None) -> None:
    """Fonction permettant de changer le mode du mode immersion.

    Parameters
    ----------
    new_mode: `Mode`
        DEACTIVATED -> Toutes les fenêtres d'immersion sont cachées. Le mode immersion est désactivé ;
        EMPTY -> Les fenêtres sont visibles (sauf celles à sauter) avec un fond uni ;
        LOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de chargement -> mode STILL ;
        STILL -> Les fenêtres sont visibles (sauf celles à sauter) avec le logo du simulateur au centre ;
        UNLOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de déchargement -> mode EMPTY ;
    function: `function | None`
        Fonction à executer en arrière plan dans le cas du mode chargement/déchargement afin d'optimiser le simulateur.
        Sort dés que la vidéo de chargement/déchargement ET la fonction ont finis.
        La fonction sera executé dans un thread parrallèle. Attention au data races et à aux composants graphiques.
        Les arguments doivent être inclus directement dans la fonction envoyer (utiliser un lambda si nécessaire)

    Raises
    ------
    RuntimeError
        Jetée lorsqu'aucune instance de QApplication n'a été initialisée.
    """
    # First verify if an instance of QApplication has been initialised
    if QApplication.instance() is None:
        raise RuntimeError("Aucune instance de <PyQt5.QtWidgets.QApplication> n'a été initialisée.")

    # First generate the windows if they aren't generated
    if not IMMERSION:
        initialise_immersion_windows()

    # Now find what immersion mode was sent and change the behavior of the immersion mode depending on it
    if new_mode == Mode.EMPTY:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, sans video, ni image, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_empty()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode fenêtres vides (fond unique et version du logiciel).",
                 prefix="Module immersion")
    elif new_mode == Mode.LOADING:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec la vidéo de chargement, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_loading()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode chargement (vidéo de chargement -> logo du simulateur).",
                 prefix="Module immersion")
    elif new_mode == Mode.STILL:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec le logo du simulateur centré, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_still()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode simulation (logo du simulateur).",
                 prefix="Module immersion")
    elif new_mode == Mode.UNLOADING:
        # Montre toutes les fenêtres qui ne sont pas dans la skiplist, avec l'animation de fermeture, sinon la cache
        for i, window in enumerate(IMMERSION):
            if i not in SKIP_LIST:
                window.set_unloading()
            else:
                window.set_deactivated()
        log.info("Changement du mode immersion : mode déchargement (vidéo de déchargement -> fenêtre vide).",
                 prefix="Module immersion")
    else:
        # Cache toutes les fenêtres
        for window in IMMERSION:
            window.set_deactivated()
        log.info("Changement du mode immersion : mode désactivé.",
                 prefix="Module immersion")

    # Si la fonction est appelée dans le thread principal, execute l'application pendant 5ms pour mettre à jour le mode
    # Attention, cela ne marche que pour les modes DEACTIVATED, EMPTY et STILL
    if threading.current_thread().__class__.__name__ == '_MainThread' and \
            new_mode in (Mode.DEACTIVATED, Mode.EMPTY, Mode.STILL):
        QTimer.singleShot(5, lambda: QApplication.instance().quit())
        QApplication.instance().exec()
    # Si le mode mode loading/unloading est détecté, que le thread est le thread principal, que la vidéo existe,
    # met en pause l'application le temps de la vidéo de (dé)chargement et execute la fonction envoyée en fond si existe
    if threading.current_thread().__class__.__name__ == "_MainThread" and \
            ((new_mode == Mode.LOADING and os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}")) or
             (new_mode == Mode.UNLOADING and os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}"))):
        # Récupère le temps de la vidéo de chargement/déchargement
        video_time = loading_duration() if new_mode == Mode.LOADING else unloading_duration()

        # Si aucune fonction n'a été envoyée, ou que le type n'est pas bon, laisse un message de warning
        # Et execute l'application le temps qu'il faut pour jouer la vidéo entièrement
        if "__call__" not in dir():
            # Si aucune fonction n'a été envoyée
            if function is None:
                log.warning(f"Aucune fonction envoyée lors de la vidéo de {'dé' if new_mode == Mode.UNLOADING else ''}" +
                            f"chargement. Application mise en pause pour {video_time * 1000} secondes.")
            # Si quelque chose a été envoyée mais qu'elle ne peut pas être appelée (__call__ manquant)
            else:
                log.warning(f"L'object \"{function}\" ne peut pas être appelée. Application mise en pause pour " +
                            f"{video_time * 1000} pour la vidéo de {'dé' if new_mode == Mode.UNLOADING else ''}chargement.")

            # Execute l'application pendant le temps nécessaire
            QTimer.singleShot(video_time, lambda: QApplication.instance().quit())
            QApplication.instance().exec()
        # Si une fonction appelable a été envoyée, execute la fonction dans un thread parallèle et lance la vidéo
        else:
            worker_thread = threading.Thread(target=function)
            worker_thread.start()
            QTimer.singleShot(video_time, lambda: QApplication.instance().quit())
            QApplication.instance().exec()
            worker_thread.join()


def change_skip_list(skip_list=(), new_mode=Mode.EMPTY, function=None) -> None:
    """Fonction permettant de rajouter des écrans à désactiver (et donc à sauter).

    Parameters
    ----------
    skip_list: `tuple[int] | list[int]`
        Liste des écrans à sauter (de 1 à Nécrans). Par défaut aucun ;
    new_mode: `Mode`
        DEACTIVATED -> Toutes les fenêtres d'immersion sont cachées. Le mode immersion est désactivé ;
        EMPTY -> Les fenêtres sont visibles (sauf celles à sauter) avec un fond uni ;
        LOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de chargement -> mode STILL ;
        STILL -> Les fenêtres sont visibles (sauf celles à sauter) avec le logo du simulateur au centre ;
        UNLOADING -> Les fenêtres sont visibles (sauf celles à sauter) avec l'animation de déchargement -> mode EMPTY ;
    function: `function | None`
        Fonction à executer en arrière plan dans le cas du mode chargement/déchargement afin d'optimiser le simulateur.
        Sort dés que la vidéo de chargement/déchargement ET la fonction ont finis.
        La fonction sera executé dans un thread parrallèle. Attention au data races et à aux composants graphiques.
        Les arguments doivent être inclus directement dans la fonction envoyer (utiliser un lambda si nécessaire)
    """
    # Réinitialise la liste des SKIP_LIST et rajoute chacun des index écrans
    SKIP_LIST.clear()
    for i in (s_l for s_l in skip_list if s_l <= wm.screens_count()):
        SKIP_LIST.append(int(i) - 1)

    # Indique pour quels écrans le module d'immersion a été désactivé
    if not SKIP_LIST:
        log.info("Mode immersion activé pour tous les écrans.", prefix="Module immersion")
    elif len(SKIP_LIST) == 1:
        log.info(f"Mode immersion désactivé pour l\'écran : {SKIP_LIST[0]}", prefix="Module immersion")
    else:
        log.info(f"Mode immersion désactivé pour les écrans : {[i + 1 for i in SKIP_LIST]}", prefix="Module immersion")

    # Change le mode de chargement
    change_mode(new_mode)


@lru_cache(maxsize=1)
def loading_duration():
    """Récupère la durée de la vidéo de chargement.

    Returns
    -------
    loading_duration: `int`
        Durée de la vidéo (0 si la vidéo n'existe pas) en millisecondes.
    """
    if os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}"):
        cap = cv.VideoCapture(f"{PROJECT_DIR}src\\misc\\immersion\\{LOADING_PATH}")
        return int(cap.get(cv.CAP_PROP_FRAME_COUNT) / cap.get(cv.CAP_PROP_FPS) * 1000)
    else:
        return 0


@lru_cache(maxsize=1)
def unloading_duration():
    """Récupère la durée de la vidéo de déchargement.

    Returns
    -------
    loading_duration: `int`
        Durée de la vidéo (0 si la vidéo n'existe pas) en millisecondes.
    """
    if os.path.isfile(f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}"):
        cap = cv.VideoCapture(f"{PROJECT_DIR}src\\misc\\immersion\\{UNLOADING_PATH}")
        return int(cap.get(cv.CAP_PROP_FRAME_COUNT) / cap.get(cv.CAP_PROP_FPS) * 1000)
    else:
        return 0
