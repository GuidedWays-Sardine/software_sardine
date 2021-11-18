import pyfirmata
import time
from pyfirmata import Arduino, util

#dans les classes on doit stocker l'etat du bouton et de la led, le pin sur l'arduino du bouton et de led

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
    pin =  None
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