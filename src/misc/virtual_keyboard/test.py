# Librairies par défaut
import os
import sys
import time


# Librairies graphiques
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.virtual_keyboard as vk


if __name__ == "__main__":
    # Initialise le test (registre et application)
    app = QApplication(sys.argv)
    log.initialise(save=False, terminal=True)

    # Génère la fenêtre  et la montre
    engine = QQmlApplicationEngine()
    engine.load(PROJECT_DIR + "\\src\\misc\\virtual_keyboard\\test.qml")
    win = engine.rootObjects()[0]

    # Connecte chacun des composants avec les signaux pour faire apparaitre et disparaitre le clavier numérique
    test_float = win.findChild(QObject, "test_float")
    test_float.focus_gained.connect(lambda: vk.show_keyboard(window=win,
                                                             widget=test_float,
                                                             language=vk.KeyboardMode.NUMPAD,
                                                             skip_list=("-",) if test_float.property("visible_minimum_value") >= 0 else ()))
    test_float.focus_lost.connect(vk.hide_keyboard)

    test_integer = win.findChild(QObject, "test_integer")
    test_integer.focus_gained.connect(lambda: vk.show_keyboard(window=win,
                                                               widget=test_integer,
                                                               language=vk.KeyboardMode.NUMPAD,
                                                               skip_list=("-", ".") if test_integer.property("visible_minimum_value") >= 0 else (".")))
    test_integer.focus_lost.connect(vk.hide_keyboard)

    test_string = win.findChild(QObject, "test_string")
    test_string.focus_gained.connect(lambda: vk.show_keyboard(window=win,
                                                              widget=test_string,
                                                              language=vk.KeyboardMode.FRANCAIS,
                                                              skip_list=["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]))
    test_string.focus_lost.connect(vk.hide_keyboard)

    # Montre et execute l'application
    win.closed.connect(app.quit)
    win.show()
    sys.exit(app.exec())
