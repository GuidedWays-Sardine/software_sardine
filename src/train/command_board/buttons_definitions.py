# Librairies par défaut
import sys
import os
import time
import threading


# Librairies pour le controle de l'Arduino
import pyfirmata


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.train.command_board.control as control


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

    def __init__(self, board, pin_index, action):
        """Fonction permettant d'initialiser une led sur le pupitre (seule ou sur un bouton)

        Parameters
        ----------
        board: `pyfirmata.Board`
            Carte Arduino/Electronique sur lequel la led est branchée
        pin_index: `int`
            Index sur lequel la led est connectée (forcément numérique)
        action: `control.Actions`
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
        if isinstance(action, control.Actions):
            self.__action = action
        else:
            raise TypeError(f"L'action ({action}) de la LED connectée au pin {int(pin_index)} n'est pas valide. " +
                            f"Elle est de type \"{type(action)}\" et non de type \"<class \'control.Actions\'>\"")

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

    def __init__(self, board, pin_index, action_down=None, action_up=None, THRESHOLD=1):
        """Fonction permettant d'initialiser une led sur le pupitre (seule ou sur un bouton)

        Parameters
        ----------
        board: `pyfirmata.Board`
            Carte Arduino/Electronique sur lequel le boutton est branchée
        pin_index: `int`
            Index du pinsur lequel le bouton poussoir est connectée (forcément numérique)
        action_down: `control.Actions`
            Action appelée lorsque le bouton est pressé
        action_up: `control.Actions`
            Action appelée lorsque le bouton est relachée (par défaut aucune)
        THRESHOLD: `int`
            Nombre de fois que la valeur minimales doit être lu pour être acceptée. Evite les faux-positifs lors des
            lectures des valeurs du bouton mais rajoute un délai de Control.DELAY * THRESHOLD

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
        self.__pin = board.get_pin(f"d:{int(pin_index)}:i")

        # Enregistre l'action appelée lorsque le bouton est pressé, laisse un message de debug si elle n'est pas bonne
        if isinstance(action_down, control.Actions):
            self.__action_down = action_down
        elif action_down is not None:
            log.debug(f"L'action' ({action_down}) du bouton poussoir connecté au pin {pin_index} n'est pas valide. " +
                      f"Elle est de type \"{type(action_down)}\" et non de type \"<class \'control.Actions\'>\"")

        # Enregistre l'action appelée lorsque le bouton est relaché, laisse un message de debug si elle n'est pas bonne
        if isinstance(action_up, control.Actions):
            self.__action_up = action_up
        elif action_up is not None:
            log.debug(f"L'action ({action_up}) du bouton poussoir connecté au pin {pin_index} n'est pas valide. " +
                      f"Elle est de type \"{type(action_up)}\" et non de type \"<class \'control.Actions\'>\"")

        # Si aucune des actions n'a été chargée correctement, jette une erreur
        if self.__action_down is None and self.__action_up is None:
            raise TypeError(f"Aucune action du bouton poussoir pin {pin_index} n'a été chargée correctement.")

        # Stocke le seuil nécessaire pour accepter une valeur (la transforme en entier pour éviter tout problème d'index
        if THRESHOLD >= 1:
            self.__THRESHOLD = int(THRESHOLD)

        # Modifie le tableau de valeurs précédemment lues pour qu'il soit de bonnes dimensions
        self.__previous_states = [False] * self.__THRESHOLD

    def add_action(self, actions_list):
        """Fonction permettant de rajouter l'action à la liste d'actions selon l'état actuel du bouton.
        Aucune action ne sera ajoutée si l'état actuel n'a pas d'action ajoutée, et le seuil ne sera pas considéré

        Parameters
        ----------
        actions_list: `list`
            Liste des actions sur laquelle l'action sera ajoutée
        """
        # Récupère l'état du bouton actuel et si l'action relié à l'état existe, ajoute cette action à la list d'actions
        state = self.read_value()
        if state and self.__action_down is not None:
            actions_list.append([self.__action_down, time.time()])
        elif not state and self.__action_up is not None:
            actions_list.append([self.__action_up, time.time()])

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

    def __init__(self, board, pin_index, action, PRECISION=0, LIMITS=(-1, 1), ERROR=0.002):
        """Fonction permettant d'initialiser une led sur le pupitre (seule ou sur un bouton)

        Parameters
        ----------
        board: `pyfirmata.Board`
            Carte Arduino/Electronique sur lequel le potentiomètre est branchée
        pin_index: `int`
            Index du pin sur lequel le potentiomètre est connectée (forcément numérique)
        action: `control.Actions`
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
            Jeté lorsque l'index du pin envoyé ne correspond à aucun pin sur la carte électronique
        pyfirmata.PinAlreadyTakenError:
            Jeté si le pin utilisé par la LED est déjà utilisé par un autre composant
        TypeError:
            Jeté si l'action envoyée ne correspond à aucune action valide
        """
        # Récupère le pin sur la carte à partir de son index
        self.__pin = board.get_pin(f"a:{int(pin_index)}:i")

        # Sauvegarde l'action permettant de mettre à jour l'état de la LED et jette une erreur si elle n'est pas bonne
        if isinstance(action, control.Actions):
            self.__action = action
        else:
            raise TypeError(f"La fonction ({action}) du potentiomètre connecté au pin A{int(pin_index)} n'est pas valide. " +
                            f"Elle est de type \"{type(action)}\" et non de type \"<class \'control.Actions\'>\"")

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

    def add_action(self, actions_list):
        """Fonction permettant de rajouter l'action à la liste d'actions selon l'état actuel du potentiomètre.

        Parameters
        ----------
        actions_list: `list`
            Liste des actions sur laquelle l'action sera ajoutée
        """
        actions_list.append([self.__action, time.time(), self.read_value()])

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


class SwitchButton:
    pins = []
    pins_state = []
    functions = {}

    def __init__(self, carte, pins, functions):
        for pin in pins:
            self.pins.append(carte.get_pin('d:' + str(pin) + ':i'))
        self.functions = functions
        for func in self.functions:
            if len(self.pins) != len(func):
                log.debug("Cle non valide pour appel de la fonction : " + str(self.functions[func]) + ".\n")
                self.functions.pop(func)

    def add_action(self, actions_list):
        self.read_value()
        try:
            action = self.functions[self.pins_state]
        except KeyError:
            pass
        else:
            if action is not None:
                actions_list.append([action, time.time()])

    def verify_value(self, actions_list):
        old_value = self.pins_state
        self.read_value()
        if old_value != self.pins_state:
            try:
                action = self.functions[self.pins_state]
            except KeyError:
                pass
            else:
                if action is not None:
                    actions_list.append([action, time.time()])

    def read_value(self):
        pins_state = []
        for pin in self.pins:
            pins_state.append(pin.read())
        self.pins_state = tuple(pins_state)

