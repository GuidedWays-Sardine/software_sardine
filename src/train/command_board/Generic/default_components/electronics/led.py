# Librairies par défaut
import sys
import os
import time
import threading


# Librairies pour le controle de l'Arduino
import pyfirmata


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.train.command_board.Generic.actions.actions as actions
import src.misc.decorators.decorators as decorators


class LED:
    """Classe permettant de controler une LED"""
    # Cadenas permettant d'éviter les data races lors du clignotement de la LED (pour pin, state, frequency)
    lock = threading.Lock()

    # Paramètres nécessaires au fonctionnement de la LED
    __pin = None
    __action = None

    # Paramètres d'état de la LED
    __state = False
    __half_period = 0

    @decorators.CommandBoardComponent()
    def __init__(self, board, pin_index, action):
        """Fonction permettant d'initialiser une led sur le pupitre (seule ou sur un bouton)

        Parameters
        ----------
        board: `pyfirmata.Board`
            Carte Arduino/Electronique sur lequel la led est branchée
        pin_index: `int`
            Index sur lequel la led est connectée (forcément numérique)
        action: `actions.Actions`
            Action permettant de controller la LED (appelée à chaque mise à jour logique)

        Raises
        ------
        pyfirmata.InvalidPinDefError:
            Jeté lorsque l'index du pin envoyé ne correspond à aucun pin sur la carte électronique
        pyfirmata.PinAlreadyTakenError:
            Jeté si le pin utilisé par la LED est déjà utilisé par un autre composant
        TypeError:
            Jeté si l'action envoyée ne correspond à aucune action valide
        """
        # Récupère le pin à partir de son index
        self.__pin = board.get_pin(f"d:{int(pin_index)}:o")

        # Sauvegarde l'action permettant de mettre à jour l'état de la LED et jette une erreur si elle n'est pas bonne
        if isinstance(action, actions.Actions):
            self.__action = action
        else:
            raise TypeError(f"L'action ({action}) de la LED connectée au pin {int(pin_index)} n'est pas valide. " +
                            f"Elle est de type \"{type(action)}\" et non de type \"<class \'actions.Actions\'>\"")

    def add_action(self, actions_list):
        """Fonction permettant d'ajouter l'appel d'une action dans la liste d'action

        Parameters
        ----------
        actions_list: `list`
            Liste des actions à executer lors de la prochaine mise à jour logique
        """
        # Ajoute une action avec : l'action demandée, le pin (pour controller la LED) et le temps de demande du bouton
        actions_list.append([self.__action, self.__pin, time.time()])

    def change_led_state(self, led_state=False, frequency=0):
        """Fonction permettant de changer l'état de la LED

        Parameters
        ----------
        led_state: `bool`
            Nouvel état de la LED (par défaut False pour l'éteindre)
        frequency: `float`
            fréquence de clignotement, pris en compte que si led_state à True (par défaut à 0 pour aucun clignotement)
        """
        # bloque le cadenas le temps du changement d'état de la LED pour éviter les data races
        with self.lock:
            # Cas d'un clignotement de la LED
            if led_state and frequency > 0:
                # Calcule la half période
                self.__half_period = 0.5 / frequency

                # Crée un thread avec la fonction de clignotement et le lance
                # Thread daemon pour que l'application puisse se fermer même si le thread tourne encore
                led_blink = threading.Thread(target=self.__blink, daemon=True)
                led_blink.start()
            else:
                self.__half_period = 0
                self.__pin.write(led_state)
                self.__state = led_state

    def __blink(self):
        """Fonction (privée) permettant de faire clignoter la LED. Pour l'initier, appeler change_led_state"""
        # Initialise la variable pour indiquer si la LED clignotte encore (si la half période est strictement positive)
        is_blinking = self.__half_period > 0

        # Tant que la led doit encore clignoter
        while is_blinking:
            # Bloque le thread temporairement et inver l'état de la LED
            with self.lock:
                self.__pin.write(not self.__state)
                self.__state = not self.__state

            # Attends une demie période
            time.sleep(self.__half_period)

            # Réactualise la variable is_blinking
            with self.lock:
                is_blinking = (self.__half_period > 0)
