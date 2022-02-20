# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.train.train_database.database as tdb
import src.misc.settings_dictionary.settings as sd
from src.train.train_database.Systems.traction.bogie.bogie import Bogie


class Disk:
    """Classe contenant toutes les informations sur le système de stockage"""
    # Informations sur la position du système de freinage
    bogie_linked = None             # le bogie sur lequel les systèms de freinage se situent
    axles_linked = None             # Position dans le bogie ou se situe le système de freinage

    # Informations techniques sur les charactéristiques du freinage

    def __init__(self, bogie_linked, brake_parameters):
        """Fonction permettant d'initialiser un systèmes de freinage de foucault

        Parameters
        ----------
        bogie_linked: `Bogie`
            Bogie sur lequel se situe

        brake_parameters: `sd.SettingsDictionary`
            Tous les arguments sur la position du système de freinage dans le train
        """
        # Indique le bogie auquel le système de freinage est connecté
        self.bogie_linked = bogie_linked

        # Change les valeurs du système de freinage
        self.set_general_brake_values(brake_parameters)

    def set_general_brake_values(self, brake_parameters):
        """Fonction permettant de changer les paramètres de freinage

        Parameters
        ----------
        brake_parameters: `sd.SettingsDictionary`
            Tous les arguments sur la position du système de freinage dans le train
        """
        pass  # TODO : définir les paramètres nécessaires pour le freinage par disque
