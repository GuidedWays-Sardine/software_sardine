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
        #self.tracks = pandas.read_csv(self.tracks_path, delimiter=";", usecols=self.tracks_attr)

        # Chargement des éléments nécessaires à la génération de la ligne (courbe des voies, déclivités, vitesses maximales)
        #self.curves = pandas.read_csv(self.curves_path, delimiter=";", usecols=self.curves_attr)
        #self.slopes = pandas.read_csv(self.slopes_path, delimiter=";", usecols=self.slopes_attr)
        #self.max_speed = pandas.read_csv(self.max_speed_path, delimiter=";", usecols=self.max_speed_attr)
        #self.electrification = pandas.read_csv(self.electrification_path, delimiter=";", usecols=self.electrification_attr)

        # Indique le temps de chargement des bases de données
        log.info("Chargement de toutes les bases de données en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " milisecondes.\n\n")

    def test(self, line_code):
        """
        .head() -> affiche les premiers
        .tail() -> affiche les derniers
        .shape -> nb lignes, nb_atributes
        .describe() -> donne le nombre de valeurs, le nombre de valeurs différentes et la valeur avec la valeur la plus élevée
        .columns -> Le nom des colonnes
        .index -> le numéro des lignes (avec pandas, l'index est indépendant de [])
        .columns = ["", "",...]-> pour renommer les colonnes
        ["column_name] -> retourne la colonne avec se nom en format Series (DataFrame avec un seul colonne)
        .loc[index, "column_name"]      attention index
        .loc[index, "first_column":"end_column"]
        ["column"][index]
        .loc[index]["column_index"]
        .loc[5, ["column_1", "column_2", ...]]
        .iloc[index, index_column]
        .iloc[index, index_columb_begin:index_column_end]
        .iloc/loc[index_begin:index_end, ...]
        ["column_name"].mean()

        .append({"column_1":...})



        mask = ...["column_1", ...] > value
        si plusieurs colomnes, valeurs comparés sur plusieurs colones
        stock colomne avec le résultat pour toutes les lignes. Permet de rendre le tableau plus lisible

        ...[mask]

        .dtypes -> type de chaque colonne
        si string ou truc au pif -> object
        df.index[0]     -> index de la première ligne
        .drop[index, inplace=True]      -> inplace indique si le nouveau tableau doit être retourné, ou s'il doit être stocké dans le tableau actuel
        .to_list() -> transforme la Series en Liste
        .dropna() -> supprime toutes les colonnes qui contient un NaN dans une des valeurs
        .drop_duplicate()   -> supprime toutes les lignes en doubles
        .reset_index(drop=True)      -> reset tous les index (0, 1,...) (drop sinon ça garde les anciens index dans une colonnes)
        .where(mask, inplace=True)  -> remplace toutes les cas ou le mask retourne true en NaN
        .replace(old_value, new_value)  -> à regarder plus en détail ?
        .isin([])       -> regarde si la valeur est cases sont dans cette list
        .copy()         -> renvoie une copie (pas un pointeur)
        .datetime()     -> pour les dates ?
        np.vectorize(lambda...)     -> parfois rapide que juste df["column_name"] = ...
        ~signifie l'inverse
        .concat()       -> existe mais peu utile pour le projet
        .merge()        -> existe mais peu utile pour le projet
        regex (re)      -> pour des recherches pas complètes
        df["A"] = pd.to_numeric(df["A"], downcast="float")
        df["column_name"].astype(type)      -> attention string object donc possibilité que ça ne marche pas
        pas de for dans les tableaux        -> truc que j'ai loupé -> vectorisation pour l'optimiser
        https://www.google.com/url?sa=i&url=https%3A%2F%2Fstackoverflow.com%2Fquestions%2F52783882%2Fpandas-and-numpy-program-slower-than-loop-version-of-same-functionality-how-to&psig=AOvVaw1X5Q98avR9f1Ipj9jDxT2k&ust=1637102449664000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCKDlvYO4m_QCFQAAAAAdAAAAABAD
        .sort pour trier()
        """
        print(self.lines.head(10))

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
    log.initialise("../../../log", "1.1.0", log.Level.DEBUG)

    # Codes pour la LGV Sud-Est
    line_generator = LineGenerator()
    line_generator.test(752000)
    #line_generator.generate_line(752000)

