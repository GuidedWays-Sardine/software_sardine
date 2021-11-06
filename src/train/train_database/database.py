# Librairies par défaut python
import sys
import os
import threading


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


class TrainDatabase:
    # Données du train
    lock = threading.Lock()
    speed = 0


    # TODO : travailler la structure et rajouter tous les


    def __init__(self, train_data):
        #TODO : faire une fonction qui récupère les données du trains et qui complète la base de donnée
        with self.lock:
            log.info("Début de l'initialisation de la base de donnée train.", prefix="Train database")
