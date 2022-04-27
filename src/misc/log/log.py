# librairies par défaut
import os
import sys
import logging
import traceback
from datetime import datetime
import re


# librairies graphiques (pour récupérer les messages d'erreurs)
from PyQt5 import QtCore


VERSION = "1.1.0"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
from src.misc.log.log_levels import Level
QT_IGNORE = ("Found metadata in lib",
             "Got keys from plugin meta data",
             "loaded library",
             "loaded plugins",
             "QFactoryLoader::QFactoryLoader() looking at",
             "QFactoryLoader::QFactoryLoader() checking directory path")   # List of all spammy debug messages to ignore


def initialise(path=f"{PROJECT_DIR}log\\", version=VERSION, log_level=Level.DEBUG, save=True) -> None:
    """Initialise un registre (console ou enregistré).

    Parameters
    ----------
    path : `string`
        Chemin vers le fichier log par rapport au fichier source. (par défaut {PROJECT_DIR}/log).
    version : `string`
        Version du programme (stocké en haut du fichier log.py du module).
    log_level : `Level`
        Niveau de registre. (Par défaut Level.DEBUG pour inscrire tous les messages de registre).
    save : `bool`
        Indique si les messages doivent être sauvegardés dans un fichier ;
    terminal: `bool`
        Indique si le terminal sera utilisé (sinon il ne sera pas initialisé).
    """
    # Vérifie si un fichier log a déjà été créé, si oui, change le niveau de logging sinon le crée
    if logging.getLogger().hasHandlers():
        logging.getLogger().setLevel(log_level.value)
        logging.warning("Fichier de registre pour cette simulation déjà existant. Aucun besoin d'en créer un nouveau.")
        return

    # Dans le cas où les logs doivent être enregistrées et que le niveau n'est pas mis à log.NOTSET
    if save and log_level is not Level.NOTSET:
        # Rajoute un / à la fin du chemin s'il a été oublié
        path += "\\" if path[-1] != "/" or "\\" else ""
        path.replace("/", "\\")

        # Prend la date et crée le nom du fichier log
        now = str(datetime.now()).split(".", 1)[0]
        file_name = path + f"sardine {version} {now}.log".replace(':', ';')

        # Crée le fichier log avec les informations envoyées
        logging.basicConfig(level=log_level.value,
                            filename=file_name,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
    else:
        # Sinon crée juste une configuration sans fichier (le registre s'affichera dans la console directement)
        logging.basicConfig(level=log_level.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
        
    # si le terminal a été demandé, l'initialise
    if terminal:
        from src.misc.log.log_window import __initialise_log_window
        __initialise_log_window()


def change_log_level(log_level) -> None:
    """Change le niveau de registre le niveau de registre.

    Parameters
    ----------
    log_level: `Level`
        Nouveau niveau de registre.
    """
    logging.getLogger().setLevel(log_level.value)
    info(f"Niveau de registre changé à : {log_level[6:]}.")


def change_log_prefix(prefix="") -> None:
    """Change le Préfixe devant chaque message de registre pour mieux indiquer leur provenance.
    Celui-ci s'affichera entre crochets entre l'heure et le niveau de registre.
    
    Parameters
    ----------
    prefix: `string`
        Le nouveau Préfixe à afficher.
    """
    # Dans le cas où aucun registre n'a été initialisé
    if not logging.getLogger().hasHandlers():
        # initialise un simple registre console et affiche un message de warning pour avertir de l'oubli
        logging.basicConfig(level=Level.DEBUG.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.warning("Préfixe changé sans registre initialisé. Configuration par défaut utilisée.")

        # Initialise la fenêtre de registre
        from src.misc.log.log_window import __initialise_log_window, __add_log_window_message
        __initialise_log_window()
        __add_log_window_message("Préfixe changé sans registre initialisé. Configuration par défaut utilisée.",
                               Level.WARNING)

    # Si un Préfixe non vide a été envoyé, l'ajoute au format du registre, sinon remet celui par défaut
    handler = logging.getLogger().handlers[0]
    if prefix != "":
        handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S",
                                               fmt=f"%(asctime)s - [{prefix}] - %(levelname)s - %(message)s"))
    else:
        handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S",
                                               fmt="%(asctime)s - %(levelname)s - %(message)s"))


