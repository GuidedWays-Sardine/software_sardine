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


mission_getter = {i: key for i, key in enumerate(MissionType)}


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

    def get_qml_values(self):
        """Fonction permettant de retourner les valeurs au format qml

        Returns
        -------
        qml_values: `list`
            [levels, doors, Mtare, Mfull, length, Aempty, Bempty, Cempty, multiply_mass_empty, Afull, Bfull, Cfull, multiply_mass_full]
        """
        return [self.levels, self.doors, self.Mtare, self.Mfull, self.length,
                self.Aempty, self.Bempty, self.Cempty, self.multiply_mass_empty,
                self.Afull, self.Bfull, self.Cfull, self.multiply_mass_full]

    def read_qml_values(self, qml_values):
        """Fonction permettant de lire les valeurs au format qml

        Parameters
        ----------
        qml_values: `list`
            [levels, doors, Mtare, Mfull, length, Aempty, Bempty, Cempty, multiply_mass_empty, Afull, Bfull, Cfull, multiply_mass_full]
        """
        # Rajoute une vérification pour s'assurer que  la taille du tableau de valeurs est dans les bonnes dimensions
        if isinstance(qml_values, list) and len(qml_values) == 13:
            self.levels = qml_values[0]
            self.doors = qml_values[1]
            self.Mtare = qml_values[2]
            self.Mfull = qml_values[3]
            self.length = qml_values[4]
            self.Aempty = qml_values[5]
            self.Bempty = qml_values[6]
            self.Cempty = qml_values[7]
            self.multiply_mass_empty = qml_values[8]
            self.Afull = qml_values[9]
            self.Bfull = qml_values[10]
            self.Cfull = qml_values[11]
            self.multiply_mass_full = qml_values[12]

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
    foucault_brake_count = 0

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
            list[int] -> [pad_brake, disk_brake, magnetic_brake, foucault_brake]
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
            self.motorisation = [False if i >= len(motorized_axles_count) else bool(motorized_axles_count[i]) for i in range(self.axles_count)]
        elif isinstance(motorized_axles_count, int):
            # Motorise les "motorized_axles_count" premier essieux et laissent les autres porteurs
            self.motorisation = [True if i < motorized_axles_count else False for i in range(self.axles_count)]

        if isinstance(braking_systems_count, list):
            self.pad_brake_count = 0 if len(braking_systems_count) <= 0 else braking_systems_count[0]
            self.disk_brake_count = 0 if len(braking_systems_count) <= 1 else braking_systems_count[1]
            self.magnetic_brake_count = 0 if len(braking_systems_count) <= 2 else braking_systems_count[2]
            self.foucault_brake_count = 0 if len(braking_systems_count) <= 3 else braking_systems_count[3]

    def get_motorized_axles_count(self):
        """Fonction permettant de retourner le nombre d'essieux moteurs

        Returns
        ----------
        Motorized_axles_count: `int`
            Nombre d'essieux motorisés du bogie
        """
        return self.motorisation.count(True)


