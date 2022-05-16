# Librairies par défaut
import sys
import os
from enum import Enum


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
from src.misc.units_converter.units import get_conversion_list


class ConversionList(Enum):
    """Enum contenant une série de liste de conversions"""
    # Valeurs reliées aux coefficients Rav
    Aconst = ("kN", "daN", "N")
    Bconst = ("kN/(km/h)", "daN/(km/h)", "N/(km/h)", "N/(m/s)")
    Cconst = ("kN/(km/h)^2", "daN/(km/h)^2", "N/(km/h)^2", "N/(m/s)^2")
    Aweight = ("kN/t", "daN/t", "N/kg")
    Bweight = ("kN/t/(km/h)", "daN/t/(km/h)", "N/t/(km/h)", "N/kg/(m/s)")
    Cweight = ("kN/t/(km/h)^2", "daN/t/(km/h)^2", "N/t/(km/h)^2", "N/kg/(m/s)^2")

    def __call__(self):
        """Retourne la liste de conversion en appelant sa valeur d'enum (e.g : uc.ConversionList.weight())"""
        return get_conversion_list(self.value)
