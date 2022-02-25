# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary.settings as sd
from src.train.train_database.Systems.traction.bogie.bogie import Bogie


class Foucault:
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

        brake_parameters: `tuple | list`
            Tous les arguments sur la position du système de freinage dans le train
            format : (...) # TODO : trouver le format des arguments
        """
        # Indique le bogie auquel le système de freinage est connecté
        self.bogie_linked = bogie_linked

        # Change les valeurs du système de freinage
        self.set_general_brake_values(brake_parameters)

    def set_general_brake_values(self, brake_parameters=None):
        """Fonction permettant de changer les paramètres de freinage

        Parameters
        ----------
        brake_parameters: `tuple | list`
            Tous les arguments sur les spécificités du système de freinage. Valeurs par défaut si vide
            format : (...) # TODO : trouver le format des arguments
        """
        if brake_parameters is not None:
            pass        # TODO : définir les paramètres nécessaires à définir

    def get_general_brake_values(self):
        """Fonction permettant de retourner les paramètres de freinage

        Returns
        -------
        brake_parameters: `tuple | list`
            Tous les arguments sur les spécificités du système de freinage
            format : (...) # TODO : trouver le format des arguments (identique au seter pour simplification)
        """
        return ()   # TODO : définir les paramètres nécessaires à retourner

    def get_values(self, list_index):
        """Fonction permettant de récupérer toutes les valeurs du système de freinage de foucault.

        Parameters
        ----------
        list_index: `int`
            Index du bogie dans la liste (permet de distinguer les différents bogies dans le fichier paramètres)

        Returns
        -------
        settings_dictionary: `sd.SettingsDictionary`
            dictionaire des paramètres avec tous les paramètres techniques du système de freinage de foucault.
        """
        parameters = sd.SettingsDictionary()
        prefix = f"bogie{list_index}.foucault"

        # Récupère tous les paramètres du système de freinage du bogie
        # TODO : ajouter tous les paramètres techniques du système de freinage

        return parameters