class Train:
    """classe contenant les informations trains (et des fonctions de récupération de données"""
    # Propriétés principales (liste de bogies et de voitures
    general_mission = None
    bogies_list = []
    coaches_list = []

    def __init__(self, train_data=None):
        """Fonction d'initialisation de la classe des données train (pour la popup complex).
        Si des données sont envoyés la fonction génèrera automatiquement un train.

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Dictionnaire de paramètre du train (si non envoyé -> retourne un train vide)

        Raises
        ------
        KeyError
            Soulevé dans le cas où un paramètre nécessaire manque au dictionnaire de paramètres train
        """
        # L'appel de la fonction d'initialisation va dépendre de la présence ou non du mode.
        # Celui-ci ne sera pas présent lors de la génération mais uniquement lors d'ouverture de fichier
        if train_data is not None:
            try:
                train_data["mode"]
            except KeyError:
                self.generate(train_data)
            else:
                self.read_train(train_data)

    def generate(self, train_data):
        """Cette fonction permet de générer un train lors du paramétrage simple du train.
        Certaines conditions seront prises en comptes :
        - Les bogies classiques seront mis de préférence à l'avant et à l'arrière du train
        - Les bogies articulés seront mis de préférence en milieu de train
        - Le train sera considéré comme une unité simple (cela peut facilement être modifié)
        - Les essieux moteurs seront mis à l'extérieur du train
        - Les systèmes de freinages seront mis de préférence à l'avant et à l'arrière du train (magnétique puis foucault)

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Toutes les données du train

        Raises
        ------
        KeyError
            Soulevé dans le cas où un paramètre nécessaire manque au dictionnaire de paramètres train
        """
        # Informations sur le nombre de rames entièrement non articulées et le nomre d'essieux moteurs
        # Dans le cas d'un nombre impaire de bogies supplémentaires ou d'essieux moteurs, le mets à gauche
        left_non_articulated = int(((train_data["bogies_count"] - (train_data["coaches"] + 1)) + 1) / 2.0)
        left_motorized_axles = int((train_data["motorized_axles_count"] + 1)/2.0)
        right_non_articulated = int((train_data["bogies_count"] - (train_data["coaches"] + 1)) / 2.0)
        right_motorized_axles = int(train_data["motorized_axles_count"]/2.0)
        motorized_axle_weight = train_data["motorized_axle_weight"]
        non_motorized_axle_weight = (train_data["weight"] - (motorized_axle_weight * (left_motorized_axles + right_motorized_axles)))/((train_data["bogies_count"] * train_data["axles_per_bogies"]) - (left_motorized_axles + right_motorized_axles))
        previous_axles_count = 0
        next_axles_count = train_data["bogies_count"] * train_data["axles_per_bogies"]


        # Commence par indiquer le type de mission générale du train
        self.general_mission = MissionType[str(train_data.get_value("mission", "MissionType.PASSENGER"))[12:]]

        # Passe par toutes les voitures
        for car_index in range(train_data["coaches"]):
            # Commence par déterminer quels bogies sont articulés et combien de motorisation y a t'il
            previous_articulated = left_non_articulated < car_index <= train_data["coaches"] - right_non_articulated -1
            next_articulated = left_non_articulated <= car_index < train_data["coaches"] - right_non_articulated - 1
            axles_count = ((not previous_articulated) + 1) * train_data["axles_per_bogies"]
            next_axles_count -= axles_count
            still_to_motorize = ((left_motorized_axles - previous_axles_count) * (left_motorized_axles > previous_axles_count) +
                                 (right_motorized_axles - next_axles_count) * (right_motorized_axles > next_axles_count))
            motorized_count = axles_count if axles_count < still_to_motorize else still_to_motorize
            left_motorized_count = ((train_data["axles_per_bogies"] if train_data["axles_per_bogies"] < motorized_count else motorized_count)
                                    if not previous_articulated else
                                    (self.get_bogies([car_index - 1, car_index])[0].get_motorized_axles_count()))
            left_weight = (left_motorized_count * motorized_axle_weight + (train_data["axles_per_bogies"] - left_motorized_count) * non_motorized_axle_weight) * (0.5 + 0.5 * (not previous_articulated))
            right_motorized_count = (((motorized_count - train_data["axles_per_bogies"]) if motorized_count > train_data["axles_per_bogies"] else 0)
                                     if not previous_articulated else motorized_count)
            right_weight = (right_motorized_count * motorized_axle_weight + (train_data["axles_per_bogies"] - right_motorized_count) * non_motorized_axle_weight) * (0.5 + 0.5 * (not next_articulated))
            weight = left_weight + right_weight
            previous_axles_count += axles_count

            # si le bogie arrière n'est pas articulé le rajoute
            if not previous_articulated:
                self.bogies_list.append(Bogie(position=Position.FRONT,
                                              linked_coaches=car_index,
                                              axles_count=train_data["axles_per_bogies"],
                                              motorized_axles_count=left_motorized_count,
                                              axle_power=train_data["axle_power"],
                                              braking_systems_count=[0, 0, 0, 0]))  # TODO : modifier

            # Ajouter le bogie avant (dans tous les cas)
            self.bogies_list.append(Bogie(position=Position.BACK,
                                          linked_coaches=car_index if not next_articulated else [car_index, car_index+1],
                                          axles_count=train_data["axles_per_bogies"],
                                          motorized_axles_count=right_motorized_count,
                                          axle_power=train_data["axle_power"],
                                          braking_systems_count=[0, 0, 0, 0]))  # TODO : modifier

            # Commence par générer la voiture associé à l'index
            self.coaches_list.append(Coaches(mission_type=self.general_mission,
                                             position_type=Position.FRONT if car_index == 0 else
                                                           Position.BACK if car_index == (train_data["coaches"] - 1)
                                                           else Position.MIDDLE,
                                             position_index=car_index,
                                             levels=1 if self.general_mission == MissionType.PASSENGER else 0,
                                             doors=2 if self.general_mission == MissionType.PASSENGER else 0,
                                             Mtare=weight,
                                             Mfull=weight,
                                             length=train_data["length"]/train_data["coaches"],
                                             ABCempty=[train_data["a"], train_data["b"], train_data["c"]],
                                             multiply_mass_empty=False,
                                             ABCfull=[train_data["a"], train_data["b"], train_data["c"]],
                                             multiply_mass_full=False))


    def read_train(self, train_data):
        pass

    def clear(self):
        """Fonction permettant de vider les données train. Attention : Toutes réinitialisation est définitive."""
        self.bogies_list = []
        self.coaches_list = []

    def get_bogies(self, position_index, position_type=None):
        """Fonction permettant d'avoir un bogie avec les index indiqués

        Parameters
        ----------
        position_index: `Union[int, list]`
            Les voitures auxquelles le bogie est connecté (int ou liste de int) doit aller de 0 à Nvoitures - 1
        position_type: `Position`
            La position des bogies dans la voiture (Position.FRONT ; Position.MIDDLE ; Position.BACK) si cela est vital

        Returns
        -------
        bogies_list: `list`
            liste des bogies suivant les conditions envoyés
        """
        if isinstance(position_index, int):
            # Vérification si coaches_index est un int
            return [b for b in self.bogies_list if ((position_index in b.linked_coaches
                                                    and (position_index is None or b.position == position_type))
                                                or (position_type is not None and not Position.MIDDLE
                                                    and (position_index + (position_type == Position.BACK) - (position_type == Position.FRONT)) in b.linked_coaches)
                                                    and ((position_type == Position.BACK and b.position == Position.FRONT)
                                                         or (position_type == Position.FRONT and b.position == Position.BACK)))]
        elif isinstance(position_index, list):
            # Vérification si coaches_index est une liste
            return [b for b in self.bogies_list if all(p_i in b.linked_coaches for p_i in position_index)
                                                and (position_type is None or b.position == position_type)]
        else:
            # Cas où le position_index est invalide
            return []


def main():
    log.initialise(save=False)

    train_data = sd.SettingsDictionary()
    if "mode" in train_data:
        train_data.pop("mode")
    train_data.open(f"{PROJECT_DIR}\\settings\\train_settings\\default.train")

    initial_time = time.perf_counter()
    train_database = Train(train_data)
    log.debug(f"Train généré en {(time.perf_counter() - initial_time) * 1000} millisecondes")


if __name__ == "__main__":
    main()
