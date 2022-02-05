# Librairies par défaut
import sys
import os
import time


# Librairies pour le controle de l'Arduino
import pyfirmata


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.train.command_board.Generic.actions.actions as actions
import src.misc.decorators.decorators as decorators


class SwitchButton:
    """Classe permettant de controller un boutton multiposition"""
    # Paramètres nécessaires au fonctionnement du bouton multiposition
    __pins = ()
    __actions = {}

    # Paramètres sur l'état du bouton multiposition
    __state = ()
    __previous_states = []
    __lookup = 0
    __THRESHOLD = 1

    @decorators.CommandBoardComponent()
    def __init__(self, board, pins_index, actions_list, THRESHOLD=1):
        """Fonction permettant d'initialiser une led sur le pupitre (seule ou sur un bouton)

        Parameters
        ----------
        board: `pyfirmata.Board`
            Carte Arduino/Electronique sur lequel le boutton est branchée
        pins_index: `tuple`
            Index des pins sur lesquel le bouton multiposition est connectée (forcément numérique)
        actions_list: `dict`
            Liste des actions à appeler selon les valeurs lus sur les pins. Clés = tuple des entrées -> valeurs : Action
        THRESHOLD: `int`
            Nombre de fois que la valeur minimales doit être lu pour être acceptée. Evite les faux-positifs lors des
            lectures des valeurs du bouton mais rajoute un délai de actions.DELAY * THRESHOLD

        Raises
        ------
        pyfirmata.InvalidPinDefError:
            Jeté lorsque l'index du pin envoyé ne correspond à aucun pin sur la carte électronique
        pyfirmata.PinAlreadyTakenError:
            Jeté si le pin utilisé par le bouton est déjà utilisé par un autre composant
        TypeError:
            Jeté si l'action envoyée ne correspond à aucune action valide
        """
        # Récupère le pin sur la carte à partir de son index
        self.__pins = tuple([board.get_pin(f"d:{pins_index[p_i]}:i") for p_i in pins_index])

        # Enregistre chacune des actions valides dans le dictionnaire des actions
        for key, action in actions_list.items():
            # Vérifie que l'action est bien une action
            if isinstance(action, actions.Actions):
                # Vérifie que les entrées sont bien au bon nombre
                if len(key) == len(self.__pins):
                    # Ajoute alors la fonction et ses clés au dictionnaire des actions
                    self.__actions[key] = action
                else:
                    log.debug(f"pas suffisament de valeurs pour la clé : {key}: {action}. " +
                              f"{len(key)} valeurs {key} au lieu des {len(self.__pins)} {pins_index} requis.")
            else:
                log.debug(f"L'action ({action}) du bouton multiposition relié aux positions {key}, " +
                          f" connecté aux pins {pins_index} n'est pas valide. " +
                          f" Elle est de type \"{type(action)}\" et non de type \"<class \'actions.Actions\'>\"")

        # Si aucune des actions n'a été chargée correctement, jette une erreur
        if not self.__actions:
            raise TypeError(f"Aucune action du bouton multiposition pins {pins_index} n'a été chargée correctement.")

        # Stocke le seuil nécessaire pour accepter une valeur (la transforme en entier pour éviter tout problème d'index
        if THRESHOLD >= 1:
            self.__THRESHOLD = int(THRESHOLD)

        # Modifie le tableau de valeurs précédemment lues pour qu'il soit de bonnes dimensions
        self.__previous_states = [(False,) * len(self.__pins)] * self.__THRESHOLD

    def add_action(self, actions_list):
        """Fonction permettant de rajouter l'action à la liste d'actions selon la position du bouton multiposition.
        Aucune action ne sera ajoutée si l'état actuel n'a pas d'action ajoutée, et le seuil ne sera pas considéré

        Parameters
        ----------
        actions_list: `list`
            Liste des actions sur laquelle l'action sera ajoutée
        """
        # Lit la valeur et la stocke dans la variable
        state = self.read_value()

        # Essaye de rajouter l'action correspondant à la valeur lu. Si une erreur est jetée, c'est qu'aucune n'est là
        try:
            actions_list.append([self.__actions[state], time.time()])
        except Exception:
            pass

    def verify_value(self, actions_list):
        """Fonction permettant de lire la valeur et si elle est différentes pour plus de THRESHOLD fois,
        ajouter l'action associée (si elle existe) à la liste d'actions.

        Parameters
        ----------
        actions_list: `list`
            Liste des actions sur laquelle l'action sera potentiellement ajoutée
        """
        # Lit la valeur et la stocke dans la case du tableau pointée, et passe à la case suivante
        self.__previous_states[self.__lookup] = self.read_value()
        self.__lookup = (self.__lookup + 1) % self.__THRESHOLD      # 0 -> 1 -> ... -> THRESHOLD - 1 -> 0 -> 1 -> ...

        # Si toutes les valeurs sont identiques et ne valent pas None (erreur de lecture) ou la valeur précédente
        if not any([p_s is None for p_s in self.__previous_states[0]]) and self.__previous_states[0] != self.__state and \
                self.__previous_states.count(self.__previous_states[0]) == len(self.__previous_states):
            # Change l'état du bouton
            self.__state = self.__previous_states[0]

            # Ajoute la fonction correspondante à la liste d'actions si elle existe
            try:
                actions_list.append([self.__actions[self.__state], time.time()])
            except Exception:
                pass

    def read_value(self):
        """Fonction permettant de lire les valeur sur les pins du bouton multiposition

        Returns
        -------
        value: `tuple`
            Les valeurs lus sur les différents pins du bouton multiposition
        """
        # Récupère les valeurs pour chacun des pins, les convertits en tuples et les retournes
        return tuple([pin.read() for pin in self.__pins])
