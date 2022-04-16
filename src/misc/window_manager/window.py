# Librairies par défaut
import os
import sys


# Librairies graphiques
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QObject


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.window_manager.screen as wms
import src.misc.settings_dictionary as sd
import src.misc.decorators as decorators


@decorators.UIupdate
@decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
def set_window_position(window, settings, key, minimum_size=(124, 48)) -> None:
    """Fonction permettant de redimenssioner une fenêtre en toute sécurité

    Parameters
    ----------
    window: `QMainWindow | QObject`
        Fenêtre à redimensionnée, peut provenir d'un QMainWindow (python) ou d'un Window (QML)
    settings: `sd.SettingsDictionary | dict[str, Any]`
        Dictionaire de paramètres contenant les informations sur la fenêtre. Les paramètres suivant doivent apparaitre :
        key.screen_index, key.x, key.y, key.w, key.h -> avec key le paramètre key envoyé
    key: `str`
        Clé à partir de laquelle, les paramètres écrans seront lus.
    minimum_size: `tuple[int, int] | list[int, int]`
        Liste des dimensions minimales de la fenêtre. format : (min_w, min_h)
    """
    # récupère la liste de la position et de la taille de chacun des écrans
    screens = wms.screens_list()

    # Dans le cas où la clé ne se finit pas par un point, l'ajoute
    key += "." if not key.endswith(".") else ""

    # Pour windows, les dimensions minimales d'une fenêtre sont : 124x48. S'assure que c'est le cas
    minimum_size = (max(minimum_size[0], 124), max(minimum_size[1], 48))

    # Si la fenêtre est cachée, il est impossible de récupérer ses informations. Montre la temporairement
    if isinstance(window, QMainWindow):
        is_visible = window.isVisible()
    else:
        is_visible = window.property("visible")
    if not is_visible:
        window.show()

    # Calcule la hauteur de la titlebar
    if isinstance(window, QMainWindow):
        titlebar_height = window.geometry().y() - window.pos().y()
    else:
        titlebar_height = window.geometry().y() - window.framePosition().y()

    # Vérifie que chacun des paramètres nécessaires sont présents dans le dictionaire de paramètres
    if all(((f"{key}{p}" in settings) for p in ("screen_index", "x", "y", "w", "h"))):
        try:
            # Récupère l'index de l'écran, cache la fenêtre s'il vaut 0, le met à 1 si trop peu d'écrans sont connectés.
            screen_index = settings[f"{key}screen_index"]
            if screen_index <= 0:
                log.debug(f"La fenêtre \"{key[:-1]}\" n'est pas activée (screen_index à 0), dimensionnement annulé.")
                window.hide()
                return

            if not (1 <= settings[f"{key}screen_index"] <= len(screens)):
                log.debug(f"L'écran {screen_index} n'existe pas ({len(screens)} écrans).")
                screen_index = 1

            # Commence par calculer la taille théorique maximale selon la position de la fenêtre et la taille écran
            max_window_size = [screens[screen_index - 1][1][0] - settings[f"{key}x"],
                               screens[screen_index - 1][1][1] - settings[f"{key}y"]]

            # Puis garde la dimensions la plus faible entre sa taille demandée et la taille maximale possible
            if max_window_size[0] < settings[f"{key}w"] or max_window_size[1] < settings[f"{key}h"]:
                log.debug(f"Les dimensions pour l'écran \"{key[:-1]}\" ({settings[f'{key}w']}, {settings[f'{key}h']})" +
                          f"sont trop grandes pour l'écran (maximum : {max_window_size[0]}, {max_window_size[1]})." +
                          f"Les dimensions maximales seront utilisées")
            window_size = [min(max_window_size[0], settings[f"{key}w"]),
                           min(max_window_size[1], settings[f"{key}h"])]

            # S'assure que la nouvelle taille de la fenêtre est suffisante (si la fenêtre a une taille minimale=
            if window_size[0] >= minimum_size[0] and (window_size[1] - titlebar_height) >= minimum_size[1]:
                # Repositione et redimensionne la fenêtre (fonctions différentes pour QMainWindow et QObject)
                if isinstance(window, QMainWindow):
                    window.move(screens[screen_index - 1][0][0] + settings[f"{key}x"],
                                screens[screen_index - 1][0][1] + settings[f"{key}y"])
                else:
                    window.setPosition(screens[screen_index - 1][0][0] + settings[f"{key}x"] + 1,
                                       screens[screen_index - 1][0][1] + settings[f"{key}y"] + titlebar_height)
                window.resize(window_size[0], window_size[1] - titlebar_height)
                log.debug(f"fenêtre \"{key[:-1]}\" placée avec succès.")
            else:
                # indique dans le cas où les positions sur l'écran rendent impossible le positionnement de la fenêtre
                log.debug(f"La fenêtre \"{key[:-1]}\" ne rentre pas à l'écran." +
                          f" ({window_size} -> [{minimum_size[0]}, {minimum_size[1]}] minimum).")
        except Exception as error:
            # Récupère une exception si l'une des données n'est pas au bon format
            log.warning(f"Erreur lors du redimensionement de la fenêtre \"{key[:-1]}\".",
                        exception=error)
    else:
        # Sinon laisse un message de debug indiquant que certaines données sont manquantes
        log.debug(f"Paramètres manquants pour la position et la taille de la fenêtre \"{key[:-1]}\".")

    # Si la fenêtre était cachée (motrée temporairement), la recache
    if not is_visible:
        window.hide()


