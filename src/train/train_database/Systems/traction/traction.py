# Librairies par défaut
import sys
import os
from typing import Union


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.train.train_database.database as tdb
from src.train.train_database.Systems.traction.bogie.bogie import Bogie


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
        position_index: `Union[int, list]`
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
        bogie: `Bogie`
            bogie à rajouter dans la liste de bogies
        """
        # Ajoute le bogie si c'est bien un bogie sinon laisse un message de debug
        if isinstance(bogie, Bogie):
            self.bogies.append(bogie)
        else:
            log.debug(f"bogie envoyé de mauvais type ({type(bogie)} au lieu de Bogie).")

    def remove_bogie(self, bogie):
        """fonction permettant d'enlever un bogie de la liste des bogies (par élément ou par bogie)

        Parameters
        ----------
        bogie: `Union(Bogie, int)`
            Bogie -> bogie à enlever (à récupérer avec la méthodes get_bogies()[...]
            int -> position dans la liste de bogies du bogie (Attention! Les bogies ne sont pas forcément dans l'ordre).
        """
        # Enlève le bogie envoyé en s'assurant qu'il existe bien encore dans la liste
        if isinstance(bogie, Bogie) and bogie in self.bogies:
            self.bogies.remove(bogie)
        elif isinstance(bogie, int) and -len(self.bogies) <= bogie < len(self.bogies):
            self.bogies.pop(bogie)
        elif isinstance(bogie, Bogie) and bogie not in self.bogies:
            log.debug(f"Impossible de supprimer le bogie {bogie} qui n'est pas dans la liste.")
        elif isinstance(bogie, int) and (bogie >= len(self.bogies) or bogie < -len(self.bogies)):
            log.debug(f"Impossible de supprimer le bogie {bogie}. Le train a seulement {len(self.bogies)} bogies.")
        else:
            log.debug(f"{type(bogie)} n'est pas un bogie valide. Il doit être de type Bogie ou int.")