def get_log_level():
    """Récupère le niveau de registre

    Returns
    -------
    log_level: `Level`
        Niveau de registre actuel.
    """
    # Retourne le niveau (convertit de niveau logging au niveau Level). retourne Level.NOTSET si niveau inconnu
    try:
        return {50: Level.CRITICAL,
                40: Level.ERROR,
                30: Level.WARNING,
                20: Level.INFO,
                10: Level.DEBUG,
                00: Level.NOTSET}[logging.root.level]
    except KeyError:
        return Level.NOTSET


def get_log_prefix():
    """Récupère le préfix actuel
    
    Returns 
    -------
    log_prefix: `str`
        Préfixe actuel du registre.
    """
    log_format = logging.getLogger().handlers[0].formatter._fmt
    return log_format.split("[")[-1].split("]")[0] if "[" in log_format else ""


def log(log_level, message, exception=None, prefix=None) -> None:
    """Permet de laisser un message de registre de niveau log_level.

    Parameters
    ----------
    log_level: `Level`
        Niveau de registre du message.
    message: `string`
        Message à afficher dans le registre.
    prefix: `string`
        Préfixe temporaire (uniquement pour ce message) à utiliser.
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur).
    """
    # Dans le cas où aucun registre n'a été initialisé
    if not logging.getLogger().hasHandlers():
        # initialise un simple registre console et affiche un message de warning pour avertir de l'oubli
        logging.basicConfig(level=Level.DEBUG.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.warning("Message laissé sans registre initialisé. Configuration par défaut utilisée.")

        # Initialise la fenêtre de registre
        from src.misc.log.log_window import __initialise_log_window, __add_log_window_message
        __initialise_log_window()
        __add_log_window_message("Message laissé sans registre initialisé. Configuration par défaut utilisée.",
                               Level.WARNING)

    # Vérifie si un Préfixe temporaire a été envoyé, si oui, enregistre le format actuel et change le préfix
    previous_format = logging.getLogger().handlers[0].formatter._fmt
    if prefix is not None:
        change_log_prefix(prefix)

    # Dans le cas où une exception a été envoyée, l'ajoute dans le message avec une belle présentation
    if isinstance(exception, Exception):
        message += (("\n" if not message.endswith("\n") else "") + f"\tErreur de type : {type(exception)}\n" +
                    f"\tAvec comme message d'erreur : {exception.args}\n\t" + "Traceback : \n\t" +
                    "".join(traceback.format_tb(exception.__traceback__)).replace("\n", "\n\t"))

    # Remplace les "\n\t..." par autant d'espaces que nécessaire pour bien aligner le texte avec le message
    prefix_length = len(logging.getLogger().handlers[0].formatter._fmt) - 3 - 19 + len(str(log_level)) - 11
    message = re.sub("\\n[\\t]*", "\n" + " " * prefix_length, message)

    # Laisse le message fraichement créé dans le registre avec le niveau de registre demandé
    logging.log(log_level.value, message)
    from src.misc.log.log_window import __add_log_window_message
    __add_log_window_message(message, log_level)

    # Si le Préfixe a été changé temporairement, remet celui d'origine
    if prefix is not None:
        logging.getLogger().handlers[0].setFormatter(logging.Formatter(datefmt="%H:%M:%S", fmt=previous_format))


def debug(message, exception=None, prefix=None) -> None:
    """Permet de laisser un message de niveau DEBUG dans le fichier registre.

    Parameters
    ----------
    message: `string`
        Message à afficher dans le registre.
    prefix: `string`
        Préfixe temporaire (uniquement pour ce message) à utiliser.
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur).
    """
    log(Level.DEBUG, message, exception, prefix)


def info(message, exception=None, prefix=None) -> None:
    """Permet de laisser un message de niveau INFO dans le fichier registre.

    Parameters
    ----------
    message: `string`
        Message à afficher dans le registre.
    prefix: `string`
        Préfixe temporaire (uniquement pour ce message) à utiliser.
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur).
    """
    log(Level.INFO, message, exception, prefix)


def warning(message, exception=None, prefix=None) -> None:
    """Permet de laisser un message de niveau WARNING dans le fichier registre.

    Parameters
    ----------
    message: `string`
        Message à afficher dans le registre.
    prefix: `string`
        Préfixe temporaire (uniquement pour ce message) à utiliser.
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur).
    """
    log(Level.WARNING, message, exception, prefix)


def error(message, exception=None, prefix=None) -> None:
    """Permet de laisser un message de niveau ERROR dans le fichier registre.

    Parameters
    ----------
    message: `string`
        Message à afficher dans le registre.
    prefix: `string`
        Préfixe temporaire (uniquement pour ce message) à utiliser.
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur).
    """
    log(Level.ERROR, message, exception, prefix)


def critical(message, exception=None, prefix=None) -> None:
    """Permet de laisser un message de niveau CRITICAL dans le fichier registre.

    Parameters
    ----------
    message: `string`
        Message à afficher dans le registre.
    prefix: `string`
        Préfixe temporaire (uniquement pour ce message) à utiliser.
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur).
    """
    log(Level.CRITICAL, message, exception, prefix)


def add_empty_lines(lines_count=1, log_level=Level.INFO) -> None:
    """Fonction permettant de rajouter des lignes vides dans le fichier de registre.

    Parameters
    ----------
    lines_count: `int`
        Nombre de lignes vides à ajouter dans le fichier de registre (par défaut 1).
    log_level: `Level`
        Niveau de registre à partir duquel le message doit apparaitre.
    """
    # Dans le cas où aucun registre n'a été initialisé, retourne (inutile de commencer le registre par une ligne vide
    if not logging.getLogger().hasHandlers():
        return

    # Récupère le format de registe actuel et le change pour un format vide (pour écrire des lignes vides)
    handler = logging.getLogger().handlers[0]
    current_format = handler.formatter._fmt
    handler.setFormatter(logging.Formatter(fmt=""))

    # Ajoute autant de lignes que demandés (si la valeur est négative, une seule ligne sera sautée)
    log(log_level, "\n" * (lines_count - 1))

    # Remet de nouveau le format actuel
    handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S", fmt=current_format))


def _qt_message_handler(mode, context, message) -> None:
    """Fonction (non appelable) permettant de récupérer et d'afficher les messages d'erreurs des fichiers qml.

    Parameters
    ----------
    mode: `QtCore.QtInfoMsg`
        Niveau du message d'erreur (convertit en niveau de registre)
    context: `QtCore.QMessageLogContext`
        Contexte sur le message d'erreur (fichier, ligne, charactère)
    message: `str`
        Message associé à l'erreur
    """
    # Vérifie que l'erreur ne fait pas partie des erreurs à sauter (pour éviter le spam en niveau debug)
    if not any(ignore in message for ignore in QT_IGNORE):
        message = f"message : {message.split(': ', maxsplit=1)[-1]}" + \
                  (f"\n\tline: {context.line} ; file: {context.file}" if context.file is not None else "")

        # Pour chaque mode, met le message d'erreur sous le bon format et l'indique dans le registre
        if mode == QtCore.QtFatalMsg or mode == QtCore.QtFatalMsg:
            critical(f"Erreur Critique dans un fichier graphique QML : \n\t{message}", prefix="QML")
        elif mode == QtCore.QtWarningMsg:
            warning(message, prefix="QML")
        else:
            debug(message, prefix="QML")
