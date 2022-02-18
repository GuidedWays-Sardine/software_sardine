# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.train.train_database.database as tdb


class Railcar:
    """classe cotenant toutes les informations sur la voiture"""
    # Toutes les informations générale
    mission_type = None
    position_type = None
    position_index = None   # Index de 0 à Nrailcars - 1

    # Autres informations générales
    levels = 0
    doors = 0
    doors_activable = None      # format [[bool, ...], [bool, ...]] -> [[portes gauches], [portes droites]]
    doors_open = None           # format [[bool, ...], [bool, ...]] -> [[portes gauches], [portes droites]]

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
    multiply_mass_full = False

    def __init__(self, mission_type, position_type, position_index, levels, doors, Mtare, Mfull, length,
                           ABCempty, multiply_mass_empty, ABCfull, multiply_mass_full):
        """Fonction permettant d'initialiser une voiture

        Parameters
        ----------
        mission_type: `tdb.MissionType`
            Type de mission associé à la voiture
        position_type: `tdb.Position`
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
        multiply_mass_full: `bool`
            Indique si les facteurs avec charge doivent être multipliés par la masse du train
        """
        self.set_general_values(mission_type, position_type, position_index, levels, doors, Mtare, Mfull, length,
                                ABCempty, multiply_mass_empty, ABCfull, multiply_mass_full)

    def set_general_values(self, mission_type, position_type, position_index, levels, doors, Mtare, Mfull, length,
                           ABCempty, multiply_mass_empty, ABCfull, multiply_mass_full):
        """Fonction permettant de mettre à jour les paramètres d'une voiture

        Parameters
        ----------
        mission_type: `tdb.MissionType`
            Type de mission associé à la voiture
        position_type: `tdb.Position`
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
        multiply_mass_full: `bool`
            Indique si les facteurs avec charge doivent être multipliés par la masse du train
        """
        # Change les informations sur le type de missions de la voiture et sa position
        self.mission_type = mission_type
        self.position_type = position_type
        self.position_index = position_index

        # Change le nombre de portes et de niveaux et initialise si les portes sont fonctionnemles ou non
        self.levels = levels
        self.doors = doors
        self.doors_open = [[False] * self.doors, [False] * self.doors]
        self.doors_activable = [[True] * self.doors, [True] * self.doors]

        # Initialise les informations sur la masse
        self.Mtare = Mtare
        self.Mfull = Mfull
        if self.Mcurrent > self.Mfull or self.Mcurrent < self.Mtare:
            self.Mcurrent = self.Mfull if self.Mcurrent > self.Mfull else self.Mtare
        self.length = length

        # Initialise les facteurs ABC
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

    def get_general_values(self):
        """Fonction permettant de retourner toutes les valeurs de paramétrages voiture

        Returns
        -------
        qml_values: `list`
            (mission_type, position_type, position_index, levels, doors, Mtare, Mfull, length,
            Aempty, Bempty, Cempty, multiply_mass_empty,
            Afull, Bfull, Cfull, multiply_mass_full)
        """
        return (self.mission_type, self.position_type, self.position_index,  self.levels, self.doors, self.Mtare, self.Mfull, self.length,
                self.Aempty, self.Bempty, self.Cempty, self.multiply_mass_empty,
                self.Afull, self.Bfull, self.Cfull, self.multiply_mass_full)
