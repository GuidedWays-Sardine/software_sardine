# Librairies par défaut
import os
import sys
from functools import wraps


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


# Appel : @decorators.QtSignal(log_level=log.Level.DEBUG, end_process=False)
def QtSignal(log_level=log.Level.ERROR, end_process=False):
    """décorateur permettant de récupérer les exceptions dans les signaux (ne pouvant pas être récupéré par le main)

    Parameters
    ----------
    log_level: `log.Level`
        Le niveau du message de registre dans le cas où le signal jette une exception
    end_process: `bool`
        Est ce que l'erreur doit générer une sortie de l'application
    """
    def signal_decorator(signal):
        @wraps(signal)
        def signal_wraper(*args):
            try:
                # Appelle la fonction normalement et récupère une potentielle erreur
                signal(*args)
            except Exception as error:
                # Récupère le nom de la fonction pour plus d'indication et laisse un message de registre
                function_name = str(signal)[10:].split(" at ")[0]
                log.log(log_level=log_level,
                        message=f"Exception jeté dans le signal : {function_name}().",
                        exception=error)
                if end_process:
                    exit(-1)

        return signal_wraper
    return signal_decorator
