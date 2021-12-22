# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

class Moteur:
    def __init__(self):
        self.power = 0
        self.number = 0

        print("enter values: ")
        self.power = input()
        self.number = input()

class traction:
    # Define attributes
   def __init__(self):
       self.bogie=Bogie.bogie

class Bogie:
    def __init__(self):
        self.nbressieux = 0
        self.charge = 0
        self.type = 0
        self.moteur=Moteur.moteur

        print("enter values: ")
        self.nbressieux = input()
        self.charge = input()
        self.type = input()





