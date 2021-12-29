# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
class Moteur:

    power = 0
    number = 0

    def __init__(self):
        self.power = 0
        self.number = 0

        print("enter values: ")
        self.power = input()
        self.number = input()

        numero/position/etat/fonctionnel