# Librairies par défaut python
import sys
import os
from enum import Enum


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

class Position(Enum):
    Front = "front"
    Middle = "middle"
    Back = "back"

class Boggie:

    nbressieux = 0
    nbressieux_moteur = 0
    charge  = 0
    puissance = 0
    etat = 0
    type = None
    position = 0
    boggie_mass = 0

    def __init__(self):
        self.nbressieux = 0
        self.nbressieux_moteur = 0
        self.charge = 0
        self.puissance = 0
        self.type = None
        self.position = 0
        self.boggie_mass = 0

        print("enter values: ")
        self.nbressieux = input()
        self.nbressieux_moteur = input()
        self.charge = input()
        self.puissance = input()
        self.type = input()
        self.position = input()
        self.boggie_mass = input()
