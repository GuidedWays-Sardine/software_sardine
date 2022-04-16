# Librairies par défaut
import sys
import os
import threading
import time


# Librairies graphiques
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.window_manager as wm
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd


def main():
    # Initialise le registre pour récupérer de potentielles erreurs des fichiers QML
    log.initialise(save=False)
    settings = sd.SettingsDictionary()

    # Initialiser une application et une fenêtre QML et python
    app = QApplication(sys.argv)
    win_python = QMainWindow()
    engine = QQmlApplicationEngine()
    engine.load(f"{PROJECT_DIR}src/misc/visual_position/test.qml")
    win_qml = engine.rootObjects()[0]

    wm.get_window_position(win_qml, settings, "win_qml")
    wm.get_window_position(win_python, settings, "win_py")
    log.info(str(settings))

    # Génère deux thread pour positioner et placer les différentes fenêtres et les lancent
    thread = threading.Thread(target=worker, daemon=True, args=(win_python, win_qml))
    thread.start()

    # Execute l'applcation
    win_python.show()
    win_qml.show()
    app.exec()

    # Arrête le registre pour éviter l'erreur de segmentation
    log.stop()


def worker(win_python, win_qml):
    settings = sd.SettingsDictionary()

    # Fais les premiers essais avec la fenêtre QMainWindow
    log.info("Essais sur la fenêtre python (QMainWindow).")
    for i in range(5):
        # Do some random tests
        wm.get_window_position(win_python, settings, f"test{i}")
        time.sleep(0.5)
        wm.set_window_position(window=win_python,
                               settings={"test.screen_index": 1,
                                         "test.x": 35 * i,
                                         "test.y": 35 * i,
                                         "test.w": 300,
                                         "test.h": 210},
                               key=f"test")
        time.sleep(0.5)
    log.info(str(settings) + "\n")

    # Refais les premiers essais avec la fenêtre QMainWindow
    log.info("Essais sur la fenêtre qml (QWindow).")
    for i in range(5):
        # Do some random tests
        wm.get_window_position(win_qml, settings, f"test{i}")
        time.sleep(0.5)
        wm.set_window_position(window=win_qml,
                               settings={"test.screen_index": 1,
                                         "test.x": 35 * i,
                                         "test.y": 35 * i,
                                         "test.w": 300,
                                         "test.h": 210},
                               key=f"test")
        time.sleep(0.5)
    log.info(str(settings))


if __name__ == "__main__":
    main()
