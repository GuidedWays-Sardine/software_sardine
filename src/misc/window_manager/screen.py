# Librairies par défaut
import os
import sys
import functools


# Librairies graphiques
from PyQt5.QtWidgets import QApplication, QDesktopWidget


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log


@functools.lru_cache(maxsize=1)
def screens_list():
    """Récupère les informations sur tous les écrans détectés (position et taille).

    Returns
    -------
    screens_informations: `tuple[tuple[tuple[int, int], tuple[int, int]]]`
        Information sur les écrans, indiquant leur position et taille : format : (((x, y), (w, h)), ...).

    Raises
    ------
    RuntimeError :
        Jetée si l'appel de la fonction se fait avant l'initialisation du QApplication (nécessaire).
    """
    # Vérifie qu'un QApplication a déjà été généré (vital à la récupération des écrans)
    if QApplication.instance() is None:
        raise RuntimeError("Le QApplication doit être initialisé pour permettre la récupération de la liste des écrans")

    screens_geometry = []
    # Charge tous les écrans connectés à l'ordinateur (utile pour la positionnement de certaines popup)
    for screen_index in range(0, QDesktopWidget().screenCount()):
        # Charge les informations de l'écran (au format [x_min, y_min, x_max, y_max]
        sg = QDesktopWidget().screenGeometry(screen_index).getCoords()

        # Les stockes au bon format ((x, y), (w, h))
        screens_geometry.append(((sg[0], sg[1]), (sg[2] - sg[0] + 1, sg[3] - sg[1] + 1)))

    log.info(f"Détection de {len(screens_geometry)} écran{'s' * (len(screens_geometry) > 1)} sur l'ordinateur.")
    return tuple(screens_geometry)


@functools.lru_cache(maxsize=1)
def screens_count():
    """Récupère le nombre d'écrans connectés à l'ordinateur.

    Returns
    -------
    screens_count: `int`
        Nombre d'écrans connectés à l'ordinateur.

    Raises
    ------
    RuntimeError :
        Jetée si l'appel de la fonction se fait avant l'initialisation du QApplication (nécessaire).
    """
    return len(screens_list())


@functools.lru_cache(maxsize=8)     # 8 car nombre d'écrans connectables au maximum sur un ordinateur avec 2 CG/GPU
def get_screen(screen_index):
    """fonction permettant de récupérer les informations d'un écran en particulier (position et taille).

    Parameters
    ----------
    screen_index: `int`
        Index de l'écran à retourner (de 1 à Nécrans).

    Returns
    -------
    screen_informations: `tuple[tuple[int, int], tuple[int, int]]`
        Informations sur l'écran, leur position et taille. Format : ((x, y), (w, h)).

    Raises
    ------
    RuntimeError:
        Jetée si lappel de la fonction se fait avant l'initialisation du QApplication (nécessaire) ;
    IndexError:
        Jetée si l'index demandé ne correspond a aucun écran connecté.
    """
    # Vérifie que l'index envoyé correspond bien à un écran visible
    if 1 < screen_index < screens_count():
        raise IndexError(f"Index de l'écran envoyé incorrect : {screen_index} (1 -> {screens_count()})")

    # Sinon retourne les informations de l'écran
    return screens_list()[screen_index - 1]
