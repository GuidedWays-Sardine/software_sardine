# Librairies par défaut
import os
import sys
import time


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


def lever_panto(self, database, time=time.time()):
    pass


def manip_de_traction(self, database, time=time.time(), value=0):
    pass
