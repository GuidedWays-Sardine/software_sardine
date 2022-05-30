# librairies par défaut
import os
import sys
import threading
import time


# Librairies graphiques
from PyQt5.QtWidgets import QApplication


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.immersion as immersion


def random_print():
    for i in range(10):
        print(i)
        time.sleep(1)


def worker():
    # Fais des essais pour différents skip list
    for s_l in [(), (2,)]:
        immersion.change_skip_list(s_l, immersion.Mode.DEACTIVATED)
        time.sleep(0.5)
        immersion.change_mode(immersion.Mode.LOADING)
        time.sleep(immersion.loading_duration())
        print(f"loading done : {immersion.loading_duration()}")
        immersion.change_mode(immersion.Mode.STILL)
        time.sleep(3)
        immersion.change_mode(immersion.Mode.UNLOADING)
        time.sleep(immersion.unloading_duration())
        print(f"unloading done : {immersion.unloading_duration()}")
        immersion.change_mode(immersion.Mode.EMPTY)
        time.sleep(3)


if __name__ == "__main__":
    # Create the application, a thread to do the actions and starts the application
    app = QApplication(sys.argv)
    log.initialise(save=True, terminal=True)
    immersion.initialise_immersion_windows()

    immersion.change_mode(immersion.Mode.LOADING, function=random_print)

    worker_thread = threading.Thread(target=worker)
    worker_thread.start()

    app.exec()
