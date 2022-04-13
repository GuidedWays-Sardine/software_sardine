# Librairies par défaut
import os
import sys
from functools import wraps
import inspect
import functools
import threading
import copy


# Librairies graphiques
from PyQt5 import QtCore


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


# Appel : @decorators.CommandBoardComponent
def CommandBoardComponent():
    """décorateur permettant de récupérer les exceptions lors de l'initialision d'une des sous-classe pour le pupitre"""
    def signal_decorator(init):
        @wraps(init)
        def signal_wraper(*args, **kwargs):
            try:
                # Appelle la fonction normalement et récupère une potentielle erreur
                return init(*args, **kwargs)
            except Exception as error:
                # Laisse un message en niveau log.WARNING pour indiquer que le composant n'a pas su être chargé
                log.warning("Un des composant pour le pupitre n'a pas pu être chargé correctement : \n" +
                            f"\tErreur de type : {type(error)}\n\tAvec comme message d'erreur : {error.args}\n\t")

        return signal_wraper
    return signal_decorator


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
        def signal_wraper(*args, **kwargs):
            try:
                # Appelle la fonction normalement et récupère une potentielle erreur
                signal(*args, **kwargs)
            except Exception as error:
                # Récupère le nom de la fonction pour plus d'indication et laisse un message de registre
                function_name = str(signal)[10:].split(" at ")[0]
                log.log(log_level=log_level,
                        message=f"Exception jetée dans le signal : {function_name}().",
                        exception=error)
                if end_process:
                    exit(-1)

        return signal_wraper
    return signal_decorator


# Appel : @decorators.UIupdate
class UIupdate:
    """décorateur à obligatoirement utiliser pour toutes les fonctions mettant à jour des éléments grahiques"""

    class UIThread(QtCore.QThread):
        """Classe contenant tous les éléments nécessaires pour faire fonctionner le décorateur"""
        # Informations nécessaires pour la génération des pyqtSignal
        # Les arguments de pyqtSignal dépendent du nombre d'arguments de la fonction
        # Cependant le pyqtSignal doit être initialisé lors du chargement du fichier
        # pour prendre en compte chaque situation, plusieurs pyqtSignal avec un nombre d'arguments différent est généré
        __MAX_PARAMETERS = 10
        __function = None
        for i in range(__MAX_PARAMETERS + 1):
            exec(f"__signal{i} = QtCore.pyqtSignal(*((object,) * {i}))")
        __signal = None

        # Liste des arguments par défauts et des arguments pour l'appel de la fonction
        __args_list = None
        __args = None

        def __init__(self, function):
            """Fonction permettant d'initialiser le QThread et le décorateur UI.
            Il connecte la fonction au thread principal à l'aide d'un pyqtSignal.

            Parameters
            ----------
            function: `function`
                Fonction influençant un module graphique à connecter avec le thread principal

            Raises
            ------
            RuntimeError
                Jetée lorsque le thread dans lequel l'initialisation se fait n'est pas le thread principal
                ou que la limite d'argument configurée (__MAX_PARAMETERS) n'est pas suffisant"""
            # Initialise le QThread
            super().__init__()
            self.__function = function

            # Chaque élément de la librairie pyQt (ou autre lib graphique) doit être initialisé sur le thread principal
            # Il est donc vital que le QThread et le pyqtSignal soit initialisé sur le thread principal
            # On vérifie donc le "nom" du thread, qui s'appelle "_MainThread" pour le thread principal
            if threading.current_thread().__class__.__name__ != '_MainThread':
                raise RuntimeError("Les composants pyQt doivent obligatoirement être initialisés sur thread principal")

            # Récupère les arguments par défaut)
            signature = inspect.signature(self.__function)
            self.__args_list = {i + 1: (k, v.default) if v.default is not inspect.Parameter.empty else (k,)
                                for i, (k, v) in enumerate(signature.parameters.items())}

            # Si le nombre d'arguments est supérieur au nombre maximum d'arguments, alors jette une erreur
            if len(self.__args_list) > self.__MAX_PARAMETERS:
                raise RuntimeError(f"La fonction envoyée a trop de paramètres. {len(self.__args_list)} nécessaires " +
                                   f"pour {self.__MAX_PARAMETERS} maximums. Changer la valeur de __MAX_PARAMETERS")

            # Sinon connecte la fonction au bon pyqtSignal (index = nombre d'arguments permis)
            exec(f"self.__signal{len(self.__args_list)}.connect(self._UIThread__function)")

            # Pré-compile les exec d'émissions de signal pour une optimisation du temps d'appel du signal
            self.__signal = compile(f"self.__signal{len(self.__args_list)}.emit(*self._UIThread__args)",
                                    filename=f"signal{len(self.__args_list)}",
                                    mode="eval")

        def set_arguments(self, *args, **kwargs):
            """Fonction pour changer les arguments pour le prochain appel de la fonction
            (impossible à envoyer dans la fonction run(), définit par défaut par QThread et appelé avec QThread.start())

            Parameters
            ----------
            *args, **kwargs: Any
                les différents arguments à envoyer lors de l'appel de la fonction

            Raises
            ------
            TypeError:
                Jetée lorsque le nombre d'arguments ne correspond pas au nombre d'arguments de la fonction
            """
            # Transforme le tuple d'argument en une liste
            arguments = list(args)

            # Rajoute le reste des arguments à l'aide de la liste d'argument par défaut, du kwarg et des valeurs défaut
            for i in range(len(arguments) + 1, len(self.__args_list) + 1):
                # Cas où la valeur a été envoyée dans le kwarg
                if self.__args_list[i][0] in kwargs:
                    arguments.append(kwargs[self.__args_list[i][0]])
                # Si elle n'a pas été envoyée, mais qu'une valeur par défaut existe, rajoute une copie
                elif len(self.__args_list[i]) == 2:
                    arguments.append(copy.deepcopy(self.__args_list[i][1]))
                # Sinon la valeur n'a pas été envoyée, laisse un message d'erreur (un crash se produira dans le signal)
                else:
                    log.warning(f"Argument \"{self.__args_list[i][0]}\" manquant dans appel fonction {self.__function}")

            # Reconvertit la liste d'arguments en tuple et le stocke dans la classe
            self.__args = tuple(arguments)

            # # S'assure que le nombre d'argument qui sera envoyé sera le bon
            if len(self.__args_list) != len(self.__args):
                raise TypeError(f"{self.__function} takes {len(self.__args_list)} " +
                                f"positional arguments but {len(args)} was given")

        def run(self):
            """Fonction permettant d'émettre le signal et donc d'appeler la fonction avec les paramètres sauvegardés"""
            # Emet le signal, l'executant et attend qu'il se finisse
            exec(self.__signal)

            # réinitialise les arguments pour éviter de rappeler la fonction avec les mêmes arguments
            self.__args = ()

    # Stocke une instance de la classe précédente
    __ui_thread = None

    def __init__(self, function):
        """fonction appelée lors de l'initialisation de la fonction ciblée par le décorateur

        Parameters
        ----------
        function: `function`
            fonction à appeler de façon sécurisé
        """
        # Initialise le QThread
        self.__ui_thread = self.UIThread(function)

    def __call__(self, *args, **kwargs):
        """fonction appelée lors de l'appel de la fonction ciblée par le décorateur"""
        # Démarre le QThread (appelant sa fonction run() et donc la fonction envoyée) et attend que l'appel se finisse
        self.__ui_thread.set_arguments(*args, **kwargs)
        self.__ui_thread.start()
        self.__ui_thread.wait()

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)
