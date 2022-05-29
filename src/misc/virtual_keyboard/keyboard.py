# Librairies par défaut
import functools
import os
import sys
import time
import pyautogui


# Librairies graphiques
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QObject, Qt


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.decorators as decorators
import src.misc.log as log
import src.misc.window_manager as wm
from src.misc.virtual_keyboard.mode import KeyboardMode, get_keyboard_from_language


# Instance du clavier virtuel
KEYBOARD = []
NUMPAD_SIZE = (240, 300)        # Tailles maximales pour le pavé numérique et le clavier
KEYBOARD_SIZE = (900, 300)


class VirtualKeyboard:
    """Partie logique du clavier virtuel"""
    # Chemin d'accès vers le fichier graphique du clavier virtuel
    keyboard___window_file_path = PROJECT_DIR + "\\src\\misc\\virtual_keyboard\\Keyboard.qml"

    # Eléments nécessaires au chargement de l'image
    __engine = None
    __win = None

    # Valeur pour indiquer si le clavier virtuel est activé (mettre à False si un clavier solide est utilisé)
    __is_activated = True

    def __init__(self):
        """Initialise le clavier virtuel (par défaut KeyboardMode.NUMPAD).

        Raises
        ------
        FileNotFoundError:
            Jetée si le fichier QML (graphique) du clavier virtuel n'est pas trouvé ;
        SyntaxError:
            Jetée si le fichier QML (graphique) du clavier virtuel contient des erreurs.
        """
        initial_time = time.perf_counter()
        # Cherche pour le fichier QML avec tous les éléments de la fenêtre du clavier virtuel
        self.__engine = QQmlApplicationEngine()
        self.__engine.load(self.keyboard___window_file_path)

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.__engine.rootObjects() and not os.path.isfile(self.keyboard___window_file_path):
            raise FileNotFoundError(f"Le fichier .qml du clavier virtuel (virtual_keyboard) n'a pas été trouvée.\n\t" +
                                    self.keyboard___window_file_path)
        elif not self.__engine.rootObjects() and os.path.isfile(self.keyboard___window_file_path):
            raise SyntaxError(f"Le fichier .qml du clavier virtuel (virtual_keyboard) contient des erreurs.\n\t" +
                              self.keyboard___window_file_path)
        else:
            # Récupère la fenêtre et la cache
            self.__win = self.__engine.rootObjects()[0]
            self.__win.hide()

            # Indique au clavier virtuel de taper la touche à chaque fois qu'elle est touchée
            # pyautogui.typewrite prend la clé comme argument. Celle-ci est fourni par l'émission du signal
            self.__win.key_clicked.connect(pyautogui.typewrite)
            self.__win.key_pushed.connect(pyautogui.press)

            # Indique le temps de chargement du clavier virtuel
            log.info(f"Initialisation du clavier virtuel en " +
                     f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.",
                     prefix="Chargement clavier virtuel")

    def change_keyboard(self, keyboard_mode) -> None:
        """Change le mode/la langue du clavier virtuel.

        Parameters
        ----------

        keyboard_mode: `KeyboardMode`:
            Mode du nouveau clavier (contenant la liste des touches comme valeur).
        """
        if isinstance(keyboard_mode, KeyboardMode):
            # Change le clavier actif
            self.__win.setProperty("keyboard", keyboard_mode.value)

            # Change la dimension du clavier virtuel (automatiquement réalisé par le fichier graphique)
            # Dimensions conseillées : 260*300 en mode numpad ; 900*300 en mode clavier
            self.__win.setProperty("width", 260 if keyboard_mode.value == [] else 900)
            self.__win.setProperty("height", 300)
        else:
            log.warning(f"{keyboard_mode} n'est pas de type KeyboardMode, changement de langue non pris en compte.,",
                        prefix="Clavier virtuel")

    def change_skip_list(self, skip_list):
        """Change la liste des charactères interdits (ceux-ci apparaitront mais ne seront pas sélectionable).

        Parameters
        ----------
        skip_list: `list[str], tuple[str]`
            Liste des charactère interdits.
        """
        self.__win.setProperty("skip_list", list(skip_list))

    def move_to(self, x, y):
        """Bouge la fenêtre aux coordonées (absolus) envoyées

        Parameters
        ----------
        x: `int`
            Coordonées x à partir du coin haut, gauche du premier écran ;
        y: `int`
            Coordonées y à partir du coin haut, gauche du premier écran ;
        """
        self.__win.setProperty("x", x)
        self.__win.setProperty("y", y)

    def resize(self, width_factor, height_factor):
        """Redimenssione le clavier virtuel en fonction de sa taille théorique maximale et de ses facteurs.

        Parameters
        ----------
        width_factor: `float`
            Facteur de réduction sur la largeur du composant (compris entre 0.0 et 1.0) ;
        height_factor: `float`
            Facteur de réduction sur la hauteur du composant (compris entre 0.0 et 1.0).
        """
        keyboard_size = KEYBOARD_SIZE if self.__win.property("keyboard").toVariant() else NUMPAD_SIZE

        # Vérifie que les facteurs sont biens entre 0 et 1 (sinon l'indique dans le registre)
        if width_factor <= 0 or height_factor <= 0:
            log.debug(f"Les facteurs de conversions pour le clavier numériques doivent être strictement positifs " +
                      f"(width_factor = {width_factor} ; height_factor = {height_factor}).",
                      prefix="Clavier virtuel")
        elif width_factor > 1 or height_factor > 1:
            log.debug(f"Le clavier numérique ne peut pas avoir une taille supérieure à sa taille maximale " +
                      f"(width_factor = {width_factor} ; height_factor = {height_factor}).",
                      prefix="Clavier virtuel")

        # Calcule les dimensions finales du clavier et le redimensionne
        width = min(max(round(keyboard_size[0] * width_factor), 1), keyboard_size[0])
        height = min(max(round(keyboard_size[1] * height_factor), 1), keyboard_size[1])
        self.__win.setProperty("width", width)
        self.__win.setProperty("height", height)

        # Si les nouvelles dimensions de la fenêtre sont inférieures à celles maximales, l'indique dans le registre
        if 0 < width_factor < 1 or 0 < height_factor < 1:
            log.debug(f"Pas suffisament d'espace pour afficher le clavier virtuel en ses dimensions maximales " +
                      f"({width}*{height} au lieu de {keyboard_size[0]}*{keyboard_size[1]})")

    def show(self):
        """Montre le clavier virtuel"""
        self.__win.show()

    def hide(self):
        """Cache le clavier virtuel"""
        self.__win.hide()

    def is_activated(self, new_state=None):
        """Retourne (et change) l'état de la variable indiquant si le module du clavier virtuel est activé.

        Parameters
        ----------
        new_state: `bool | None`
            Nouvel état de la variable pour si le module du clavier virtuel est activé (None pour ne pas changer).

        Returns
        -------
        current_state: `bool`
            Etat de la variable après changement.
        """
        # Change l'état de la variable si un nouvel état a été envoyé
        if new_state is not None:
            self.__is_activated = bool(new_state)

        # Retour ce nouvel état/l'état actuel
        return self.__is_activated


