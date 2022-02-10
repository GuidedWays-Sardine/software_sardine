# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.train.train_database.database as tdb

class coaches:

class RailCar:
    """classe cotenant toutes les informations sur la voiture"""
    # Toutes les informations générale
    mission_type = None
    position_type = None
    position_index = None   # Index de 0 à Ncoaches - 1

    # Autres informations générales
    levels = 0
    doors = 0
    doors_activable = [[], []]
    doors_open = [[], []]

    # Informations reliées à la masse et la longueur
    Mtare = 0
    Mcurrent = 0
    Mfull = 0
    length = 0

    # Informations reliées aux facteurs A,B,C à vide
    Aempty = 0
    Bempty = 0
    Cempty = 0
    multiply_mass_empty = False

    # Informations reliées aux facteurs A, B, C chargé
    Afull = 0
    Bfull = 0
    Cfull = 0


    def __init__(self):
        self.axle_number = 0

        self.levels = 0
        self.doors = 0

        self.Mtare = 0
        self.Mfull = 0
        self.length = 0

        self.mission_type = None
        self.position_type = None
        self.position_index = None

        self.Aempty = 0
        self.Bempty = 0
        self.Cempty = 0

        self.Afull = 0
        self.Bfull = 0
        self.Cfull = 0