@decorators.UIupdate
@decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
def get_window_position(window, settings, key):
    """Fonction permettant de redimenssioner une fenêtre en toute sécurité

    Parameters
    ----------
    window: `QMainWindow | QObject`
        Fenêtre dont les dimensions doivent être récupérés, peut provenir d'un QMainWindow (python) ou d'un Window (QML)
    settings: `sd.SettingsDictionary | dict`
        Dictionaire de paramètres où les informations seront stockées. Les paramètres seront sous la forme :
        key.screen_index, key.x, key.y, key.w, key.h -> avec key le paramètre key envoyé
    key: `str`
        Clé avec laquelle les dimensions seront enregistrées.
    """
    # Parce que windows pue du cul, voici quelques éléments à prendre en compte :
    # - Quand la fenêtre est maximisée, la "titlebar" dépasse légèrement de la partie supérieur de l'écran
    #   Une marge d'erreur sur l'écran supérieur sera rajoutée pour éviter ce désagrément
    # - Si l'échelle des écrans n'est pas la même, windows redimensionnera les fenêtres lorsqu'ells changent d'écran
    # - La taille d'une fenêtre ne prend pas en compte la titlebar, contrairement à sa position

    # récupère la liste de la position et de la taille de chacun des écrans
    screens = wms.screens_list()

    # Dans le cas où la clé ne se finit pas par un point, l'ajoute
    key += "." if not key.endswith(".") else ""

    # Si la fenêtre est cachée, il est impossible de récupérer ses informations. Montre la temporairement
    if isinstance(window, QMainWindow):
        is_visible = window.isVisible()
    else:
        is_visible = window.property("visible")
    if not is_visible:
        window.show()

    # Calcule la hauteur de la titlebar
    if isinstance(window, QMainWindow):
        titlebar_height = window.geometry().y() - window.pos().y()
    else:
        titlebar_height = window.geometry().y() - window.framePosition().y()

    # Récupère l'écran sur lequel se situe la fenêtre envoyée.
    # Windows décallant légèrement les coordonées de certaines fenêtres et les dimensions minimales étant de 124*48
    # On rajoutera une marge de 24 pixels en haut et à gauche et on enlèvera la même marge en bas et à droite
    screen_index = [i for i in range(len(screens))
                    if (screens[i][0][0] - 1 - 24) <= window.x() <= (screens[i][0][0] + screens[i][1][0] - 24)
                    and (screens[i][0][1] - 1 - 24) <= window.y() <= (screens[i][0][1] + screens[i][1][1] - 24)]

    # Si la fenêtre a été détectée sur un écran, récupère et stocke ses coordonées
    # Pour la position, le max(..., 0) s'assure que le coin supérieur ne sorte pas du haut/de la droite de l'écran
    # Pour la taille, le min(..., w | h) s'assure que la fenêtre n'est pas trop grand si elle a été légèrement déplacée
    # Cela provoquera des déplacements mineurs pour les fenêtre maximisés avec barre des titres
    if screen_index:
        sg = screens[screen_index[0]]
        settings[f"{key}screen_index"] = screen_index[0] + 1
        settings[f"{key}x"] = max(window.x() - sg[0][0] - (not isinstance(window, QMainWindow)), 0)
        settings[f"{key}y"] = max(window.y() - sg[0][1] - titlebar_height * (not isinstance(window, QMainWindow)), 0)
        settings[f"{key}w"] = min(window.width(), sg[1][0])
        settings[f"{key}h"] = min(window.height() + titlebar_height, sg[1][1])

        # Donne des indications sur la position et la taille de l'écran récupéré
        log.debug(f"Emplacement de la fenêtre \"{key[:-1]}\" récupéré avec succès :\n\t" +
                  " ; ".join((f"{p}: {settings[key + p]}" for p in ["screen_index", "x", "y", "w", "h"])))
    else:
        # Indique si la recherche de l'écran  n'a pas été concluant (coin supérieur droit hors de tout écran)
        log.debug(f"Impossible de localiser la fenêtre \"{key[:-1]}\".")

    # Si la fenêtre était cachée (motrée temporairement), la recache
    if not is_visible:
        window.hide()