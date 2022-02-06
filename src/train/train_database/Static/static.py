# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary.settings as sd


class Static:

    A = 0
    B = 0
    C = 0
    MuO = 0
    k = 0
    type = 0


    def __init__(self, train_data):
        self.A = 0
        self.B = 0
        self.C = 0
        self.MuO = 0
        self.k = 0
        self.type = 0

