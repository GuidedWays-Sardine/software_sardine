# Librairies par défaut
import os
import sys
import functools
import threading


# Librairies graphiques
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow
from PyQt5.QtCore import QObject


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd
import src.misc.decorators.decorators as decorators


@functools.lru_cache(maxsize=1)
def get_screens_informations():
    """fonction permettant de récupérer les informations sur tous les écrans détectés (position et taille)

    Returns
    -------
    screens_informations: `tuple[tuple[tuple[int, int], tuple[int, int]]`
        information sur les écrans, indiquant leur position et taille
        format : (((x, y), (w, h)), ...)

    Raises
    ------
    RuntimeError :
        Jetée si le premier appel de la fonction se fait avant l'initialisation du QApplication (nécessaire).
    """
    # Vérifie qu'un QApplication a déjà été généré (vital à la récupération des écrans)
    if QApplication.instance() is None:
        raise RuntimeError("Le QApplication doit être initialisé pour permettre la récupération de la liste des écrans")

    window_size = []
    # Charge tous les écrans connectés à l'ordinateur (utile pour la positionnement de certaines popup)
    for screen_index in range(0, QDesktopWidget().screenCount()):
        # Charge les informations de l'écran (au format [x_min, y_min, x_max, y_max]
        sg = QDesktopWidget().screenGeometry(screen_index).getCoords()

        # Les stockes au bon format ((x, y), (w, h))
        window_size.append(((sg[0], sg[1]), (sg[2] - sg[0] + 1, sg[3] - sg[1] + 1)))

    log.info(f"Détection de {len(window_size)} écrans connectés à l'ordinateur.")
    return tuple(window_size)


@decorators.UIupdate
@decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
def set_window_position(window, key, settings, minimum_size=(0, 0)):
    """Fonction permettant de redimenssioner une fenêtre en toute sécurité

    Parameters
    ----------
    window: `QMainWindow | QObject`
        Fenêtre à redimensionnée, peut provenir d'un QMainWindow (python) ou d'un Window (QML)
    key: `str`
        Clé à partir de laquelle, les paramètres écrans seront lus.
    settings: `sd.SettingsDictionary`
        Dictionaire de paramètres contenant les informations sur la fenêtre. Les paramètres suivant doivent apparaitre :
        key.screen_index, key.x, key.y, key.w, key.h -> avec key le paramètre key envoyé
    minimum_size: `tuple[int, int] | list[int, int]`
        Liste des dimensions minimales de la fenêtre. format : (min_w, min_h)
    """
    # récupère la liste de la position et de la taille de chacun des écrans
    screens = get_screens_informations()

    # Dans le cas où la clé ne se finit pas par un point, l'ajoute
    key += "." if not key.endswith(".") else ""

    # Calcule la hauteur de la titlebar
    title_bar_height = window.geometry().y() - window.pos().y()

    # Vérifie que chacun des paramètres nécessaires sont présents dans le dictionaire de paramètres
    if all(((f"{key}{p}" in settings) for p in ("screen_index", "x", "y", "w", "h"))):
        try:
            # Récupère l'index de l'écran, retourne s'il vaut 0 et le met à 1 si trop peu d'écrans sont connectés
            screen_index = settings[f"{key}screen_index"]
            if screen_index <= 0:
                log.debug(f"La fenêtre \"{key[:-1]}\" n'est pas activée (screen_index à 0), dimensionnement annulé.")
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
            if window_size[0] >= minimum_size[0] and (window_size[1] - title_bar_height) >= minimum_size[1]:
                # Repositione et redimensionne la fenêtre (fonctions différentes pour QMainWindow et QObject)
                if isinstance(window, QMainWindow):
                    window.move(screens[screen_index - 1][0][0] + settings[f"{key}x"],
                                screens[screen_index - 1][0][1] + settings[f"{key}y"])
                else:
                    window.setPosition(screens[screen_index - 1][0][0] + settings[f"{key}x"],
                                       screens[screen_index - 1][0][1] + settings[f"{key}y"])
                window.resize(window_size[0], window_size[1] - title_bar_height)
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


