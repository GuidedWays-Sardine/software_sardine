# Librairies par défaut
import os
import sys


# librairies graphiques
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


class B01:
    """Classe contenant les éléments d'initialisation et de mise à jour de la page B01 de section B du DMI ETCS ETCS"""

    # variables nécessaire au bon fonctionnement de la page
    section = "B"
    page_name = "B01"
    engine = None
    page = None


    # séries de tests suivant la documentation DMI (pour s'assurer que les différents modules fonctionne bien
    tests = [[400, "FS", "CSM", "NoS", 25, -1, 160, -1, 138],
             [400, "FS", "CSM", "NoS", 25, -1, 160, -1, 67],
             [400, "FS", "CSM", "Nos", 25, -1, 100, -1, 67],
             [400, "FS", "TSM", "Inds", 25, 100, 150, -1, 138],
             [400, "FS", "TSM", "IndS", 25, 100, 140, -1, 109],
             [400, "FS", "TSM", "IndS", 30, 0, 78, -1, 67],
             [400, "FS", "TSM", "WaS", 30, 0, 52, 72, 67],
             [400, "FS", "TSM", "Ints", 30, 0, 39, 49, 61],
             [400, "FS", "RSM", 'IndS', 30, 0, 14, -1, 25],
             [400, "FS", "TSM", "IndS", 25, 0, 140, -1, 133],
             [400, "FS", "CSM", "NoS", 25, -1, 140, -1, 133],
             [250, "FS", "CSM", "NoS", 25, -1, 140, -1, 133],
             [180, "FS", "CSM", "NoS", 25, -1, 140, -1, 133],
             [140, "FS", "CSM", "NoS", 25, -1, 100, -1, 96],
             [400, "FS", "CSM", "NoS", 25, -1, 140, -1, 133],
             [400, "FS", "TSM", "OvS", 30, 40, 132, 147, 143],
             [400, "FS", "CSM", "NoS", 30, 60, 140, -1, 133],
             [400, "OS", "CSM", "noS", 30, -1, 40, -1, 36],
             [400, "OS", "TSM", "IndS", 30, 0, 40, -1, 36],
             [400, "SR", "TSM", "IndS", 30, 90, 117, -1, 102],
             [400, "FS", "RSM", "IndS", 25, 0, 52, -1, 28],
             [400, "FS", "RSM", "IndS", 25, 0, 12, -1, 19]]

    index = 0

    def __init__(self, engine, section, page_name): # TODO : voir pour envoyer le DMI ou la simulation et la dmi_key
        """Fonction permettant d'initialiser la page B01 de la section B du DMI ETCS ETCS

        Parameters
        ----------
        engine: `QQmlApplicationEngine`
            La QQmlApplicationEngine de la page
        section: `string`
            La clé de la section de la page
        page_name: `string`
            Le nom de la page
        """
        self.section = section
        self.page_name = page_name
        self.engine = engine
        self.page = engine.rootObjects()[0]

    def update(self):  # TODO : voir si la fonction récupère la base de donnée EVC
        """Fonction permettant de mettre à jour l'EVC"""
        test = self.tests[self.index]
        self.page.setProperty("max_speed", test[0])
        self.page.setProperty("operating_mode", test[1])
        self.page.setProperty("speed_monitoring", test[2])
        self.page.setProperty("status_information", test[3])
        self.page.setProperty("release_speed", test[4])
        self.page.setProperty("target_speed", test[5])
        self.page.setProperty("permitted_speed", test[6])
        self.page.setProperty("brake_speed", test[7])
        self.page.setProperty("speed", test[8])
        self.index = (self.index + 1) % len(self.tests)
