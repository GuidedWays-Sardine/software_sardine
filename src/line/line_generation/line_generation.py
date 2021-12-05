# Librairies par défaut
import sys
import os
import time
import traceback


# Librairies de traitement de données
import pandas as pd
import numpy as np


#librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.line.line_generation.database as DB
import src.line.line_generation.spline as SP


class LineGenerator:
    """Classe contenant toute la logique pour générer la ligne à partir des bases de données"""

    # Bases de données nécessaires à la génération de la ligne
    lines = DB.DataBase("line\\lignes-par-statut.csv",
                        ["CODE_LIGNE", "LIB_LIGNE", "STATUT", "PKD", "PKF", "C_GEO_D", "C_GEO_F"],
                        "https://ressources.data.sncf.com/explore/dataset/lignes-par-statut/table/")

    tracks = DB.DataBase("line\\fichier-de-formes-des-voies-du-reseau-ferre-national.csv",
                         ["CODE_LIGNE", "NOM_VOIE", "PK_DEBUT_R", "PK_FIN_R", "Geo Shape"],
                         "https://ressources.data.sncf.com/explore/dataset/fichier-de-formes-des-voies-du-reseau-ferre-national/table/")

    curves = DB.DataBase("line\\courbe-des-voies.csv",
                         ["CODE_LIGNE","NOM_VOIE", "SENS", "RAYON", "PKD", "PKF", "C_GEO_D", "C_GEO_F"],
                         "https://ressources.data.sncf.com/explore/dataset/courbe-des-voies/table/")

    slopes = DB.DataBase("line\\caracteristique-des-voies-et-declivite.csv",
                         ["CODE_LIGNE", "NOM_VOIE", "TYPE", "VALEUR", "PKD", "PKF", "C_GEO_D", "C_GEO_F"],
                         "https://ressources.data.sncf.com/explore/dataset/caracteristique-des-voies-et-declivite/table/")

    max_speed = DB.DataBase("line\\vitesse-maximale-nominale-sur-ligne.csv",
                            ["CODE_LIGNE", "V_MAX", "PKD", "PKF", "C_GEO_D", "C_GEO_F"],
                            "https://ressources.data.sncf.com/explore/dataset/vitesse-maximale-nominale-sur-ligne/table/")

    electrification = DB.DataBase("line\\liste-des-lignes-electrifiees.csv",
                                  ["CODE_LIGNE", "ELECT", "PKD", "PKF", "C_GEO_D", "C_GEO_F"],
                                  "https://ressources.data.sncf.com/explore/dataset/liste-des-lignes-electrifiees/table/")

    def __init__(self):
        """Initialise la liste des lignes"""
        # Initialise la base de données lignes
        log.change_log_prefix("line generator")
        self.lines.load()

    def generate_line(self, line_code, reload=False):
        """Fonction permettant de générer les données lignes (Python et UE5) à partir du code ligne

        Parameter
        ---------
        line_code: `int`
            Code de la ligne (trouvable en ligne selon le nom de la ligne
        """
        # Si la ligne existe déjà (enregistrée dans settings/line_settings/line_code) et qu'elle ne doit pas être rechargée, retourne
        if str(line_code) in os.listdir(PROJECT_DIR + "settings\\line_settings") and not reload:
            log.info("La ligne " + str(line_code) + " existe déjà. Elle ne sera pas recréée.\n\n")
            return

        # Vérifie que la ligne qu'on essaye de charger existe, sinon arrête le chargement de la ligne
        line_name = list(self.lines.df.loc[self.lines.df["CODE_LIGNE"] == line_code, "LIB_LIGNE"])
        if not line_name:
            log.warning("Aucune ligne existance avec le code_ligne : " + str(line_code) + ".\n\n")
            return
        else:
            # Sinon indique le nom et les informations clés de la ligne en question
            log.info("Génération de la ligne " + line_name[0] + ".\n")

        # charge le reste des bases de données ligne (si ce n'est pas déjà fait)
        self.load_line_databases()

        # Génère la liste de toutes les splines de la ligne
        line_splines = self.generate_splines_data(self.tracks.df.loc[self.tracks.df["CODE_LIGNE"] == line_code].reset_index(drop=True),
                                                  self.curves.df.loc[self.curves.df["CODE_LIGNE"] == line_code].reset_index(drop=True),
                                                  self.slopes.df.loc[self.slopes.df["CODE_LIGNE"] == line_code].reset_index(drop=True),
                                                  self.max_speed.df.loc[self.max_speed.df["CODE_LIGNE"] == line_code].reset_index(drop=True),
                                                  self.electrification.df.loc[self.electrification.df["CODE_LIGNE"] == line_code].reset_index(drop=True))

    def load_line_databases(self):
        """Charge toutes les bases de données reliées à la ligne"""
        initial_time = time.time()
        log.change_log_prefix("chargement des bases de données lignes")
        log.info("Chargement des bases de données pour la génération des lignes")

        # Chargement base de données voies
        if self.tracks.load():
            # Récupère à partir du linestring le premier et dernier point géographique
            self.tracks.df["Geo Shape"] = self.tracks.df["Geo Shape"].str.split("[\[\]]{2,}", n=2).str[1]
            self.tracks.df.insert(len(self.tracks.df.columns), DB.GEO_LO + DB.DEBUT,
                                  self.tracks.df["Geo Shape"].str.split("\], \[", n=1).str[0].str.split(", ").str[1].astype(np.float32))
            self.tracks.df.insert(len(self.tracks.df.columns), DB.GEO_LA + DB.DEBUT,
                                  self.tracks.df["Geo Shape"].str.split("\], \[", n=1).str[0].str.split(", ").str[0].astype(np.float32))
            self.tracks.df.insert(len(self.tracks.df.columns), DB.GEO_LO + DB.FIN,
                                  self.tracks.df["Geo Shape"].str.split("\], \[").str[-1].str.split(", ").str[1].astype(np.float32))
            self.tracks.df.insert(len(self.tracks.df.columns), DB.GEO_LA + DB.FIN,
                                  self.tracks.df["Geo Shape"].str.split("\], \[").str[-1].str.split(", ").str[0].astype(np.float32))

            # Enlève la colonne Geo Shape, plus utile pour les calculs
            self.tracks.df.drop("Geo Shape", axis=1, inplace=True)
            self.tracks.attr.pop()
            self.tracks.attr.append([DB.GEO_LO + DB.DEBUT, DB.GEO_LA + DB.DEBUT, DB.GEO_LO + DB.FIN, DB.GEO_LA + DB.FIN])

        # Chargement bases de données courbes
        if self.curves.load():
            # Gestion des cas où le rayon contient une valeur non lisible (le convertit en alignement et passe le rayon à 0)
            self.curves.df.loc[self.curves.df["RAYON"].str.contains("^[a-zA-Z].*", regex=True), "SENS"] = "ALIGNEMENT"
            self.curves.df.loc[self.curves.df["RAYON"].str.contains("^[a-zA-Z].*", regex=True), "RAYON"] = "0"
            self.curves.df["RAYON"] = self.curves.df["RAYON"].astype(np.int16)

        # Chargement des pentes et rampes
        if self.slopes.load():
            # Gestion du problème lié au pentes et rampes exprimés en % avec des ","
            self.slopes.df["VALEUR"] = np.where(self.slopes.df["VALEUR"].str.contains(","),
                                                self.slopes.df["VALEUR"].str.replace(",", ""),
                                                self.slopes.df["VALEUR"] + "0").astype(np.int8)

        # Chargement de la vitesse max pas tronçons
        self.max_speed.load()

        # Chargement de l'électrification des lignes
        self.electrification.load()

        # Indique le temps de chargement des bases de données
        log.info("Chargement de toutes les bases de données génération de ligne en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " milisecondes.\n\n")

    def generate_splines_data(self, tracks, curves, slopes, max_speed, electrification):
        """Permet à partir des données d'une ligne de générer la liste des splines nécessaires

        Parameters
        ----------
        tracks: `pd.DataFrame`
            Liste de toutes les voies de la ligne chargée
        curves: `pd.DataFrame`
            Liste de toutes les courbes de la ligne chargée
        slopes: `pd.DataFrame`
            Liste de toutes les pentes et ramples de la ligne chargée
        max_speed: `pd.DataFrame`
            Liste de toutes les vitesses maximales de la ligne chargée
        electrification: `pd.DataFrame`
            Liste des électrifications de la ligne actuelle
        """
        splines = []
        # Pour chacune des voies de la ligne, crée une nouvelle spline avec les informations de la voie
        for index, track in tracks.iterrows():
            # Récupère les informations principales pour la voir (pour simplifier la lecture des masques)
            track_name = track["NOM_VOIE"]
            pk_d = track[DB.PK + DB.DEBUT]
            pk_f = track[DB.PK + DB.FIN]

            # Crée la liste des splines au format
            splines.append(SP.Spline(track,
                                     curves.loc[(curves["NOM_VOIE"] == track_name) &
                                                (curves[DB.PK + DB.DEBUT] >= pk_d) &
                                                (curves[DB.PK + DB.FIN] <= pk_f)],
                                     slopes.loc[(slopes["NOM_VOIE"] == track_name) &
                                                (slopes[DB.PK + DB.DEBUT] >= pk_d) &
                                                (slopes[DB.PK + DB.FIN] <= pk_f)]))

        # Pour chacunes des voies créées, vérifie si le début et la fin de celle-ci n'est pas connectée à une autre spline
        for spline in splines:
            # Fait d'abord la vérification pour le pk de début
            possibly_connected = [s for s in splines if s is not spline and spline.pk_debut >= s.pk_debut and spline.pk_debut <= s.pk_fin]
            # Vérifier pour chacune des splines

            possibly_connected = [s for s in splines if s is not spline and spline.pk_fin >= s.pk_debut and spline.pk_fin <= s.pk_fin]
            # Vérifier pour chacune des splines


            # Pour le pk de début fait la vérification pour toutes les splines passant par le même PK

        # Pour chaque spline s'occupe
        # Pour chaque spline dans la liste de splie :
            # Crée la spline avec les informations par défaut
            # Vérifie par rapport au PKD et PKF sur toutes les autres splines ayant

def get_distance_to_line(line_begin, line_end, point):
    """

    :param line_:
    :param la_d:
    :param lo_f:
    :param la_f:
    :param x:
    :param y:
    :return:
    """
    # ax1 + b = y1      =>      a = (x1-x2)/(y1+y2)
    # ax2 + b = y2      =>      b = y1-x1*(x1-x2)/(y1+y2)
    a = (line_begin[0] - line_end[0])/(line_begin[1] + line_end[1])
    b = line_begin[1] - line_begin[0] * a

    # d =  |y - ax - b|/sqrt(1 + a²)
    print(abs(point[1] - a * point[1] - b) / ((1 + a ** 2) ** 0.5))

if __name__ == "__main__":
    log.initialise("../../../log", "1.1.0", log.Level.DEBUG)

    # Codes pour la LGV Sud-Est
    try:
        line_generator = LineGenerator()
        line_generator.generate_line(752000)
    except Exception as error:
        # Récupère une potentielle erreur lors de l'initialisation de la simulation
        log.critical("Erreur fatale lors de l'initialisation du simulateur\n\t\t" +
                     "Erreur de type : " + str(type(error)) + "\n\t\t" +
                     "Avec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                     "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                     prefix="")


