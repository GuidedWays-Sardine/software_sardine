# Librairies par défaut
import os
import sys
import time
from enum import Enum


# Librairies graphiques
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QFileDialog


#Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.initialisation.initialisation_window as ini
import src.misc.settings_dictionary.settings as sd
import src.misc.translation_dictionary.translation as td
import src.misc.log.log as log


class ComplexPopup:
    """classe contenant toutes les fonctions pour la page de paramètre train en mode complexe"""

    # Eléments nécessaires au fonctionnement de la popup
    loaded = False
    app = None
    engine = None
    win = None
    parent = None


    def __init__(self, page_rb):
        """Fonction d'initialisation de la popup de paramétrage complexe train (reliée à la page_rb2)

        Parameters
        ----------
        page_rb: `PageRB2`
            La page de paramètres train (permettant d'accéder aux widgets du mode simple
        """
        log.change_log_prefix("Initialisation popup train")
        self.parent = page_rb

        # Initialise la popup de paramétrage complexe
        self.engine = QQmlApplicationEngine()
        self.engine.load(f"{PROJECT_DIR}src\\initialisation\\graphics\\page_rb\\page_rb2\\complex_popup.qml")

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon laisse un message d'erreur
        if self.engine.rootObjects():
            log.info("Chargement de la popup de paramétrage complexe réussi avec succès.\n")
            self.win = self.engine.rootObjects()[0]
            self.win.hide()

            # Récupère le bouton des modes, le rend activable et le connecte à sa fonction
            self.win.closed.connect(lambda: self.win.hide())

            # Connecte tous les boutons nécessaires au fonctionnement de la popup de paramétrage complex
            self.win.findChild(QObject, "generate_button").clicked.connect(self.on_complex_generate_clicked)

            # TODO : connecter tous les autres boutons

            # Indique que la fenêtre est chargée
            self.loaded = True
        else:
            # Sinon laisse un message de warning selon si le fichier est introuvable ou contient des erreurs
            if os.path.isfile(f"{PROJECT_DIR}src\\initialisation\\graphics\\page_rb\\page_rb2\\complex_popup.qml"):
                log.warning("Impossible de charger la popup de configuration complexe. Le fichier complex_popup.qml contient des erreurs.\n")
            else:  # Cas où le fichier n'existe pas
                log.warning("Impossible de charger la popup de configuration complexe. Le fichier complex_popup.qml n'a pas été trouvé.\n")

        log.change_log_prefix("Initialisation")

    def on_complex_generate_clicked(self):
        """Fonction activée lorsque le bouton généré est cliqué"""
        # Indique aux différentes pages que le mode complexe de paramétrage a été activé
        self.parent.current_mode = self.parent.Mode.COMPLEX
        self.parent.page.setProperty("generated", True)
        self.parent.setProperty("generated", True)

        #TODO  générer une structure de train

    def get_complex_mode_values(self):
        """Fonction permettant de récupérer toutes les informations de la configuration simple

        Returns
        ----------
        train_parameters: `sd.SettingsDictionary`
            Dictionaire de paramètre avec tous les paramètres complexes du train
        """
        parameters = sd.SettingsDictionary()

        # TODO : sauvegarder les données

        return parameters