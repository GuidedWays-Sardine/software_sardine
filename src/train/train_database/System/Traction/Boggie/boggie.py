# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

import src.train.train_database.System.Traction.Boggie.Moteur.moteur as moteur

class Boggie:

    nbressieux = 0
    charge  = 0
    type = 0
    moteur = moteur
    def __init__(self):
        self.nbressieux = 0
        self.charge = 0
        self.type = 0
        self.moteur = moteur.Moteur

        print("enter values: ")
        self.nbressieux = input()
        self.charge = input()
        self.type = input()