@decorators.UIupdate
@decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
def get_window_position(window, key, settings):
    """Fonction permettant de redimenssioner une fenêtre en toute sécurité

    Parameters
    ----------
    window: `QMainWindow | QObject`
        Fenêtre dont les dimensions doivent être récupérés, peut provenir d'un QMainWindow (python) ou d'un Window (QML)
    key: `str`
        Clé avec laquelle les dimensions seront enregistrées.
    settings: `sd.SettingsDictionary`
        Dictionaire de paramètres où les informations seront stockées. Les paramètres seront sous la forme :
        key.screen_index, key.x, key.y, key.w, key.h -> avec key le paramètre key envoyé
    """
    # Parce que windows pue du cul, voici quelques éléments à prendre en compte :
    # - Quand la fenêtre est maximisée, la "titlebar" dépasse légèrement de la partie supérieur de l'écran
    #   Une marge d'erreur sur l'écran supérieur sera rajoutée pour éviter ce désagrément
    # - Si l'échelle des écrans n'est pas la même, windows redimensionnera les fenêtres lorsqu'ells changent d'écran
    # - La taille d'une fenêtre ne prend pas en compte la titlebar, contrairement à sa position

    # récupère la liste de la position et de la taille de chacun des écrans
    screens = get_screens_informations()

    # Dans le cas où la clé ne se finit pas par un point, l'ajoute
    key += "." if not key.endswith(".") else ""

    # Calcule la hauteur de la titlebar
    title_bar_height = window.geometry().y() - window.pos().y()

    # Récupère l'écran sur lequel se situe la fenêtre envoyée.
    screen_index = [i for i in range(len(screens))
                    if (screens[i][0][0] - 1) <= window.x() <= (screens[i][0][0] + screens[i][1][0])
                    and (screens[i][0][1] - 1 - title_bar_height) <= window.y() <= (screens[i][0][1] + screens[i][1][1] - title_bar_height)]

    # Si la fenêtre a été détectée sur un écran, récupère et stocke ses coordonées
    # Pour la position, le max(..., 0) s'assure que le coin supérieur ne sorte pas du haut/de la droite de l'écran
    # Pour la taille, le min(..., w | h) s'assure que la fenêtre n'est pas trop grand si elle a été légèrement déplacée
    # Cela provoquera des déplacements mineurs pour les fenêtre maximisés avec barre des titres
    if screen_index:
        sg = screens[screen_index[0]]
        settings[f"{key}screen_index"] = screen_index[0] + 1
        settings[f"{key}x"] = max(window.x() - sg[0][0], 0)
        settings[f"{key}y"] = max((window.y() - sg[0][1]), 0)
        settings[f"{key}w"] = min(window.width(), sg[1][0])
        settings[f"{key}h"] = min(window.height() + title_bar_height, sg[1][1])

        # Donne des indications sur la position et la taille de l'écran récupéré
        log.debug(f"Emplacement de la fenêtre \"{key[:-1]}\" récupéré avec succès :\n\t" +
                  " ; ".join((f"{p}: {settings[key + p]}" for p in ["screen_index", "x", "y", "w", "h"])))
    else:
        # Indique si la recherche de l'écran  n'a pas été concluant (coin supérieur droit hors de tout écran)
        log.debug(f"Impossible de localiser la fenêtre \"{key[:-1]}\".")


def main():
    import threading
    from PyQt5.QtWidgets import QMainWindow

    app = QApplication(sys.argv)
    win = QMainWindow()
    thread = threading.Thread(target=worker, daemon=True, args=(win,))
    thread.start()

    win.show()
    app.exec()


def worker(win):
    import time
    settings = sd.SettingsDictionary()
    for i in range(5):
        # Do some random tests
        get_window_position(win, f"test{i}", settings)
        time.sleep(0.5)
        set_window_position(window=win, key=f"test", settings={"test.screen_index": 1,
                                           "test.x": 35 * i,
                                           "test.y": 35 * i,
                                           "test.w": 300,
                                           "test.h": 210})
        time.sleep(0.5)
    print(settings)


if __name__ == "__main__":
    main()
