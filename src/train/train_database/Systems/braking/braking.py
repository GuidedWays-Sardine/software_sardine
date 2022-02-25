# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd
from src.train.train_database.Systems.traction.bogie.bogie import Bogie
from src.train.train_database.Systems.braking.brakes.disk import Disk
from src.train.train_database.Systems.braking.brakes.pad import Pad
from src.train.train_database.Systems.braking.brakes.magnetic import Magnetic
from src.train.train_database.Systems.braking.brakes.foucault import Foucault


class Braking:
    # Informations sur certains types de freinages
    regenerative_activated = False
    dynamic_activated = False

    # Informations sur les systèmes de freinages
    pad_brakes = None
    disk_brakes = None
    magnetic_brakes = None
    foucault_brakes = None

    def __init__(self, train_data):
        """Fonction permettant d'initialiser les systèmes de freinages

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Dictionaire de paramètres train
        """
        # Récupère les valeurs pour le freinage rhéostatique et par régénération
        self.regenerative_activated = train_data.get_value("regenerative", False)
        self.dynamic_activated = train_data.get_value("dynamic", False)
        # TODO : chercher comment le système de freinage rhéostatique et régénératif seront paramétrés

        # Initialise des listes vides pour chacuns des systèmes de freinage
        self.pad_brakes = []
        self.disk_brakes = []
        self.magnetic_brakes = []
        self.foucault_brakes = []

    def get_brake_list(self, brake_type):
        """Fonction permettant de retourner la liste de freinage adéquat selon le type envoyé

        Parameters
        ----------
        brake_type: `type`
            Le type de freinage

        Returns
        -------
        brake_list: `list`
            La liste des systèmes de freinage du type demandé

        Raises
        ------
        TypeError:
            Exception jetée si le système de freinage recherché n'est pas bon
        """
        # Selon le système de freinage recherché, retourne la liste de freinage, sinon jette une exception
        if brake_type is Pad:
            return self.pad_brakes
        elif brake_type is Disk:
            return self.disk_brakes
        elif brake_type is Magnetic:
            return self.magnetic_brakes
        elif brake_type is Foucault:
            return self.foucault_brakes
        else:
            raise TypeError(f"le type {brake_type} n'est pas un système freinage connu.")

    def get_bogie_brake_list(self, bogie=None, brake_type=None):
        """Fonction permettant de retourner les systèmes de freinages appartenant à un bogie

        Parameters
        ----------
        bogie: `Bogie | None`
            bogie auquel appartient les systèmes de freinage recherché (freinages de tous les bogies si à None)
        brake_type: `type | None`
            type de bogie recherché (laisser à None pour tous)

        Returns
        -------
        brakes_list: `list`
            liste des systèmes de freinage [...] -> si freinage spécifique, [[...], [...], [...], [...]] si tous
        """
        # Prend dans le cas où aucun bogie n'est spécifié (et que tous les systèmes de freinages doivent être retournés)
        if bogie is None:
            return [self.pad_brakes, self.disk_brakes, self.magnetic_brakes, self.foucault_brakes]

        # Se prépare a une potentielle erreur de type de système de freinage
        try:
            # Si un type spécifique de freinage a été demandé, retourne la liste de ce système spécifique
            if brake_type is not None:
                return [b_s for b_s in self.get_brake_list(brake_type) if b_s.bogie_linked is bogie]
            # Sinon rappelle la fonction récursivement avec chacun des types de freinage
            else:
                return [self.get_bogie_brake_list(bogie, b_t) for b_t in [Pad, Disk, Magnetic, Foucault]]
        except TypeError as error:
            log.debug(f"Erreur dans le type de système de freinage demandé ({brake_type})", exception=error)
            return []

    def get_bogie_brakes_count(self, bogie):
        """Retourne le compte de chacun des systèmes de freinage pour le bogie en question

        Parameters
        ----------
        bogie: `Bogie`
            bogie dont les systèmes de freinages doivent être comptés
        """
        # Récupère la liste des systèmes de freinage du bogie
        bogie_brake_list = self.get_bogie_brake_list(bogie)

        # Si la liste est vide (dû à une erreur) retourne une liste de 4 zéros, sinon compte chacun des systèmes
        if bogie_brake_list:
            return [len(b_l) for b_l in bogie_brake_list]
        else:
            return [0, 0, 0, 0]

    def add_braking_systems(self, bogie, brakes_list, brakes_parameters):
        """fonction permettant à partir d'une liste de systèmes de freinage et de ses paramètres de les ajouter

        Parameters
        ----------
        bogie: `Bogie`
            bogie auquel les nouveaux systèmes de freinage sont connectés
        brakes_list: `list | tuple`
            Liste du nombre de systèmes de freinage à rajouter pour chaque types de freinage
            format : [pad, disk, magnetic, foucault]
        """
        # Pour chacun des systèmes de freinage
        for i, brake in enumerate([Pad, Disk, Magnetic, Foucault]):
            # Ajoute autant du bon type de freinage
            for _ in range(brakes_list[i]):
                self.get_brake_list(brake).append(brake(bogie, brakes_parameters))
