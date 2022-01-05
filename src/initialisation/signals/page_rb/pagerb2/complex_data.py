# Librairies par défaut
import os
import sys
import time
from enum import Enum
from typing import Union


#Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd


class Position(Enum):
    """Enum permettant de savoir si la voiture est une voiture avant ou arrière (utile pour savoir l'image à charger"""
    FRONT = "front"
    MIDDLE = "middle"
    BACK = "back"


class MissionType(Enum):
    """Enum permettant de connaitre le type de mission (pour la génération"""
    PASSENGER = "passenger"
    FREIGHT = "freight"


class Coaches:
    """classe cotenant toutes les informations sur la voiture"""
    # Toutes les informations générale
    mission_type = None
    position_type = None
    position_index = None   # Index de 0 à Ncoaches - 1

    # Autres informations générales
    levels = 0
    doors = 0

    # Informations reliées à la masse et la longueur
    Mtare = 0
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
    multiply_mass_full = False

    def __init__(self, mission_type, position_type, position_index, levels, doors, Mtare, Mfull, length,
                 ABCempty, multiply_mass_empty, ABCfull, multiply_mass_full):
        """Fonction permettant d'initialiser une voiture

        Parameters
        ----------
        mission_type: `MissionType`
            Type de mission associé à la voiture
        Position_type: `Position`
            Permet d'indiquer la forme de la voiture (avant : pupitre à gauche ; arrière : pupitre à droite)
        position_index: `int`
            Position de la voiture dans le train
        levels: `int`
            Nombre de niveau dans la voiture (0 si fret, 1 ou 2 si passagers)
        doors: `int`
            Nombre de portes dans la voiture (0 si fret)
        Mtare: `float`
            Masse à vide (en tonnes)
        Mfull: `float`
            Masse à charge maximale (en tonnes)
        length: `float`
            Longueur de la voiture (en mètres)
        ABCempty: `list`
            facteur ABC lorsque le train n'est pas chargé [A (en kN) ; B (en kN/(km/h)) ; C (en kN/(km/h)²)]
        multiply_mass_empty: `bool`
            Indique si les facteurs sans charge doivent être multipliés par la masse du train
        ABCfull: `list`
            facteur ABC lorsque le train est chargé [A (en kN) ; B (en kN/(km/h)) ; C (en kN/(km/h)²)]
        multiply_mass_empty: `bool`
            Indique si les facteurs avec charge doivent être multipliés par la masse du train
        """
        self.mission_type = mission_type
        self.position_type = position_type
        self.position_index = position_index
        self.levels = levels
        self.doors = doors
        self.Mtare = Mtare
        self.Mfull = Mfull
        self.length = length

        if isinstance(ABCempty, list):
            self.Aempty = 0 if len(ABCempty) <= 0 else ABCempty[0]
            self.Bempty = 0 if len(ABCempty) <= 1 else ABCempty[1]
            self.Cempty = 0 if len(ABCempty) <= 2 else ABCempty[2]
        self.multiply_mass_empty = multiply_mass_empty

        if isinstance(ABCfull, list):
            self.Afull = 0 if len(ABCfull) <= 0 else ABCfull[0]
            self.Bfull = 0 if len(ABCfull) <= 1 else ABCfull[1]
            self.Cfull = 0 if len(ABCfull) <= 2 else ABCfull[2]
        self.multiply_mass_full = multiply_mass_full


class Bogie:
    """classe contenant toutes les informations sur le bogie"""
    # Informations générales (masse non stockée car dépendante de la masse voiture)
    position = None
    axles_count = 1
    linked_coaches = []
    motorisation = []
    axle_power = 0.0

    # Informations sur le freinage
    pad_brake_count = 0
    disk_brake_count = 0
    magnetic_brake_count = 0
    fouccault_brake_count = 0

    def __init__(self, position, linked_coaches, axles_count, motorized_axles_count, axle_power, braking_systems_count):
        """Fonction permettant d'initialiser un bogie

        Parameters
        ----------
        position: `Position`
            La position du bogie sur la voiture (Position.FRONT ; Position.MIDDLE ; Position.BACK)
        linked_coaches: `Union[int, list]`
            Liste des voitures auxquelles le bogie est connecté
        axles_count: `int`
            nombre d'essieux
        motorized_axles_count: `Union[list, int]`
            list[bool] -> liste de la position des essieux moteurs (doit être de taille axles_count)
            int -> nombre d'essieux moteurs (doit être inférieur à axles_count)
        axle_power: `float`
            puissance de chacun des moteurs
        braking_systems_count: `list`
            list[int] -> [pad_brake, disk_brake, magnetic_brake, fouccault_brake]
        """
        self.position = position
        if isinstance(linked_coaches, list):
            self.linked_coaches = linked_coaches
        elif isinstance(linked_coaches, int):
            self.linked_coaches = [linked_coaches]
        self.axles_count = axles_count
        self.axle_power = axle_power

        if isinstance(motorized_axles_count, list):
            # Pour chacun des essieux -> lit la motorisation si elle est indiquée sinon la met à False
            self.motorisation = [False if i >= len(motorized_axles_count) else bool(motorized_axles_count[i]) for i in
                                 range(self.axles_count)]
        elif isinstance(motorized_axles_count, int):
            # Motorise les "motorized_axles_count" premier essieux et laissent les autres porteurs
            self.motorisation = [True if i < motorized_axles_count else False for i in range(self.axles_count)]

        if isinstance(braking_systems_count, list):
            self.pad_brake_count = 0 if len(braking_systems_count) <= 0 else braking_systems_count[0]
            self.disk_brake_count = 0 if len(braking_systems_count) <= 1 else braking_systems_count[1]
            self.magnetic_brake_count = 0 if len(braking_systems_count) <= 2 else braking_systems_count[2]
            self.fouccault_brake_count = 0 if len(braking_systems_count) <= 3 else braking_systems_count[3]

    def get_motorized_axles_count(self):
        """Fonction permettant de retourner le nombre d'essieux moteurs

        Returns
        ----------
        Motorized_axles_count: `int`
            Nombre d'essieux motorisés du bogie
        """
        return self.motorisation.count(True)