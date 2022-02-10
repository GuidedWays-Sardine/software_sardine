# Librairies par défaut python
# Librairies par défaut python
import sys
import os



# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.train.train_database.database as tdb


class Bogie:
    """classe contenant toutes les informations sur le bogie"""
    # Informations générales
    position_type = None
    position_index = -1  # Uniquement pour les bogies centraux! Les bogies extérieurs n'ont pas d'index
    axles_count = 1
    linked_coaches = []

    # Informations sur la motorisation
    axles_power = []     # Puissance du moteur, sinon 0 si aucun moteur
    activated = []      # True si le moteur est allumé, False sinon
    activable = []      # True si le moteur est activable, False sinon (si panne)

    def __init__(self):
        self.axle_count = 0
        self.axle_power = 0
        self.motor_position = None
        self.state = None
        self.ignitable = None
        self.linked_coaches = None
        self.power = None
        self.type = None
        self.bogie_mass = 0










