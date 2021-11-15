# Librairies par défaut
import sys
import os
import time


# Librairies de traitement de données
import pandas
import numpy


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

    def __init__(self):
        """Initialise le générateur de ligne en chargeant toutes les bases de données"""
        initial_time = time.time()
        log.change_log_prefix("initialisation des données lignes")
        log.info("Chargement des bases de données pour la génération des lignes.\n")

        # Chargement des lignes existantes et de la liste des voies sur le RFN
        self.lines = pandas.read_csv(self.lines_path, delimiter=";", usecols=self.lines_attr)
        self.tracks = pandas.read_csv(self.tracks_path, delimiter=";", usecols=self.tracks_attr)

        # Chargement des éléments nécessaires à la génération de la ligne (courbe des voies, déclivités, vitesses maximales)
        self.curves = pandas.read_csv(self.curves_path, delimiter=";", usecols=self.curves_attr)
        self.slopes = pandas.read_csv(self.slopes_path, delimiter=";", usecols=self.slopes_attr)
        self.max_speed = pandas.read_csv(self.max_speed_path, delimiter=";", usecols=self.max_speed_attr)
        self.electrification = pandas.read_csv(self.electrification_path, delimiter=";", usecols=self.electrification_attr)

        # Indique le temps de chargement des bases de données
        log.info("Chargement de toutes les bases de données en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " milisecondes.\n\n")

    def generate_line(self, line_code, reload=False):
        """Fonction permettant de générer les données lignes (Python et UE5) à partir du code ligne

        Parameter
        ---------
        line_code: `int`
            Code de la ligne (trouvable en ligne selon le nom de la ligne
        """
        # Vérifie que la ligne n'existe pas encore et si non la recharge
        if str(line_code) in os.listdir(PROJECT_DIR + "settings\\line_settings\\" + str(line_code)) and not reload:
            log.info("La ligne " + str(line_code) + " existe déjà. Elle ne sera pas recréée.\n\n")
            return

        # Vérifie que la ligne qu'on essaye de charger existe
        line_name = self.lines.loc[self.lines["CODE_LIGNE"] == line_code]
        if not line_name:
            log.warning("Aucune ligne existance avec le code_ligne : " + str(line_code) + ".\n\n")
            return

        # Sinon indique le nom et les informations clés de la ligne en question




if __name__ == "__main__":
    read_raw_data()
