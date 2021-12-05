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
        electrification: `str`
            Electrification de la ligne
        """
        # Commence par récupérer les éléments généraux de la spline
        self.line_code = track["CODE_LIGNE"]
        self.track_name = track["NOM_VOIE"]
        self.pk_debut = track[DB.PK + DB.DEBUT]
        self.geo_debut = [track[DB.GEO_LO + DB.DEBUT], track[DB.GEO_LA + DB.DEBUT]]
        self.pk_fin = track[DB.PK + DB.FIN]
        self.geo_debut = [track[DB.GEO_LO + DB.FIN], track[DB.GEO_LA + DB.FIN]]

        # Stocke les bases de données avec les informations sur la voie
        self.curves = curves
        self.slopes = slopes
        self.max_speed = max_speed
        self.electrification = electrification

    def __init__(self):
        print("e")