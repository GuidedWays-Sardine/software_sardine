# Librairies par défaut
import sys
import os
import time
import pandas as pd


#librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


DATA_DIR = PROJECT_DIR + "src\\line\\raw_data\\"


class LineGenerator:
    # Lignes existantes sur le RFN
    lines_link = "https://ressources.data.sncf.com/explore/dataset/lignes-par-statut/table/"
    lines_path = DATA_DIR + "line\\lignes-par-statut.csv"
    lines_attr = ["CODE_LIGNE", "LIB_LIGNE", "STATUT", "PKD", "PKF", "C_GEO_D"]
    lines = None

    # Liste des voies sur le RFN
    tracks_link = "https://ressources.data.sncf.com/explore/dataset/fichier-de-formes-des-voies-du-reseau-ferre-national/table/"
    tracks_path = DATA_DIR + "line\\fichier-de-formes-des-voies-du-reseau-ferre-national.csv"
    tracks_attr = ["CODE_LIGNE", "NOM_VOIE", "PK_DEBUT_R", "PK_FIN_R"]
    tracks = None


    # Données reliées aux courbes
    curves_link = "https://ressources.data.sncf.com/explore/dataset/courbe-des-voies/table/"
    curves_path = DATA_DIR + "line\\courbe-des-voies.csv"
    curves_attr = ["CODE_LIGNE", "PKD", "PKF", "C_GEO_D", "C_GEO_F", "SENS", "RAYON"]
    curves = None

    # Données reliées aux déclivités
    slopes_link = "https://ressources.data.sncf.com/explore/dataset/caracteristique-des-voies-et-declivite/table/"
    slopes_path = DATA_DIR + "line\\caracteristique-des-voies-et-declivite.csv"
    slopes_attr = ["CODE_LIGNE", "NOM_VOIE", "TYPE", "VALEUR", "PKD", "PKF", "C_GEO_D", "C_GEO_F"]
    slopes = None

    # Données reliées à la vitesse maximale
    max_speed_link = "https://ressources.data.sncf.com/explore/dataset/vitesse-maximale-nominale-sur-ligne/table/"
    max_speed_path = DATA_DIR + "line\\vitesse-maximale-nominale-sur-ligne.csv"
    max_speed_attr = ["CODE_LIGNE", "V_MAX", "PKD", "PKF", "C_GEO_D", "C_GEO_F"]
    max_speed = None

    # Données reliées à l'électrification des lignes
    electrification_link = "https://ressources.data.sncf.com/explore/dataset/liste-des-lignes-electrifiees/table/"
    electrification_path = DATA_DIR + "line\\liste-des-lignes-electrifiees.csv"
    electrification_attr = ["CODE_LIGNE", "ELECT", "PKD", "PKF", "C_GEO_D", "C_GEO_F"]
    electrification = None





if __name__ == "__main__":
    read_raw_data()
