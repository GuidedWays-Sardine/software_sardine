# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

import src.train.train_database.System.Traction.traction as traction
import src.train.train_database.System.Freinage.freinage as freinage
import src.train.train_database.System.Electric_system

class System:

    traction = traction
    freinage = freinage

    def __init__(self):
        self.freinage = freinage.Freinage()
        self.traction = traction.Traction()

