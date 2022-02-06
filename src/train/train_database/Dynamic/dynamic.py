# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary.settings as sd


class Dynamic:
    # Define attributes

    Along = 0
    Atrans = 0
    Avert = 0
    Jlong = 0
    Jtrans = 0
    Jvert = 0
    Mtransporte = 0
    i = 0
    Pconso = 0
    Mumax = 0
    Musol = 0
    V = 0
    Pk = 0

    def __init__(self, train_data):
        self.Along = 0
        self.Atrans = 0
        self.Avert = 0
        self.Jlong = 0
        self.Jtrans = 0
        self.Jvert = 0
        self.Mtransporte = 0
        self.i = 0
        self.Pconso = 0
        self.Mumax = 0
        self.Musol = 0
        self.V = 0
        self.Pk = 0






