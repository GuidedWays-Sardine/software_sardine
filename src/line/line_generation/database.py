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

# Chemin d'accès vers les données
DATA_DIR = f"{PROJECT_DIR}src\\line\\raw_data\\"

# Constantes sur les noms des colonnes
GEO_LO = "GEO_LO"
GEO_LA = "GEO_LA"
PK = "PK"
DEBUT = "_D"
FIN = "_F"


class DataBase:
    """Class permettant de gérer les bases de données"""
    path = ""
    attr = []
    link = ""
    df = None

    def __init__(self, path, attr, link="", df=None):
        """Fonction d'initialisation d'une base de donnée.
        Attention, cette fonction ne charge pas la base de données. Pour ceci, appeler la fonction self.load()

        Parameters
        ----------
        path: `str`
            Chemin d'accès vers la base de données à partir de src\\line\\raw_data\\.
        attr: `list`
            Liste des attributs à récupérer (doivent être présents dans la base de données.
        link: `str`
            Lien vers la base de données (à titre indicatif, pas obnligatoire pour le fonctionnement).
        df: `pd.DataFrames`
            Potentiel database si la base a été chargée auparavant.
        """
        self.path = (DATA_DIR if DATA_DIR not in path else "") + path.replace("/", "\\")
        self.attr = attr
        self.link = link
        self.df = df

    def load(self):
        """Fonction permettant de charger la base de donnée. Si elle est déjà chargée, aucune action sera réalisée"""
        # Vérifie que la base de données n'a pas déjà été chargée
        if self.df is not None:
            return False

        # Si la base de donnée doit être chargée, commence par ouvrir et lire les données du fichier indiqué
        initial_time = time.time()
        self.df = pd.read_csv(self.path, delimiter=";", usecols=self.attr)[self.attr]

        # Gère en deuxième lieu la conversion de tous les paramètres par défaut (Point Kilométrique et Position Géographique)

        # Convertit le code_ligne en np.int32 (pour limiter l'espace pris)
        if "CODE_LIGNE" in self.attr:
            self.df["CODE_LIGNE"] = self.df["CODE_LIGNE"].astype(np.int32)

        # Pour toutes les colonnes mentionnant des positions géographiques
        # (Actuellement les colonnes C_GEO sont de la forme : "GEO_longitude,GEO_latitude")
        geo_index = [g_i for g_i in range(len(self.attr)) if "c_geo" in self.attr[g_i].lower()]
        for i in range(0, len(geo_index)):
            # Récupère la liste, sépare et convertit en float, les positions de longitude et de latitude
            split_geo_points = self.df[self.attr[geo_index[i] + i]].str.split(",", expand=True).astype(np.float64)

            # Change les valeurs de la colonne existante pour la longitude et en insert une nouvelle pour la latitude
            self.df[self.attr[geo_index[i] + i]] = split_geo_points[0]
            self.df.insert(geo_index[i] + i + 1, GEO_LA + str(i), split_geo_points[1])

            # Change le nom des colonnes pour garder un format compréhensible et normalisé
            self.attr[geo_index[i] + i] = GEO_LO + (DEBUT if "D" in self.attr[geo_index[i] + i]
                                                    else FIN if "F" in self.attr[geo_index[i] + i]
                                                    else "")
            self.attr.insert(geo_index[i] + i + 1, GEO_LA + (DEBUT if "D" in self.attr[geo_index[i] + i]
                                                             else FIN if "F" in self.attr[geo_index[i] + i]
                                                             else ""))
            # Le nom des colonnes dans la dataFrame seront changés en fin de processus

        # Pour toutes les colonnes mentionnant des Points Kilométriques
        # (Actuellement les PK sont au format 1+090 ou 0-365 -> convertir en nombres à virgules et convertir en float)
        for pk_i in [pk_i for pk_i in range(len(self.attr)) if "pk" in self.attr[pk_i].lower()]:
            # Certains PK sont de la forme D+090 -> les convertit en nombres
            self.df.loc[self.df[self.attr[pk_i]].str.contains("^[a-zA-Z].*", regex=True), self.attr[pk_i]] = \
                (self.df[self.attr[pk_i]].str.get(0).apply(ord) - 64).astype("string") + self.df[self.attr[pk_i]].str[1:]

            #  Remplace les + et - par des . et trasnforme en type np.float32 (PK en km mais avec des imprécisions)
            # self.df[self.attr[pk_i]] = (np.where(self.df[self.attr[pk_i]].str.contains("-"), "-", "") +
            #                            self.df[self.attr[pk_i]].str.replace("[-+]", ".", regex=True)).astype(np.float32)

            # Supprime les + et - pour convertir en m et transforme en type np.int32 (PK en m mais sans imprécisions)
            self.df[self.attr[pk_i]] = (np.where(self.df[self.attr[pk_i]].str.contains("-"), "-", "")
                                        + self.df[self.attr[pk_i]].str.replace("[-+]", "", regex=True)).astype(np.int32)

            # Actualise le nom de la colonne PK pour normaliser
            self.attr[pk_i] = PK + (DEBUT if "D" in self.attr[pk_i] else FIN if "F" in self.attr[pk_i] else "")

        # Change le nom des colonnes
        self.df.columns = self.attr

        # Trie les colonnes par CODE_LIGNE et par PK (ou PK_D)
        if any([pk for pk in self.attr if PK in pk]):
            self.df.sort_values(by=["CODE_LIGNE", PK + (DEBUT if (PK + DEBUT) in self.attr else "")]).reset_index(drop=True)

        # Indique le temps de chargement et de normaliusation de la base de données
        log.info(f"Base de données : {self.path[len(DATA_DIR)::]} chargée en : {((time.time() - initial_time) * 1000):.2f} milisecondes.\n")
        return True
