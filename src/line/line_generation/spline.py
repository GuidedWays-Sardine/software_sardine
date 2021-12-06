# Librairies par défaut
import sys
import os
import time

# Librairies de traitement de données
import pandas as pd
import numpy as np

# librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.line.line_generation.database as DB


# constantes pour la création des splines
DISTANCE_ERROR = 2      # Erreur de localisation permise en m


class Spline:
    # Informations générales sur la spline
    line_code = 0
    track_name = ""
    pk_debut = 0
    geo_debut = [0, 0]
    pk_fin = 0
    geo_fin = [0, 0]

    # Toutes les bases de données avec les informations nécessaires
    curves = None
    slopes = None
    max_speed = None
    electrification = None

    # Fonctions d'initialisation et de mise à jour de la spline
    def __init__(self, track, curves, slopes, max_speed=pd.DataFrame(), electrification=pd.DataFrame):
        """Permet d'initialiser la spline en fonction des informations de la ligne.
        Considère toutes les informations envoyées comme provenant directement de la voie et avec des données cohérentes

        Parameters
        ----------
        track: `pd.Series`
            Information sur la voie traitée (permet de récupérer le PK de début et de fin ainsi que la ligne et la voie)
        curves: `pd.DataFrame`
            Liste de toutes les courbes de la ligne chargée
        slopes: `pd.DataFrame`
            Liste de toutes les pentes et ramples de la ligne chargée
        max_speed: `pd.DataFrame`
            Liste de toutes les vitesses maximales de la ligne chargée
        electrification: `pd.DataFrame`
            Electrification de la ligne
        """
        # Commence par récupérer les éléments généraux de la spline
        self.line_code = track["CODE_LIGNE"]
        self.track_name = track["NOM_VOIE"]     # TODO : faire un algorithme qui inclut le PK de début et de fin dans le nom de la spline
        self.pk_debut = track[DB.PK + DB.DEBUT]
        self.geo_debut = [track[DB.GEO_LO + DB.DEBUT], track[DB.GEO_LA + DB.DEBUT]]
        self.pk_fin = track[DB.PK + DB.FIN]
        self.geo_fin = [track[DB.GEO_LO + DB.FIN], track[DB.GEO_LA + DB.FIN]]

        # Stocke les bases de données avec les informations sur la voie
        self.curves = curves.reset_index(drop=True)
        self.slopes = slopes.reset_index(drop=True)
        self.max_speed = max_speed.reset_index(drop=True)
        self.electrification = electrification.reset_index(drop=True)

    def update(self, curves, slopes, max_speed, electrification):
        pass
        # TODO : fonction permettant de mettre à jour la base de données

    def clean_databases(self):
        """Fonction permettant de s'assurer que toutes les valeurs sont dans les limites de la voie"""
        # Pour chacunes des bases de données contenus dans la classe
        for df in [self.curves, self.slopes, self.max_speed, self.electrification]:
            # Remplace tous les PK et positions géographiques de début et fin pour les points qui sortent de la limite
            df.loc[(df[DB.PK + DB.DEBUT] < self.pk_debut), [DB.GEO_LO + DB.DEBUT, DB.GEO_LA + DB.DEBUT, DB.PK + DB.DEBUT]] = \
                [self.geo_debut[0], self.geo_debut[1], self.pk_debut]
            df.loc[(df[DB.PK + DB.FIN] < self.pk_fin), [DB.GEO_LO + DB.FIN, DB.GEO_LA + DB.FIN, DB.PK + DB.FIN]] = \
                [self.geo_fin[0], self.geo_fin[1], self.pk_fin]

    def is_completed(self):
        """Fonction indiquant si les informations pour la spline sont complétées ou non"""
        return not self.curves.empty and not self.slopes.empty and self.electrification.empty and self.max_speed.empty
        #TODO : améliorer la vérification

    def split(self):
        # Fonction qui à partir d'un PK split la spline en deux
        pass
