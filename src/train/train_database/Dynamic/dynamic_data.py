# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

class dynamic:
    # Define attributes
    def __init__(self):
        self.A = []
        self.J = []
        self.Mtransporte = 0
        self.i = 0
        self.Pconso = 0
        self.Mumax = 0
        self.Musol = 0
        self.V = 0
        self.Pk = 0

        for i in range(0, 3):
            print("Value for A" + str(i) + " : ")
            self.A.append(input())
        for j in range(0, 2):
            print("Value for J" + str(j) + " : ")
            self.J.append(input())
        print("Value for Mtranporte : ")
        self.Mtransporte = input()
        self.i = input()
        self.Pconso = input()
        self.Mumax = input()
        self.Musol = input()
        self.V = input()
        self.Pk = input()






