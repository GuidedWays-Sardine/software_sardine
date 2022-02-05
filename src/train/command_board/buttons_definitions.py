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
    # Cadenas permettant d'éviter les data races lors du clignotement de la LED (pour led_pin, led_state, frequency)
    lock = threading.Lock()

    button_pin = None
    led_pin = None
    action_up = None
    action_down = None
    button_state = False
    led_state = False
    frequency = 0

    def __init__(self, carte, button_pin, led_pin=None, action_up=None, action_down=None):
        self.button_pin = carte.get_pin('d:' + str(button_pin) + ':i')
        self.led_pin = carte.get_pin('d:' + str(led_pin) + ':o') if led_pin is not None else None
        self.action_up = action_up
        self.action_down = action_down

    def add_value(self, actions_list):
        self.read_value()
        if self.button_state and self.action_down is not None:
            actions_list.append([self.action_down, time.time()])
        elif not self.button_state and self.action_up is not None:
            actions_list.append([self.action_up, time.time()])

    def verify_value(self, actions_list):
        old_state = self.button_state
        self.read_value()
        if old_state != self.button_state:
            if self.button_state and self.action_down is not None:
                actions_list.append([self.action_down, time.time()])
            elif not self.button_state and self.action_up is not None:
                actions_list.append([self.action_up, time.time()])

    def change_led_state(self, led_state=False, frequency=0):
        # bloque le cadenas le temps du changement d'état de la LED pour éviter les data races
        with self.lock:
            if self.led_pin is not None:
                if frequency > 0:
                    self.frequency = frequency
                    led_blinking = threading.Thread(target=self.__blinking_led, daemon=True)
                    led_blinking.start()
                else:
                    self.led_pin.write(led_state)
                    self.led_state = led_state
                    self.frequency = 0

    def read_value(self):
        self.button_state = self.button_pin.read()

    def __blinking_led(self):
        """Fonction permettant de faire clignoter la led du bouton (si celle-ci existe)
        Attention, cette fonction bloque le thread courrant jusqu'à ce que frequency soit changé.
        """
        # Revérifie que le bouton a bien une led
        if self.led_pin is not None:
            # Récupère le temps entre chaque changement d'état et crée variable pour savoir si la led doit encore clignoter
            change_state_time = 1/(2*self.frequency)
            with self.lock:
                is_blinking = self.frequency != 0

            # Tant que la LED doit clignoter, clignote
            while is_blinking:
                # Inverse l'état de la LED (en bloquant les autres fonctions de lire sur les variables du bouton)
                with self.lock:
                    self.led_pin.write(not self.led_state)
                    self.led_state = not self.led_state

                # Attends la moite d'une période (pour faire clignoter la LED à la bonne fréquence)
                time.sleep(change_state_time)

                # Vérifie que la LED doit toujours clignoter (toujours en bloquand la class pour éviter les data races)
                with self.lock:
                    is_blinking = self.frequency != 0


class Potentiometer:
    pin = None
    action = None
    value = None

    max_value = 1023
    error = 0

    def __init__(self, carte, pin, action, max_value=1023, error=0):
        self.pin = carte.get_pin('a:' + str(pin) + ':i')
        self.action = action
        self.max_value = max_value
        self.error = error

    def add_action(self, actions_list):
        self.read_value()
        actions_list.append([self.action, time.time(), self.value])

    def verify_value(self, actions_list):
        old_value = self.value
        self.read_value()
        if old_value != self.value:
            actions_list.append([self.action, time.time(), self.value])

    def read_value(self):
        value = (self.pin.read() - self.max_value * 0.5) / (self.max_value * 0.5)
        self.value = value * (value < -self.error or value > self.error)


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

