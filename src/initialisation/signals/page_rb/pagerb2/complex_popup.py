# Librairies par défaut
import os
import sys
import time


# Librairies graphiques
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


#Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.train.train_database.database as tdb
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

    # Base de données train utile au paramétrage
    train_database = None

    # Constantes sur les emplacements des différents fichiers et dossiers nécessaires au fonctionement de la popup
    graphic_file_path = f"{PROJECT_DIR}src\\initialisation\\graphics\\page_rb\\page_rb2\\complex_popup.qml"

    def __init__(self, page_rb):
        """Fonction d'initialisation de la popup de paramétrage complexe train (reliée à la page_rb2)

        Parameters
        ----------
        page_rb: `PageRB2`
            La page de paramètres train (permettant d'accéder aux widgets du mode simple)

        Raises
        ------
        FileNotFoundError
            Soulevé quand le fichier .qml de la fenêtre d'initialisation n'est pas trouvé
        SyntaxError
            Soulevé quand le fichier .qml de la fenêtre d'initialisation a une erreur de syntaxe et n'est pas lisible
        """
        log.change_log_prefix("Initialisation popup train")

        # Initialise la popup de paramétrage complexe
        self.engine = QQmlApplicationEngine()
        self.engine.load(self.graphic_file_path)

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon laisse un message d'erreur
        if self.engine.rootObjects():
            self.win = self.engine.rootObjects()[0]
            self.win.hide()

            # Récupère le bouton des modes, le rend activable et le connecte à sa fonction
            self.win.closed.connect(lambda: self.win.hide())

            # Connecte tous les boutons nécessaires au fonctionnement de la popup de paramétrage complex
            self.win.findChild(QObject, "generate_button").clicked.connect(lambda p=page_rb: self.on_complex_generate_clicked(p))
            # TODO : connecter tous les autres boutons

            # Indique que la fenêtre est complètement
            self.loaded = True
            log.info("Chargement de la popup de paramétrage complexe réussi avec succès.")
            log.change_log_prefix("Initialisation")
        else:
            # Sinon laisse un message de warning selon si le fichier est introuvable ou contient des erreurs
            if os.path.isfile(self.graphic_file_path):
                raise SyntaxError(f"le fichier graphique de la popup complexe contient des erreurs.\n\t{self.graphic_file_path}")
            else:  # Cas où le fichier n'existe pas
                raise FileNotFoundError(f"Le fichier graphique de la popup complexe n'a pas été trouvé.\n\t{self.graphic_file_path}")

    def on_complex_generate_clicked(self, page_rb):
        """Fonction activée lorsque le bouton généré est cliqué

        Parameters
        ----------
        page_rb: `PageRB2`
            La page de paramètres train (permettant d'accéder aux widgets du mode simple
        """


        try:
            # Génère le train à partir des données simples
            simple_parameters = parent.get_simple_mode_values()
            self.train = cd.Train(simple_parameters)
        except Exception as error:
            # S'il y a une erreur, désactive le mode complex et laisse un message d'erreur et désactive le mode complexe
            log.error("Impossible de correctement générer le train, mode complexe désactivé.\n",
                      exception=error, prefix="Génération train complexe")
            self.win.hide()
            mode_button = parent.page.findChild(QObject, "mode_button")
            mode_button.setProperty("text", parent.mode_switch[mode_button.property("text")])
            mode_button.setProperty("is_activable", False)
            self.loaded = False
        else:
            # Sinon indique aux différentes pages que le mode complexe de paramétrage a été activé
            parent.current_mode = parent.Mode.COMPLEX
            self.win.setProperty("generated", True)
            parent.page.setProperty("generated", True)

            # Récupère la liste des types et des positions de chacunes des voitures
            self.win.setProperty("type_list", [c.mission_type.value for c in self.train.railcars_list])
            self.win.setProperty("position_list", [c.position_type.value for c in self.train.railcars_list])

    def reset(self):
        """Fonction permettant de réinitialiser le mode complexe (supression des données)"""
        # Passe la base de données train à None (elle devra être recréée après)
        self.train_database = None

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

    def set_complex_mode_values(self, train_data):
        pass

    def change_language(self, translation_data):
        """Fonction permettant de traduire la page de paramétrage train complet (appelé dans la page_rb2

        Parameters
        ----------
        translation_data: `td.TranslationData`
            Dicionnaire de traduction contenant toutes les traductions nécessaires"""
        # Commence par traduire les différents textes visibles (fenêtre de génération)
        for widget_id in ["generate_button", "generate_l1", "generate_l2"]:
            widget = self.win.findChild(QObject, widget_id)
            widget.setProperty("text", translation_data[widget.property("text")])

        # Continue par traduire les textes des paramètres bogies
        for widget_id in ["front_bogie", "middle_bogie", "back_bogie"]:
            widget = self.win.findChild(QObject, widget_id)

            # Traduit chacuns des mots contenue dans le widget bogie parameters
            for parameter in ["articulated_text", "axle_text", "motor_text",
                              "pad_text", "disk_text", "magnetic_text", "foucault_text"]:
                widget.setProperty(parameter, translation_data[widget.property(parameter)])
