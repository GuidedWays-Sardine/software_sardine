"""Module dérivé du module logging permettant de créer des fichiers de registres adapté à la simulation de SARDINE"""
import logging
from enum import Enum
from datetime import datetime


class Level(Enum):
    """Classe contenant les différents niveaux de logs (permet une indépendance du module)"""
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def initialise(path, version, log_level):
    """ crée le fichier log

    Parameters
    ----------
    path : `string`
        Le chemin vers le fichier log par rapport au fichier source
    version : `string`
        La version du programme
    log_level : `Level`
        Le niveau de logging (Level.WARNING, Level.INFO, Level.DEBUG, Level.NOTSET)
    """
    # Vérifie si un fichier log a déjà été créé, si oui, change le niveau de logging sinon le crée
    if logging.getLogger().hasHandlers():
        logging.getLogger().setLevel(log_level.value)
        logging.warning("Fichier de registre pour cette simulation déjà existant. Aucun besoin d'en créer un nouveau.\n")
        return

    # Si aucun log n'est demandé, définit le niveau de log comme "aucun" et retourne
    if log_level is Level.NOTSET:
        logging.basicConfig(level=logging.NOTSET)
        return

    # Rajoute un / à la fin du chemin s'il a été oublié
    if path[len(path) - 1] != "/":
        path += "/"

    # Prend la date et crée le nom du fichier log
    now = str(datetime.now()).split(".", 1)[0]
    file_name = path + "sardine " + version + " " + now + ".log"
    file_name = file_name.replace(':', ';')

    # Crée le fichier log avec les informations envoyées
    logging.basicConfig(level=log_level.value,
                        filename=file_name,
                        datefmt="%H:%M:%S",
                        format="%(asctime)s - %(levelname)s - %(message)s")


def change_log_prefix(prefix=""):
    """Permet à l'utilisateur de changer le préfix devant chaque message de registre pour mieux indiquer leur provenance
    
    Parameters
    ----------
    prefix: `string`
        Le nouveau préfix à mettre en plus de l'heure et du niveau du registre

    Raises
    ------
    FileNotFoundError
        Erreur soulevée lorsque le fichier log n'a pas encore été créé ou qu'il n'existe pas
    """
    # Vérifie qu'un fichier registre existe bien sinon jette l'erreur FileNotFoundError
    if logging.getLogger().hasHandlers():
        raise FileNotFoundError("Aucun fichier de registre existant pour cette simulation")

    # Récupère le handler (fichier registre) à modifier
    handler = logging.getLogger().handlers[0]

    # Si le préfixe est vide, l'ajoute, sinon remet le logging par défaut
    if prefix != "":
        handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S",
                                               fmt="%(asctime)s - [" + str(prefix) + "] - %(levelname)s - %(message)s"))
    else:
        handler.setFormatter(logging.Formatter(datefmt="%H:%M:%S",
                                               fmt="%(asctime)s - %(levelname)s - %(message)s"))

