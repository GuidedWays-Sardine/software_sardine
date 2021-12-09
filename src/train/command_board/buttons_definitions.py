# Librairies par défaut
import sys
import os
import time
import threading


# Librairies pour le controle de l'Arduino
import pyfirmata
from pyfirmata import Arduino, util


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.train.command_board.control as control


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
    pin = None
    button_state = None
    number_of_state = None

    def __init__(self, pin, number_of_state):
        self.pin = pin
        self.number_of_state = number_of_state