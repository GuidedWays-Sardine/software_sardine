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
    button_pin = None
    led_pin = None
    action_up = None
    action_down = None
    button_state = None
    led_state = None
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
        if self.led_pin is not None:
            if frequency != 0:
                self.frequency = frequency
                led_blinking = threading.Thread(target=self.blinking_led, daemon=True)
                led_blinking.start()
            else:
                self.led_pin.write(led_state)
                self.led_state = led_state
                self.frequency = 0

    def read_value(self):
        self.button_state = self.button_pin.read()

    def blinking_led(self):
        change_state_time = 1/(2*self.frequency)
        while self.frequency != 0:
            self.led_pin.write(not self.led_state)
            self.led_state = not self.led_state
            time.sleep(change_state_time)

class Potentiometer:
    pin = None
    state = None

    def __init__(self, pin):
        self.pin = pin


class SwitchButton:
    pin = None
    button_state = None
    number_of_state = None

    def __init__(self, pin, number_of_state):
        self.pin = pin
        self.number_of_state = number_of_state