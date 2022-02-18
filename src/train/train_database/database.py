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

        # Indique le temps de chargement de la BDD
        log.info(f"Base de Données train initialisée en " +
                 f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.",
                 prefix="Initialisation BDD train")

