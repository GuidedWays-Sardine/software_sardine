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
import src.misc.log as log
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

 # Fonctions d'ouverture et d'enregistrement des splines
    def open(self):
        # Fonction qui permet de créer un spline depuis un (ou plusieurs) fichiers csv)
        pass

    def save_to_python(self, folder_path):
        """Fonction permettant de sauvegarder la spline"""
        # Fonction permettant de sauvegarder la spline dans un fichier adapté
        pass

    def save_to_ue5(self, folder_path):
        """Fonction permettant de convertir et d'enregistrer les informations d'une spline"""
        # Fonction permettant de convertir en une spline compatible pour UE 5
        pass

    # Fonctions mathématiques utiles au foncctionnement des splines
    def get_distance_to_spline(self, pk, point):
        """Fonction permettant de retourner la distance entre un point et la spline

        Parameters
        ----------
        pk: `int`
            Point kilométrique au niveau duquel la ligne intercepterait le point
        point: `list`
            Longitude et Latitude du point à vérifier"""
        # Vérifie en premier lieu que le pk est bien sur la spline, sinon retourne une valeur au dessus de l'erreur
        if pk < self.pk_debut or pk > self.pk_fin:
            return DISTANCE_ERROR + 1

        # Sinon vérifie s'il est en ligne droite, en courbe ou si la donnée n'existe pas.
        associated_curve = self.curves.loc[(self.curves[DB.PK + DB.DEBUT] <= pk) & (self.curves[DB.PK + DB.FIN]) < pk]
        if associated_curve.empty:
            # Dans le cas où la spline n'a pas d'informations entrées, retourne une distance invalidante
            return DISTANCE_ERROR + 1
        else:
            if associated_curve.iloc[0].SENS.str.upper() == "ALIGNEMENT":
                Spline.get_distance_to_line()

    @staticmethod
    def get_distance_to_line(line, point):
        """Fonction permettant de retourner la distance minimale entre une ligne et un point

        Parameters
        ----------
        line: `pd.Series`
            Information sur la section de spline
        point: `list`
            coordonées x et y du point à localiser

        Returns
        -------
        distance: `float`
            distance minimale entre le point et la droite
        """
        # ax1 + b = y1      =>      a = (x1-x2)/(y1+y2)
        # ax2 + b = y2      =>      b = y1-x1*(x1-x2)/(y1+y2)
        x1, y1 = Spline.geo_to_position(line[DB.GEO_LO + DB.DEBUT], line[DB.GEO_LA + DB.DEBUT])
        x2, y2 = Spline.geo_to_position(line[DB.GEO_LO + DB.FIN], line[DB.GEO_LA + DB.FIN])
        a = (x1 - x2) / (y1 + y2)
        b = y1 - x1 * a

        # d =  |y - ax - b|/sqrt(1 + a²)
        return abs(point[1] - a * point[1] - b) / ((1 + a ** 2) ** 0.5)

    @staticmethod
    def get_distance_to_curve(line, point):
        """Fonction permettant de retourner la distance minimale entre une ligne et un point

        Parameters
        ----------
        line: `pd.Series`
            Information sur la section de spline
        point: `list`
            coordonées x et y du point à localiser

        Returns
        -------
        distance: `float`
            distance minimale entre le point et la droite
        """
        return DISTANCE_ERROR + 1
        #TODO : faire la fonction qui retourne la distance entre une courbe et un point

    @staticmethod
    def geo_to_position(longitude, latitude):
        """A partir de la longitude et de la latitude retourne la position en m par rapport à 0°, 0°

        Parameters
        ----------
        longitude: `float`
            Longitude du point
        latitude: `float`
            Latitude du point

        Returns
        -------
        x: `float`
            Position x par rapport au point 0° 0°
        y: `float`
            Position y par rapport au point 0° 0°
        """
        return longitude, latitude
        #TODO : faire l'algorithme de conversion longitude/latitude -> x/y (en m)

    def get_geo_from_pk(self, pk):
        return 0, 0
        #TODO : fonction permettant de retourner les coordonées géographiques à partir d'un point kilométrique
        # Possibilité de le divier en 2 fonctions comme geo_to_position()


    def get_more_restrictive(self, pk_begin, pk_end):
        """Fonction permettant de retourner le profil le plus contraignant entre les pk_begin et pk_end.
        Si pk_begin < pk_end -> on considèrera que la voie est prise en direction opposée).

        Parameters
        ----------
        pk_begin: `int`
            Le pk de début de la vérification (le profil retourné se trouvera après ce PK)
        pk_end: `int`
            Le pk de fin de la vérification (le profil retourné se trouve avant ce PK)

        Returns
        -------
        curve_radius: `float`
            Le rayon de courbure du profile le plus contraignant
        slope: `float`
            La pente/rampe du profil le plus contraignant
        """
        return 0, 0
        # TODO: faire la fonction permettant de retourner le profil le plus restrictif entre deux pk
