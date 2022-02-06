# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

class Freinage:
    # Define attributes

    type = 0
    Nbr_frein = 0

    def __init__(self):
        self.type = None
        self.Nbr_frein = None

