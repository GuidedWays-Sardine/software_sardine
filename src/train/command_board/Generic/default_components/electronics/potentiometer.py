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


class Potentiometer:
    """Classe permettant de controller un bouton de type potentiomêtre (entrée analogique)"""
    # Paramètres nécessaires au fonctionnement du potentiomètre
    __pin = None
    __action = None
    __value = 0

    # Constantes sur le nombre de valeurs (précision de lecture) et sur les bornes de sorties de la valeur [min, max]
    __PRECISION = 1024
    __LIMITS = (-1, 1)
    __ERROR = 0.002

    @decorators.CommandBoardComponent()
    def __init__(self, board, pin_index, action, PRECISION=0, LIMITS=(-1, 1), ERROR=0.002):
        """Fonction permettant d'initialiser une led sur le pupitre (seule ou sur un bouton)

        Parameters
        ----------
        board: `pyfirmata.Board`
            Carte Arduino/Electronique sur lequel le potentiomètre est branchée
        pin_index: `int`
            Index du pin sur lequel le potentiomètre est connectée (forcément numérique)
        action: `actions.Actions`
            Action à appeler. Cette fonction doit prendre la valeur du potentiomètre en quatirème argument
        PRECISION: `int`
            Nombre de valeurs maximales que le potentiomètre peut lire (généralement 1024)
        LIMITS: `tuple`
            Liste de deux floats contenant la valeur minimale et maximale que le potentiomètre doit retourner.
            Toutes les valeurs seront linéairement répartis sur l'intervale fourni (par défaut -1 -> 1)
        ERROR: `float`
            différence de valeur (sur la valeur corrigée) à partir de laquelle un changement de valeur est considéré

        Raises
        ------
        pyfirmata.InvalidPinDefError:
            Jetée lorsque l'index du pin envoyé ne correspond à aucun pin sur la carte électronique
        pyfirmata.PinAlreadyTakenError:
            Jetée si le pin utilisé par la LED est déjà utilisé par un autre composant
        TypeError:
            Jetée si l'action envoyée ne correspond à aucune action valide
        """
        # Récupère le pin sur la carte à partir de son index
        self.__pin = board.get_pin(f"a:{int(pin_index)}:i")

        # Sauvegarde l'action permettant de mettre à jour l'état de la LED et jette une erreur si elle n'est pas bonne
        if isinstance(action, actions.Actions):
            self.__action = action
        else:
            raise TypeError(f"La fonction ({action}) du potentiomètre connecté au pin A{int(pin_index)} n'est pas valide. " +
                            f"Elle est de type \"{type(action)}\" et non de type \"<class \'actions.Actions\'>\"")

        # Stocke la précision (si fausse, les valeurs sortiront des limites) et l'erreur sans faire de vérifications
        self.__PRECISION = PRECISION
        self.__ERROR = ERROR

        # Stocke les valeurs limites, en les inversants si la valeur minimale est supérieure à la valeur maximale
        if len(LIMITS) == 2 and LIMITS[0] > LIMITS[1]:
            self.__LIMITS = tuple(reversed(LIMITS))
        elif len(LIMITS) == 2:
            self.__LIMITS = LIMITS
        else:
            log.debug(f"Limite par défaut gardé pour le potentiomètre connecté au pin {int(pin_index)}. " +
                      f"{LIMITS} ne contient pas les 2 bornes nécessaires")

    def add_action(self, actions_list, prepend=False):
        """Fonction permettant de rajouter l'action à la liste d'actions selon l'état actuel du potentiomètre.

        Parameters
        ----------
        actions_list: `list`
            Liste des actions sur laquelle l'action sera ajoutée
        prepend: `bool`
            Indique si l'action doit être traitée en premier ou en dernier
        """
        # Ajoute l'action avec la valeur lu (début sinon fin)
        actions_list.insert(len(actions_list) * (not prepend), [self.__action, time.time(), self.read_value()])

    def verify_value(self, actions_list):
        """Fonction permettant de lire la valeur et si elle est différentes (au seuil de ERROR), ajoute l'action.

        Parameters
        ----------
        actions_list: `list`
            Liste des actions sur laquelle l'action sera potentiellement ajoutée
        """
        # Stocke temporairement l'ancienne valeur et lit la nouvelle valeur sur le potentiomètre
        old_value = self.__value
        self.read_value()

        # Si la nouvelle valeur lu se trouve en dehors de l'invervale +- erreur, ajoute l'action à la liste d'actions
        if self.__value < (old_value - self.__ERROR) or self.__value > (old_value + self.__ERROR):
            actions_list.append([self.__action, time.time(), self.__value])

    def read_value(self):
        """Lit la valeur du potentiomètre, la change dans la classe et la retourne

        Returns
        -------
        value: `float`
            la valeur lu corrigée
        """
        self.__value = self.__LIMITS[0] + self.__pin.read() * (self.__LIMITS[1] - self.__LIMITS[0]) / self.__PRECISION
        return self.__value
