# Librairies par défaut
import sys
import os
import time


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
    button_state = None
    led_state = None

    def __init__(self, button_pin, led_pin=None, led_state=False):
        self.button_pin = button_pin
        self.led_pin = led_pin
        self.led_state = led_state

    def action(self, button, led):
        pressed = False
        led_on = False

        while True:
            if pressed != button.read():
                pressed = not pressed
                if pressed:
                    led_on = not led_on
                    led.write(led_on)

                print(pressed)
            time.sleep(0.05)


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