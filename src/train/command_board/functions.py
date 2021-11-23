# Librairies par défaut
import os
import sys
import time


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


# FEATURE : ajouter les différentes fonctions ici. Chaque fonction doit recevoir :
# - La base de données train pour modifier l'état des systèmes
# - Le temps où le changement d'état a été appelé (par défaut time.time() si pas fournis)
# - Potentiellement une valeur (par exemple pour les sorties analogiques (toujours trouver une valeur par défaut)

def lever_panto(self, database, time=time.time()):
    pass


def manip_de_traction(self, database, time=time.time(), value=0):
    pass
