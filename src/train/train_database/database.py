# Librairies par défaut python
import sys
import os
import time
from enum import Enum


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd
import src.train.train_database.Dynamic.dynamic as dynamic
import src.train.train_database.Static.static as static
import src.train.train_database.Systems.systems as systems


class Position(Enum):
    """Enum permettant de savoir si la voiture est une voiture avant ou arrière (utile pour savoir l'image à charger"""
    FRONT = "front"
    MIDDLE = "middle"
    BACK = "back"


class MissionType(Enum):
    """Enum permettant de connaitre le type de mission (pour la génération"""
    # Feature : ajouter les autres modes de transports ci-dessous. Ils seront automatiquement détectés par les modules
    PASSENGER = "Passengers"
    FREIGHT = "Freight"


mission_getter = {i: key for i, key in enumerate(MissionType)}  # Permet d'obtenir la mission avec l'index de celle-ci


class TrainDatabase:
    """base de données train"""

    # Différents éléments nécessaires pour le train
    dynamic = None
    static = None
    systems = None

    def __init__(self, train_data):
        """Fonction d'initialisation de la abse de données train

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Dictionaire de paramètres train
        """
        initial_time = time.perf_counter()
        log.info("Initialisation Base de Données train", prefix="Initialisation BDD train")

        # Initialise chacun des types de données (dynamiques, statiques, et systèmes)
        self.dynamic = dynamic.Dynamic(train_data)
        self.static = static.Static(train_data)
        self.systems = systems.Systems(train_data)

        # Récupère la quantité de chacun des systèmes du train
        railcar_count = len(self.systems.frame.railcars)
        bogies_count = len(self.systems.traction.bogies)
        pad_brakes_count = len(self.systems.braking.pad_brakes)
        disk_brakes_count = len(self.systems.braking.disk_brakes)
        magnetic_brakes_count = len(self.systems.braking.magnetic_brakes)
        foucault_brakes_count = len(self.systems.braking.foucault_brakes)
        brakes_count = pad_brakes_count + disk_brakes_count + magnetic_brakes_count + foucault_brakes_count

        # Indique le temps de chargement de la BDD
        log.info(f"Base de Données train initialisée en " +
                 f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.\n\t" +
                 f"<{railcar_count} voitures ; {bogies_count} bogies ; " +
                 f"{brakes_count} éléments de freinage ({pad_brakes_count} semelles, {disk_brakes_count} disques, {magnetic_brakes_count} magnétiques, {foucault_brakes_count} foucault) ; " +
                 f">",
                 prefix="Initialisation BDD train")

    def get_values(self):
        """Fonction permettant de récupérer tous les paramètres du train

        Returns: `sd.SettingsDictionary`
            Tous les paramètres du train
        """
        parameters = sd.SettingsDictionary()

        # Récupère les données états des sous-systèmes et les données dynamiques et statiques
        parameters.update(self.systems.get_values())
        # TODO : récupérer les valeurs statiques et dynamiques du train

        return parameters