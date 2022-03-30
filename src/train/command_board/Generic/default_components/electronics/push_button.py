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


class PushButton:
    """Classe permettant de controler un bouton poussoir"""
    # Paramètres nécessaires au fonctionnement du bouton poussoir
    __pin = None
    __action_up = None
    __action_down = None

    # Paramètres sur l'état du bouton poussoir
    __state = False
    __previous_states = []
    __lookup = 0
    __THRESHOLD = 1

    @decorators.CommandBoardComponent()
    def __init__(self, board, pin_index, action_down=None, action_up=None, THRESHOLD=1):
        """Fonction permettant d'initialiser une led sur le pupitre (seule ou sur un bouton)

        Parameters
        ----------
        board: `pyfirmata.Board`
            Carte Arduino/Electronique sur lequel le boutton est branchée
        pin_index: `int`
            Index du pinsur lequel le bouton poussoir est connectée (forcément numérique)
        action_down: `actions.Actions`
            Action appelée lorsque le bouton est pressé
        action_up: `actions.Actions`
            Action appelée lorsque le bouton est relachée (par défaut aucune)
        THRESHOLD: `int`
            Nombre de fois que la valeur minimales doit être lu pour être acceptée. Evite les faux-positifs lors des
            lectures des valeurs du bouton mais rajoute un délai de control.DELAY * THRESHOLD

        Raises
        ------
        pyfirmata.InvalidPinDefError:
            Jetée lorsque l'index du pin envoyé ne correspond à aucun pin sur la carte électronique
        pyfirmata.PinAlreadyTakenError:
            Jetée si le pin utilisé par le bouton est déjà utilisé par un autre composant
        TypeError:
            Jetée si l'action envoyée ne correspond à aucune action valide
        """
        # Récupère le pin sur la carte à partir de son index
        self.__pin = board.get_pin(f"d:{int(pin_index)}:i")

        # Enregistre l'action appelée lorsque le bouton est pressé, laisse un message de debug si elle n'est pas bonne
        if isinstance(action_down, actions.Actions):
            self.__action_down = action_down
        elif action_down is not None:
            log.debug(f"L'action' ({action_down}) du bouton poussoir connecté au pin {pin_index} n'est pas valide. " +
                      f"Elle est de type \"{type(action_down)}\" et non de type \"<class \'actions.Actions\'>\"")

        # Enregistre l'action appelée lorsque le bouton est relaché, laisse un message de debug si elle n'est pas bonne
        if isinstance(action_up, actions.Actions):
            self.__action_up = action_up
        elif action_up is not None:
            log.debug(f"L'action ({action_up}) du bouton poussoir connecté au pin {pin_index} n'est pas valide. " +
                      f"Elle est de type \"{type(action_up)}\" et non de type \"<class \'actions.Actions\'>\"")

        # Si aucune des actions n'a été chargée correctement, jette une erreur
        if self.__action_down is None and self.__action_up is None:
            raise TypeError(f"Aucune action du bouton poussoir pin {pin_index} n'a été chargée correctement.")

        # Stocke le seuil nécessaire pour accepter une valeur (la transforme en entier pour éviter tout problème d'index
        if THRESHOLD >= 1:
            self.__THRESHOLD = int(THRESHOLD)

        # Modifie le tableau de valeurs précédemment lues pour qu'il soit de bonnes dimensions
        self.__previous_states = [False] * self.__THRESHOLD

    def add_action(self, actions_list, prepend=False):
        """Fonction permettant de rajouter l'action à la liste d'actions selon l'état actuel du bouton.
        Aucune action ne sera ajoutée si l'état actuel n'a pas d'action ajoutée, et le seuil ne sera pas considéré

        Parameters
        ----------
        actions_list: `list`
            Liste des actions sur laquelle l'action sera ajoutée
        prepend: `bool`
            Indique si l'action doit être traitée en premier ou en dernier
        """
        # Récupère l'état du bouton actuel et si l'action relié à l'état existe, ajoute cette action à la list d'actions
        state = self.read_value()
        if state and self.__action_down is not None:
            # (inséré à l'index 0 si inséré sinon à l'index len(actions_list)
            actions_list.insert(len(actions_list) * (not prepend), [self.__action_down, time.time()])
        elif not state and self.__action_up is not None:
            # (inséré à l'index 0 si inséré sinon à l'index len(actions_list)
            actions_list.insert(len(actions_list) * (not prepend), [self.__action_up, time.time()])

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
        if self.__previous_states[0] is not None and self.__previous_states[0] != self.__state and \
                self.__previous_states.count(self.__previous_states[0]) == len(self.__previous_states):
            # Change l'état du bouton
            self.__state = self.__previous_states[0]

            # Appelle la fonction correspondant (button_up ou button_down) si elle a été fournis
            if self.__state and self.__action_down is not None:
                actions_list.append([self.__action_down, time.time()])
            elif not self.__state and self.__action_up is not None:
                actions_list.append([self.__action_up, time.time()])

    def read_value(self):
        """Fonction permettant de lire la valeur sur le pin du bouton poussoir

        Returns
        -------
        value: `bool`
            la valeur lu sur le bouton poussoir (est-il appuyé)
        """
        return self.__pin.read()
