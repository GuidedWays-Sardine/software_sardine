# Librairies par défaut
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd
import src.train.train_database.database as tdb
from src.train.train_database.Systems.traction.bogie.bogie import Bogie
from src.train.train_database.Systems.braking.braking import Braking


class Traction:
    """classe stockant tous tous les éléments nécessaires à la traction"""
    # Stoque la liste des bogies
    bogies = None

    def __init__(self):
        """Fonction permettant d'initialiser une liste de bogies vide (à remplir ensuite)"""
        self.bogies = []

    def get_bogies(self, position_index, position_type=None):
        """Fonction permettant d'avoir un bogie avec les index indiqués

        Parameters
        ----------
        position_index: `int | list`
            Les voitures auxquelles le bogie est connecté (int ou liste de int) doit aller de 0 à Nvoitures - 1
        position_type: `Position`
            La position des bogies dans la voiture (Position.FRONT ; Position.MIDDLE ; Position.BACK) si cela est vital

        Returns
        -------
        bogies_list: `list`
            liste des bogies suivant les conditions envoyés
        """
        # Transforme l'index de la position du bogie en liste d'index si l'index envoyé est un entier
        if isinstance(position_index, int):
            position_index = [position_index]

        # Cas où le/les bogies recherchés se trouvent sur une seule voiture
        if len(position_index) == 1:
            # Le bogie est sur la voiture dans le cas où :
            # - l'index envoyé est dans la liste et qu'aucune position n'a été donnée
            # - l'index envoyé est dans la liste et que le type de position correspond à celui du bogie
            # - le bogie avant est cherché et l'index de la voiture actuelle et précédente sont dans la liste
            # - le bogie arrière est cherché et l'index de la voiture actuelle et suivant sont dans la liste
            # - le bogie arrière (ou non spécifié) est cherche et que le bogie avant de la voiture suivant est articulée
            return [b for b in self.bogies
                    if ((position_index[0] in b.linked_railcars and (position_type is None or b.position_type == position_type))
                        or (position_type == tdb.Position.FRONT and position_index[0] in b.linked_railcars and (position_index[0] - 1) in b.linked_railcars)
                        or (position_type == tdb.Position.BACK and position_index[0] in b.linked_railcars and (position_index[0] + 1) in b.linked_railcars))]
        # Cas où le bogie recherché se trouve sur deux voiture (bogie jacobien, rame articulée)
        elif len(position_index) == 2:
            # Retourne le bogie qui appartient aux deux voitures s'il existe (sinon retourne liste vide)
            return [b for b in self.bogies if all(p_i in b.linked_railcars for p_i in position_index)
                    and (position_type is None or b.position_type == position_type)]
        # Cas où trop d'index ou aucun index n'ont été donnés (retourne une liste vide)
        else:
            return []

    def add_bogie(self, bogie):
        """Fonction permettant de rajouter un bogie à la liste de bogies du système de traction

        Parameters
        ----------
        bogie: `Bogie | list | tuple`
            Bogie -> bogie à rajouter dans la liste de bogies
            tuple/list -> Les données du bogie qui sera créé puis rajouter (se référer à traction.bogie.Bogie(...)
            format : (position_type, linked_railcars, axles_count, motorized_axles, axles_power)
        """
        # Ajoute le bogie si c'est bien un bogie sinon laisse un message de debug
        if isinstance(bogie, Bogie):
            self.bogies.append(bogie)
        elif isinstance(bogie, (tuple,  list)) and len(bogie) == 5:
            self.bogies.append(Bogie(bogie[0], bogie[1], bogie[2], bogie[3], bogie[4]))
        else:
            log.debug(f"bogie envoyé de mauvais type ({type(bogie)} au lieu de Bogie ou tuple de taille 6).")

    def remove_bogie(self, bogie, train_database):
        """fonction permettant d'enlever un bogie de la liste des bogies (par bogie)

        Parameters
        ----------
        bogie: `Bogie`
            Bogie -> bogie à enlever (à récupérer avec la méthodes get_bogies()[...]
        train_database: `tdb.TrainDatabase`
            Base de données train dans lequel le bogie est contenu (nécessaire pour enlever les systèmes de freinage)
        """
        # Enlève le bogie envoyé en s'assurant qu'il existe bien encore dans la liste
        if isinstance(bogie, Bogie) and bogie in self.bogies:
            remove_brakes = [-b_c for b_c in train_database.systems.braking.get_bogie_brakes_count(bogie)]
            train_database.systems.braking.modify_brakes_count(bogie, remove_brakes)
            self.bogies.remove(bogie)
        elif isinstance(bogie, Bogie) and bogie not in self.bogies:
            log.debug(f"Impossible de supprimer le bogie {bogie} qui n'est pas dans la liste.")
        else:
            log.debug(f"{type(bogie)} n'est pas un bogie valide. Il doit être de type Bogie.")

    def split_bogies(self, linked_coaches, train_database):
        """Fonction permettant de diviser un bogie jacobien en deux bogies.

        Parameters
        ----------
        linked_coaches: `list`
            Index des deux voitures dont le bogie articulé doit être séparé.
            elle doit contenir deux voitures consécutives. Si aucun bogie articulé n'est trouvé, rien ne se passera.
        train_database: `tdb.TrainDatabase`
            Base de données train dans lequel le bogie est contenu (nécessaire pour dupliquer les systèmes de freinage)
        """
        # Vérifie que la liste d'index est bien composé de deux index consécutif
        if isinstance(linked_coaches, list) and len(linked_coaches) == 2 and int(min(linked_coaches)) == int(max(linked_coaches) - 1):
            # Récupère le bogie articulé à diviser et le divise s'il existe (sinon fait rien)
            jacob_bogie = self.get_bogies(linked_coaches)
            if jacob_bogie:
                # Récupère les données du bogie
                bogie_data = jacob_bogie[0].get_general_values()

                # met à jour les données du bogie récupérer pour le mettre à l'arrière de la voiture avant
                jacob_bogie[0].set_general_values(tdb.Position.BACK, int(min(linked_coaches)), bogie_data[2], None, bogie_data[3])

                # Rajoute un nouveau bogie à l'avant de la voiture arrière avec les mêmes données
                duplicate_brakes = train_database.systems.braking.get_bogie_brakes_count()
                brakes_parameters = train_database.systems.braking.get_bogie_brake_list()
                brakes_parameters = [(brake[0].get_general_brake_values() if len(brake) > 0 else None) for brake in brakes_parameters]
                train_database.systems.braking.modify_brakes_count(duplicate_brakes, brakes_parameters)
                self.add_bogie(Bogie(tdb.Position.FRONT, int(max(linked_coaches)), bogie_data[2], None, bogie_data[3]))
        else:
            log.debug(f"Impossible de séparer les deux bogies. Liste de voitures invalide ({linked_coaches}).")

    def merge_bogies(self, linked_coaches):
        """Fonction permettant de fusioner deux bogies pour en faire un bogie articulé.
        Si aucun bogie existe sur les deus voitures, un bogie articulé sera créé

        Parameters
        ----------
        linked_coaches: `list`
            Index des deux voitures dont les bogies doivent être fusionés.
            elle doit contenir deux voitures consécutives. Si l'une des voitures sont suspendus, créera un nouveau bogie
        """
        # S'assure que la liste des voitures représente deux entiers
        if len(linked_coaches) == 2:
            linked_coaches = [int(min(linked_coaches)), int(max(linked_coaches))]

        # Vérifie que la liste d'index est bien composé de deux index consécutif
        if isinstance(linked_coaches, list) and len(linked_coaches) == 2 and linked_coaches[0] == linked_coaches[1] - 1:
            # Vérifie qu'il n'y a pas déjà un bogie articulé entre ces deux voitures, sinon retourne
            if self.get_bogies(linked_coaches):
                return

            # Récupère les deux bogies à fusioner
            back_bogie = self.get_bogies(linked_coaches[0], tdb.Position.BACK)
            front_bogie = self.get_bogies(linked_coaches[1], tdb.Position.FRONT)

            # Si au moins l'un des bogies non articulé existe
            if front_bogie or back_bogie:
                # Commence par supprimer le bogie arrière si les deux bogies non articulés existe (évite le duplicata)
                if front_bogie and back_bogie:
                    self.remove_bogie(back_bogie[0])

                # Utilise ce bogie comme base pour créer le bogie articulé
                bogie_data = front_bogie[0].get_general_values() if front_bogie else back_bogie[0].get_general_values()

                # met à jour les données du bogie récupérer pour le mettre à l'arrière de la voiture avant
                front_bogie[0].set_general_values(None, linked_coaches, bogie_data[3], None, bogie_data[4])
            # Si les deux bogies n'existent pas (les deux voitures suspendus)
            else:
                # Génère un essieu porteur
                axles_count = self.bogies[0].axles_count if self.bogies else 2
                self.add_bogie(Bogie(None, linked_coaches, axles_count, 0, 0.0))
        else:
            log.debug(f"Impossible de fusionner deux voitures. Liste de voitures invalide ({linked_coaches}).")

    def get_values(self, braking_systems):
        """Fonction permettant de récupérer toutes les valeurs de tous les bogies et de leurs systèmes de freinage.

        Parameters
        ----------
        braking_systems: `Braking`
            Liste de tous les systèmes de freinages du train pour les sauvegarder en même temps

        Returns
        -------
        settings_dictionary: `sd.SettingsDictionary`
            dictionaire des paramètres avec tous les paramètres de tous les bogies et de leurs systèmes de freinage.
        """
        parameters = sd.SettingsDictionary()

        # Pour chacun des bogies du train, récupère les données du bogie et celle de ses systèmes de freinages associés
        for b_i, bogie in enumerate(self.bogies):
            parameters.update(bogie.get_values(b_i))
            parameters.update(braking_systems.get_values(bogie, b_i))

        return parameters
