import logging
from datetime import datetime


def initialise(path, version, log_level):
    """ crée le fichier log

    Parameters
    ----------
    path : `string`
        Le chemin vers le fichier log par rapport au fichier source
    version : `string`
        La version du programme
    log_level : `int`
        Le niveau de logging (log.ERROR, log.WARNING, log.DEBUG, log.NOTSET)
    """
    # Vérifie si un fichier log a déjà été créé, si oui, change le niveau de logging sinon le crée
    if logging.getLogger().hasHandlers():
        logging.getLogger().setLevel(log_level)
        logging.warning("tentative de création d'un nouveau fichier log")
        return

    # Si aucun log n'est demandé, définit le niveau de log comme "aucun" et retourne
    if log_level is logging.NOTSET:
        logging.basicConfig(level=logging.NOTSET)
        return

    # Rajoute un / à la fin du chemin s'il a été oublié
    if path[len(path) - 1] != '/':
        path += '/'

    # Prend la date et crée le nom du fichier log
    now = str(datetime.now()).split('.', 1)[0]
    file_name = path + 'sardine ' + version + ' ' + now + '.log'
    file_name = file_name.replace(':', ';')

    # Crée le fichier log avec les informations envoyées
    logging.basicConfig(level=log_level,
                        filename=file_name,
                        datefmt='%H:%M:%S',
                        format='%(asctime)s - %(levelname)s - %(message)s')