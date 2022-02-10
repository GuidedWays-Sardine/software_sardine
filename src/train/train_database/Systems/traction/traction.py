# Librairies par défaut python
# Librairies par défaut python
import sys
import os



# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.train.train_database.database as tdb


class Bogie:
    """classe contenant toutes les informations sur le bogie"""
    # Informations générales
    position_type = None
    position_index = -1  # Uniquement pour les bogies centraux! Les bogies extérieurs n'ont pas d'index
    axles_count = 1
    linked_coaches = []

    # Informations sur la motorisation
    axles_power = []     # Puissance du moteur, sinon 0 si aucun moteur
    activated = []      # True si le moteur est allumé, False sinon
    activable = []      # True si le moteur est activable, False sinon (si panne)

    def __init__(self):
        self.axle_count = 0
        self.axle_power = 0
        self.motor_position = None
        self.state = None
        self.ignitable = None
        self.linked_coaches = None
        self.power = None
        self.type = None
        self.bogie_mass = 0


    def set_general_values(self, position_type, position_index, linked_coaches, axles_count, motorized_axles, axles_power):
        """Fonction permettant de changer les valeurs d'un bogie

        Parameters
        ----------
        position_type: `tdb.Position`
            La position du bogie sur la voiture (Position.FRONT ; Position.MIDDLE ; Position.BACK)
        position_index: `int`
            L'index de la position si le bogie est central (sinon -1)
        linked_coaches: `Union[int, list]`
            Liste des voitures auxquelles le bogie est connecté
        axles_count: `int`
            nombre d'essieux
        motorized_axles: `Union[list, int, NoneType]`
            list[bool] -> liste de la position des essieux moteurs (doit être de taille axles_count)
            int -> nombre d'essieux moteurs (doit être inférieur à axles_count)
            NoneType -> axles_power au format list[float] auquel cas cet argument n'est pas nécessaire
        axles_power: `Union[list, float]`
            list[float] -> liste de la puissance de chacun des moteurs
            float -> puissance des moteurs (tous les essieux motorisés auront cette puissance)
        """
        # initialise les caractéristiques générales du bogie
        self.position_type = position_type
        self.position_index = position_index
        if isinstance(linked_coaches, list):
            self.linked_coaches = linked_coaches
        elif isinstance(linked_coaches, int):
            self.linked_coaches = [linked_coaches]
        self.axles_count = axles_count if axles_count >= 1 else 1

        # Initialise la puissance des essieux moteurs
        # Cas 1 : la puissance des essieux moteurs est une liste de float
        if isinstance(axles_power, list):
            # S'assure juste qu'il y a autant d'éléments qu'il y a d'essieux sinon ralonge/raccourcis la liste
            self.axles_power = [axles_power[i] if i < len(axles_power) else 0.0 for i in range(self.axles_count)]
        # Cas 2 : la puissance des essieux moteurs est un float
        elif isinstance(axles_power, float) or isinstance(axles_power, int):
            # Cas 2.1 : les essieux moteurs est une liste
            if isinstance(motorized_axles, list):
                # Met la puissance à axles_power pour chacun des essieux moteurs et ralong/raccourcis la liste au besoin
                self.axles_power = [bool(motorized_axles[i]) * axles_power if i < len(motorized_axles) else 0.0 for i in range(self.axles_count)]
            # Cas 2.2 : les essieux moteurs est un int (nombre d'essieux moteurs
            elif isinstance(motorized_axles, int) or isinstance(motorized_axles, float):
                # Met la puissance pour les motorized_axles premiers essieux, sinon la met à 0
                self.axles_power = [axles_power * (i < motorized_axles) for i in range(self.axles_count)]
            # Cas 2.3 : les essieux moteurs ne sont ni une liste de bool, ni un int
            else:
                # Rend l'essieu porteur (puissances moteurs de 0.0) pour éviter l'exception de lecture hors du tableau
                self.axles_power = [0.0] * self.axles_count
        # Cas 3 : la puissance des essieux moteurs n'es ni une liste de float ni un float
        else:
            # Rend l'essieu porteur (puissances moteurs de 0.0) pour éviter l'exception de lecture hors du tableau
            self.axles_power = [0.0] * self.axles_count

        # Mets les essieux comme éteints et rends tous les essieux moteurs activables
        self.activated = [False] * self.axles_count
        self.activable = [bool(axles_power[i]) for i in range(self.axles_count)] # bool retourne False que pour 0.0





