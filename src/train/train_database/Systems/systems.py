# Librairies par défaut python
import sys
import os
from enum import Enum


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

import src.misc.settings_dictionary.settings as sd
import src.train.train_database.database as tdb
import src.train.train_database.Systems.traction.traction as traction
import src.train.train_database.Systems.braking.braking as freinage
import src.train.train_database.Systems.railcar.railcar as railcar
import src.train.train_database.Systems.electric.electric as electric


class Systems:

    railcars = []
    electric = []
    traction = []
    braking = []

    def __init__(self, train_data):
        pass
