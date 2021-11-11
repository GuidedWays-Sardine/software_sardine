# Librairies par défaut
import sys
import os
import time
import pandas as pd


#librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


def read_raw_data():
    initial_time = time.time()
    columns = ["NOM_VOIE", "CODE_LIGNE", "LIB_LIGNE", "SENS", "RAYON", "PKD", "PKF", "C_GEO_D", "C_GEO_F"]
    df = pd.read_csv(PROJECT_DIR + "src\\line\\raw_data\\courbe-des-voies.csv", delimiter=";", usecols=columns)
    #print(df)
    print(int((time.time() - initial_time) * 1000))





# Récupération des données SNCF
# Trie de ses données (pour garder que les données utile au tracé) et les mets dans l'ordre
# Convertis tout en courbe de Bésziers pour pour facilement pouvoir placer des ékéments
# Reconvertit tout en données compatible UE5
# Les sauvegardes




if __name__ == "__main__":
    read_raw_data()
