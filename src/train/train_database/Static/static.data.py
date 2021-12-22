# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

class static:
    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.MuO = 0
        self.k = 0
        self.type = 0

        print("enter values: ")
        self.A = input()
        self.B = input()
        self.C = input()
        self.Musol = input()
        self.k = input()
        self.type = input()