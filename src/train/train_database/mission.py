# Librairies par défaut python
from enum import Enum


class Mission(Enum):
    """Enum des différents modes de transports"""
    # ENHANCE : Ajouter les autres modes de transports ci-dessous. Ils seront automatiquement détectés par les modules
    PASSENGERS = "Passengers"
    FREIGHT = "Freight"


# Permet d'obtenir la mission avec l'index de celle-ci
mission_getter = {i: key for i, key in enumerate(Mission)} | {key: i for i, key in enumerate(Mission)}
