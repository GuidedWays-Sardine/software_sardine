# Librairies par défaut python
import sys
import os
import Dynamic.dynamic


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


import src.train.train_database.Dynamic.dynamic as dynamic
import src.train.train_database.Static.static as static
import src.train.train_database.System.system as system

class TrainDatabase:
    # Données du train

    dynamic = None
    static = None
    system = None

    def __init__(self):
        self.dynamic = dynamic.Dynamic()
        self.static = static.Static()
        self.system = system.System()



