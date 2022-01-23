# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

class coaches:

    mass = 0
    position = None
    nombre_essieux = 0
    longueur = 0
    largeur = 0

    def __init__(self):
        self.mass = 0
        self.position = None
        self.nombre_essieux = 0
        self.longueur = 0
        self.largeur = 0

        print("enter values: ")
        self.mass = input()
        self.position = input()
        self.nombre_essieux = input()
        self.longueur = input()
        self.largeur = input()