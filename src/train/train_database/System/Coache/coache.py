# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

class coaches:

    axle_number = 0

    levels = 0
    doors = 0

    Mtare = 0
    Mfull = 0
    length = 0

    mission_type = None
    position_type = None
    position_index = None

    Aempty = 0
    Bempty = 0
    Cempty = 0

    Afull = 0
    Bfull = 0
    Cfull = 0


    def __init__(self):
        self.axle_number = 0

        self.levels = 0
        self.doors = 0

        self.Mtare = 0
        self.Mfull = 0
        self.length = 0

        self.mission_type = None
        self.position_type = None
        self.position_index = None

        self.Aempty = 0
        self.Bempty = 0
        self.Cempty = 0

        self.Afull = 0
        self.Bfull = 0
        self.Cfull = 0