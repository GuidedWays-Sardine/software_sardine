# Librairies par défaut
import sys
import os
import time
import threading


# Libraires graphiques
from PyQt5.QtWidgets import QApplication


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
from src.misc.log.log_levels import Level
import src.misc.log as log
import src.misc.log.log_window as lw


def main():
    # Initialise le QApplication et le registre
    app = QApplication(sys.argv)
    log.initialise(save=False, log_level=Level.DEBUG)

    # rend la fenêtre frameless
    lw.log_window_frameless(visible=True)

    # génère et lance le thread
    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()

    # Execute l'application
    app.exec()


def worker():
    # Ajoute des messages pour montrer l'interface graphique et l'ajout des messages
    log.info("The application is starting")
    time.sleep(1)
    log.debug("It's still running I swear")
    time.sleep(1)
    log.debug("I'm still running completely fine")
    time.sleep(1)
    log.warning("Look, something weird happened ? Maybe you should look at that")
    time.sleep(1)
    log.debug("Luckily, i'm still running fine")
    time.sleep(1)
    lw.log_window_windowed()
    log.error("Oh wait no my bad I'm not :\n\tError of type : AHHHHHHHHH\n\tWith message : \"I don't feel so good\"")
    time.sleep(1)
    log.add_empty_lines(3)
    log.debug("Really not running well")
    time.sleep(1)
    log.critical('Looks like a critical error! Time to crash')

if __name__ == "__main__":
    main()