@decorators.UniqueCall
def initialise_keyboard():
    """Initialise le clavier virtuel. Si celui-ci ne s'initialise par correctement, il ne pourra pas être utilisé."""
    # Essaye d'initialiser le clavier virtuel. Si celui-ci contient une erreur, l'indique dans le registre
    try:
        KEYBOARD.append(VirtualKeyboard())
    except Exception as error:
        log.error("Erreur lors de l'initialisation du clavier virtuel. Le clavier virtuel ne sera pas utilisé.",
                  exception=error, prefix="Clavier virtuel")


def change_skip_list(skip_list=()):
    """Change la liste des charactères interdits.

    Parameters
    ----------
    skip_list: `list[str] | tuple[str]`
        Liste des charactères interdits.
    """
    # Si un clavier n'a pas été initialisé, essaye de l'initialiser
    if not KEYBOARD:
        initialise_keyboard()

    # Si un clavier a été initialisé, change la skip_list
    if KEYBOARD:
        KEYBOARD[0].change_skip_list(skip_list)


def change_mode(language=KeyboardMode.NUMPAD):
    """Change le mode/la langue du clavier virtuel.

    Parameters
    ----------
    language: `KeyboardMode | str`
        langue ou clavier à utiliser
    """
    # Si un clavier n'a pas été initialisé, essaye de l'initialiser
    if not KEYBOARD:
        initialise_keyboard()

    # Si une langue a été envoyée, récupère le clavier correspondant et change la langue
    if KEYBOARD and isinstance(language, str):
        KEYBOARD[0].change_keyboard(get_keyboard_from_language(language))
    # Si un clavier a directement été envoyé, le définit
    elif KEYBOARD and isinstance(language, KeyboardMode):
        KEYBOARD[0].change_keyboard(language)


@decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
def show_keyboard(window, widget, language=KeyboardMode.NUMPAD, skip_list=()):
    """Montre le clavier virtuel.

    Parameters
    ----------
    window: `QMainWindow | QWindow | QObject`
        Fenêtre à laquelle appartient le composant ;
    widget: `QObject`
        Objet auquel le clavier sera rattaché (généralement l'objet actif).
        Doit contenir de préfére,ce les variables : [default_x/y, default_width, default_height, ratio, x/y_offset]
        sinon les positions réelles du composant seront prises en compte ;
    language: `str | KeyboardMode | None`
        str -> langue du clavier à utiliser ;
        KeyboardMode -> clavier à utiliser ;
        None -> Le clavier ne sera pas changé et le précédent sera utilisé ;
    skip_list: `list[str] | tuple[str] | None`
        Liste des lettres à ne pas considérer.
    """
    # Si le clavier virtuel n'a pas été initialisé, essaye de l'initialiser
    if not KEYBOARD:
        initialise_keyboard()

    # Si le clavier a été initialisé
    if KEYBOARD:
        # Change le clavier actuel et la liste des charactères inteerdits
        change_mode(language)
        change_skip_list(skip_list)

        # Position de la fenêtre sur l'écran
        x = window.x() - ("framePosition" in dir(window)) + ("setPosition" not in dir(window))
        y = window.geometry().y()

        # Ajoute la position du composant sur la fenêtre (différencie le cas d'un composent personalisé et défaut)
        if not any(widget.property(key) is None for key in ("default_x", "default_y", "default_width", "default_height", "ratio")):
            # Dans le cas d'un composant personalisé avec auto redimensionnement
            x += widget.property("default_x") * widget.property("ratio")
            y += widget.property("default_y") * widget.property("ratio")
            width = widget.property("default_width") * widget.property("ratio")
            height = widget.property("default_height") * widget.property("ratio")

            # Ajoute le décallage dans le cas d'une fenêtre qui doit garder strictement le même ratio (DMI, ...)
            if widget.property("x_offset") is not None and widget.property("y_offset") is not None:
                x += widget.property("x_offset")
                y += widget.property("y_offset")
        else:
            # Dans le cas d'un composant par défaut avec les propriétés de base
            x += widget.property("x")
            y += widget.property("y")
            width = widget.property("width")
            height = widget.property("height")

        # Récupère les dimensions du type de clavier utilisé
        size = KEYBOARD_SIZE if get_keyboard_from_language(language).value else NUMPAD_SIZE

        # Récupère la fenêtre où se situe  le composant
        screens = wm.screens_list()
        screen_index = [i + 1 for i in range(len(screens))
                        if (screens[i][0][0] - 1 - 24) <= x <= (screens[i][0][0] + screens[i][1][0] - 24)
                        and (screens[i][0][1] - 1 - 24) <= y <= (screens[i][0][1] + screens[i][1][1] - 24)]

        # Si l'écran a été trouvé
        if screen_index:
            screen = wm.get_screen(screen_index[0])
            margins = [x + width - screen[0][0],
                       y - screen[0][1],
                       screen[0][0] + screen[1][0] - x,
                       screen[0][1] + screen[1][1] - (y + height)]
        else:
            # L'indique dans le registre et définit des données pour que le clavier se place en bas à gauche
            object_name = widget.property("objectName") if widget.property("objectName") is not None else ""
            log.debug(f"Impossible de localiser le composant \"{object_name}\" risque de mauvais placement du clavier.",
                      prefix="Clavier virtuel")
            margins = [0, 0, size[0], size[1]]

        # Récupère le ratio de réduction entre la taile du clavier maximale et celle permise pour chaque emplacement
        margins = [max(min(margins[0] / size[0], 1), 0),
                   max(min(margins[1] / size[1], 1), 0),
                   max(min(margins[2] / size[0], 1), 0),
                   max(min(margins[3] / size[1], 1), 0)]

        # Choisis maintenant la position du composant de la sorte suivante :
        #  - de préférence en bas à gauche (index 0 et 1)
        #  - si emplacement trop petit -> le place là où il rentre en entier
        #  - s'il rentre en entier nulle part -> le rentre là où il sera le plus grand (et redimensionne le clavier)
        KEYBOARD[0].move_to(round(x if margins[2] == 1 or margins[2] > margins[0] else (x + width - size[0] * margins[0])),
                            round((y + height) if margins[3] == 1 or margins[3] > margins[1] else (y - size[1] * margins[1])))

        # Si le clavier a du être réduit, le redimensionne par le facteur
        KEYBOARD[0].resize(max(margins[0], margins[2]), max(margins[1], margins[3]))

        # Montre le clavier virtuel et redonne le focus au composant édité
        KEYBOARD[0].show()
        window.give_focus()


@decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
def hide_keyboard():
    """Cache le clavier virtuel."""
    # Si le clavier n'a pas été initialisé, initialise le (il sera caché)
    if not KEYBOARD:
        initialise_keyboard()
    # Sinon, si le clavier n'est pas en train d'être montré, le cache
    elif KEYBOARD:
        KEYBOARD[0].hide()
