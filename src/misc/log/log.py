"""Module dérivé du module logging permettant de créer des fichiers de registres adapté à la simulation de SARDINE"""
import os
import logging
import traceback
from enum import Enum
from datetime import datetime


VERSION = "1.1.0"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]


class Level(Enum):
    """Classe contenant les différents niveaux de logs (permet une indépendance du module)"""
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def initialise(path=f"{PROJECT_DIR}log\\", version=VERSION, log_level=Level.DEBUG, save=True):
    """ crée le fichier log

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
        logging.warning("Fichier de registre pour cette simulation déjà existant. Aucun besoin d'en créer un nouveau.\n")
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
        # Sinon change juste le niveau de debug et le format
        logging.basicConfig(level=log_level.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")


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
    
    Parameters
    ----------
    prefix: `string`
        Le nouveau préfix à mettre en plus de l'heure et du niveau du registre
    """
    # Vérifie qu'un fichier registre existe bien sinon jette l'erreur FileNotFoundError
    if not logging.getLogger().hasHandlers():
        # Sinon crée une configuration de registre par défaut pour pouvoir afficher le message
        logging.basicConfig(level=Level.DEBUG.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.warning("préfix changé sans configuration de registre initialisé précédement (log.initialise().\n")

    # Récupère le handler (fichier registre) à modifier
    handler = logging.getLogger().handlers[0]

    # Si le préfixe est vide, l'ajoute, sinon remet le logging par défaut
    if prefix != "":
        handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S",
                                               fmt=f"%(asctime)s - [{prefix}] - %(levelname)s - %(message)s"))
    else:
        handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S",
                                               fmt="%(asctime)s - %(levelname)s - %(message)s"))


def log(log_level, message, exception=None, prefix=None):
    """Permet de laisser un message de niveau log_level dans le fichier registre

    Parameters
    ----------
    log_level: `Level`
        Le niveau de registre du message (élément de la classe Level)
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire à afficher
    exception: Exception
        Exception à afficher si nécessaire (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    # Vérifie qu'un fichier registre existe bien sinon en crée un (console)
    if not logging.getLogger().hasHandlers():
        # Sinon crée une configuration de registre par défaut pour pouvoir afficher le message
        logging.basicConfig(level=Level.DEBUG.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.warning("fonction de registre appelée sans configuration de registre initialisé (log.initialise().\n")

    # Vérifie si un préfix temporaire a été envoyé et si oui change le préfix utilisé
    previous_format = logging.getLogger().handlers[0].formatter._fmt
    if prefix is not None:
        change_log_prefix(prefix)

    # Rajoute un charactère de fin de ligne pour espace les messages s'il a été oublié
    message += "\n" if message[-1] != "\n" else ""

    # Si une erreur est ajoutée, l'ajoute au message.
    if isinstance(exception, Exception):
        message += (f"\t\tErreur de type ;{type(exception)}\n" +
                    f"\t\tAvec comme message d'erreur : {exception.args}\n\n\t\t" +
                    "".join(traceback.format_tb(exception.__traceback__)).replace("\n", "\n\t\t") + "\n")


    # Laisse le message dans le fichier de registre de niveau debug
    logging.log(log_level.value, message)

    # Si le préfix a été changé temporairement
    if prefix is not None:
        logging.getLogger().handlers[0].setFormatter(logging.Formatter(datefmt="%H:%M:%S", fmt=previous_format))


def debug(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau DEBUG dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire à afficher
    exception: Exception
        Exception à afficher si nécessaire (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.DEBUG, message, exception, prefix)


def info(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau INFO dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire à afficher
    exception: Exception
        Exception à afficher si nécessaire (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.INFO, message, exception, prefix)


def warning(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau WARNING dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire à afficher
    exception: Exception
        Exception à afficher si nécessaire (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.WARNING, message, exception, prefix)


def error(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau ERROR dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire à afficher
    exception: Exception
        Exception à afficher si nécessaire (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.ERROR, message, exception, prefix)


def critical(message, exception=None, prefix=None):
    """Permet de laisser un message de niveau CRITICAL dans le fichier registre

    Parameters
    ----------
    message: `string`
        Le message à afficher dans le registre
    prefix: `string`
        Le préfix temporaire à afficher
    exception: Exception
        Exception à afficher si nécessaire (pour donner plus d'indications sur la raison et l'endroit d'une erreur)
    """
    log(Level.CRITICAL, message, exception, prefix)

def add_empty_lines(lines_count=1, log_level=Level.INFO):
    """Fonction permettant de laisser des lignes vides dans le fichier de registre

    Parameters
    ----------
    lines_count: `int`
        Nombre de lignes vides à ajouter dans le fichier de registre (par défaut 1)
    log_level: `Level`

    """
    # Vérifie qu'un fichier registre existe bien en crée un (console)
    if not logging.getLogger().hasHandlers():
        # Sinon crée une configuration de registre par défaut pour pouvoir afficher le message
        logging.basicConfig(level=Level.DEBUG.value,
                            datefmt="%H:%M:%S",
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.warning("fonction de registre appelée sans configuration de registre initialisé (log.initialise().\n")

    # Récupère le handler (fichier registre) à modifier
    handler = logging.getLogger().handlers[0]

    current_format = handler.formatter._fmt
    handler.setFormatter(logging.Formatter(fmt=""))

    # Ne marche
    log(log_level, "\n" * (lines_count - 1))

    handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S", fmt=current_format))
