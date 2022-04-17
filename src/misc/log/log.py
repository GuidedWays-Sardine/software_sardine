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


def initialise(path=f"{PROJECT_DIR}log\\", version=VERSION, log_level=Level.DEBUG, save=True):
    """ initialiser un registre (console ou enregistré)

    Parameters
    ----------
    path : `string`
        Le chemin vers le fichier log par rapport au fichier source
        Par défaut chemin d'accès vers le dossier log du project
    version : `string`
        La version du programme
        Par défaut la version sauvegardée dans le module log (pour éviter les incohérences)
    log_level : `Level`
        Le niveau de logging (Level.WARNING, Level.INFO, Level.DEBUG, Level.NOTSET)
        Par défaut mis pour avoir tous les messages (Level.DEBUG)
    save : `bool`
        Indique si les messages doivent être sauvegardés dans un fichier (sinon elles apparaitront dans le terminal
        Par défault les informations s'enregistrent dans un fichier
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
        
    # Initialise la fenêtr de registre
    from src.misc.log.log_window import __initialise_log_window
    __initialise_log_window()


def change_log_level(log_level):
    """Permet de changer le niveau de registre

    Parameters
    ----------
    log_level: `Level`
        nouveau niveau de registre
    """
    logging.getLogger().setLevel(log_level.value)


def change_log_prefix(prefix=""):
    """Permet à l'utilisateur de changer le préfix devant chaque message de registre pour mieux indiquer leur provenance
    Celui-ci s'affichera entre crochets entre l'heure et le niveau de registre
    
    Parameters
    ----------
    prefix: `string`
        Le nouveau préfix à mettre en plus de l'heure et du niveau du registre
    """
    # Dans le cas où aucun registre n'a été initialisé
    if not logging.getLogger().hasHandlers():
        # initialise un simple registre console et affiche un message de warning pour avertir de l'oubli
        logging.basicConfig(level=Level.DEBUG.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.warning("Préfix changé sans registre initialisé (log.initialise). Configuration par défaut utilisée.")

    # Si un préfix non vide a été envoyé, l'ajoute au format du registre, sinon remet celui par défaut
    handler = logging.getLogger().handlers[0]
    if prefix != "":
        handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S",
                                               fmt=f"%(asctime)s - [{prefix}] - %(levelname)s - %(message)s"))
    else:
        handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S",
                                               fmt="%(asctime)s - %(levelname)s - %(message)s"))


def log(log_level, message, exception=None, prefix=None):
    """Permet de laisser un message de registre de niveau log_level

    Parameters
    ----------
    log_level: `Level`
        Le niveau de registre du message (élément de la classe Level)
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire (uniquement pour ce message) à utiliser
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    # Dans le cas où aucun registre n'a été initialisé
    if not logging.getLogger().hasHandlers():
        # initialise un simple registre console et affiche un message de warning pour avertir de l'oubli
        logging.basicConfig(level=Level.DEBUG.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.warning("Message laissé sans registre initialisé (log.initialise). Configuration par défaut utilisée.")

    # Vérifie si un préfix temporaire a été envoyé, si oui, enregistre le format actuel et change le préfix
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
    from src.misc.log.log_window import add_log_window_message
    add_log_window_message(message, log_level)

    # Si le préfix a été changé temporairement, remet celui d'origine
    if prefix is not None:
        logging.getLogger().handlers[0].setFormatter(logging.Formatter(datefmt="%H:%M:%S", fmt=previous_format))


def debug(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau DEBUG dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire (uniquement pour ce message) à utiliser
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.DEBUG, message, exception, prefix)


def info(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau INFO dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire (uniquement pour ce message) à utiliser
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.INFO, message, exception, prefix)


def warning(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau WARNING dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire (uniquement pour ce message) à utiliser
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.WARNING, message, exception, prefix)


def error(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau ERROR dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire (uniquement pour ce message) à utiliser
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.ERROR, message, exception, prefix)


def critical(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau CRITICAL dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire (uniquement pour ce message) à utiliser
    exception: `Exception`
        Potentielle exception à afficher (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.CRITICAL, message, exception, prefix)


def add_empty_lines(lines_count=1, log_level=Level.INFO):
    """Fonction permettant de rajouter des lignes vides dans le fichier de registre

    Parameters
    ----------
    lines_count: `int`
        Nombre de lignes vides à ajouter dans le fichier de registre (par défaut 1)
    log_level: `Level`
        Le niveau de registre à partir duquel le message doit apparaitre
    """
    # Dans le cas où aucun registre n'a été initialisé
    if not logging.getLogger().hasHandlers():
        # initialise un simple registre console et affiche un message de warning pour avertir de l'oubli
        logging.basicConfig(level=Level.DEBUG.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.warning("lignes sautées sans registre initialisé (log.initialise). Configuration par défaut utilisée.")

    # Récupère le format de registe actuel et le change pour un format vide (pour écrire des lignes vides)
    handler = logging.getLogger().handlers[0]
    current_format = handler.formatter._fmt
    handler.setFormatter(logging.Formatter(fmt=""))

    # Ajoute autant de lignes que demandés (si la valeur est négative, une seule ligne sera sautée)
    log(log_level, "\n" * (lines_count - 1))

    # Remet de nouveau le format actuel
    handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S", fmt=current_format))


def _qt_message_handler(mode, context, message):
    """Fonction (non appelable) permettant de récupérer et d'afficher les messages d'erreurs des fichiers qml

    Parameters
    ----------
    mode: `QtCore.QtInfoMsg`
        Niveau du message d'erreur (convertit en niveau de registre
    context: `QtCore.QMessageLogContext`
        Contexte sur le message d'erreur (fichier, ligne, charactère
    message: `str`
        message associé à l'erreur
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
