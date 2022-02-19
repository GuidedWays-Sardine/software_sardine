# Librairies par défaut
import os
import sys


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
from src.train.train_database.Systems.frame.railcar.railcar import Railcar


class Frame:
    """classe stockant tous tous les éléments nécessaires à la traction"""
    # Stoque la liste des voitures
    railcars = None

    def __init__(self):
        """Fonction permettant d'initialiser une liste de voitures vide (à remplir ensuite)"""
        self.railcars = []

    def get_railcar(self, index):
        """Fonction permettant de retourner une voiture selon son index

        Parameters
        ----------
        index: `int`
            Index de la voiture (de 0 à Nvoitures -1)

        Returns
        -------
        railcar: `Railcar | None`
            La voiture si elle existe, sinon None
        """
        if isinstance(index, int) and -len(self.railcars) <= index < len(self.railcars):
            return self.railcars[index]
        else:
            log.debug(f"Impossible de retourner la voiture {index}, Le train a que {len(self.railcars)} voitures.")
            return None

    def add_railcar(self, railcar):
        """Fonction permettant de rajouter une voiture à la liste des voitures du système de traction

        Parameters
        ----------
        railcar: `Railcar`
            voiture à rajouter dans la liste de bogies
        """
        if isinstance(railcar, Railcar):
            self.railcars.append(railcar)
        else:
            log.debug(f"voiture envoyée de mauvais type ({type(railcar)} au lieu de Railcar).")

    # Aucune fonction pour enlever une voiture car trop dangereux pour le fonctionnement de la dynamique

    def get_mission_list(self):
        """Fonction retournant la liste des missions de chacunes des voitures

        Returns
        -------
        mission_list: `list`
            liste des missions de chacunes des voitures du train
        """
        return [rc.mission_type.value for rc in self.railcars]

    def get_position_list(self):
        """Fonction retournant la liste des tupes de positions (Front, Middle, Back) de chacunes des voitures

        Returns
        -------
        mission_list: `list`
            liste des types de positions de chacunes des voitures du train
        """
        return [rc.position_type.value for rc in self.railcars]
