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
import src.misc.decorators.decorators as decorators
import src.misc.log.log as log
import src.initialisation.signals.page_rb.page_rb2 as prb2


class ComplexPopup:
    """classe contenant toutes les fonctions pour la page de paramètre train en mode complexe"""

    # Eléments nécessaires au fonctionnement de la popup
    loaded = False
    app = None
    engine = None
    win = None

    # Base de données train utile au paramétrage
    train_database = None

    # Stocke la page parent
    parent = None

    # Constantes sur les emplacements des différents fichiers et dossiers nécessaires au fonctionement de la popup
    graphic_file_path = f"{PROJECT_DIR}src\\initialisation\\graphics\\page_rb\\page_rb2\\complex_popup.qml"

    def __init__(self, page_rb):
        """Fonction d'initialisation de la popup de paramétrage complexe train (reliée à la page_rb2)

        Parameters
        ----------
        page_rb: `prb2.PageRB2`
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
            self.parent = page_rb
            self.win.findChild(QObject, "generate_button").clicked.connect(self.on_complex_generate_clicked)
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

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def on_complex_generate_clicked(self):
        """Fonction activée lorsque le bouton généré est cliqué"""
        try:
            # Génère le train à partir des données simples
            simple_parameters = self.parent.get_simple_mode_values()
            self.train_database = tdb.TrainDatabase(simple_parameters)
        except Exception as error:
            # S'il y a une erreur, laisse un message d'erreur et désactive le mode complexe
            log.error("Impossible de correctement générer le train, mode complexe désactivé.\n",
                      exception=error, prefix="Génération train complexe")
            self.win.hide()
            self.win.setProperty("generated", False)
            self.parent.page.setProperty("generated", False)
            mode_switchbutton = self.parent.page.findChild(QObject, "mode_switchbutton")
            mode_switchbutton.change_selection(0)
            mode_switchbutton.setProperty("is_activable", False)
            self.loaded = False
        else:
            # Sinon indique aux différentes pages que le mode complexe de paramétrage a été activé
            self.parent.current_mode = self.parent.Mode.COMPLEX
            self.win.setProperty("generated", True)
            self.parent.page.setProperty("generated", True)

            # Récupère la liste de chacunes des positions des voitures
            self.win.setProperty("mission_list", self.train_database.systems.get_mission_list())
            self.win.setProperty("position_list", self.train_database.systems.get_position_list())

            # Appelle la fonction permettant de mettre à jour les différentes constantes
            self.update_constants(simple_parameters)

            # Appelle la fonction de mise à jour pour montrer la première voiture
            # TODO : initialiser la première voiture

    def update_constants(self, train_data):
        """Fonction permettant de mettre à jour les différentes constantes de la popup complexe

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Les paramètres du train (certains paramètres doivent être convertis du train à la voiture/au bogie
        """
        # Commence par mettre à jour les valeurs par défaut selon la moyenne des paramètres entrés
        self.win.setProperty("default_axles_count", train_data.get_value("axles_per_bogie", 2))
        self.win.setProperty("default_axles_power", train_data.get_value("axles_power", 750.0))
        self.win.setProperty("default_pad_brakes_count", round(train_data.get_value("pad_brakes_count", 0) / train_data.get_value("bogies_count", 1)))
        self.win.setProperty("default_disk_brakes_count", round(train_data.get_value("disk_brakes_count", 0) / train_data.get_value("bogies_count", 1)))
        self.win.setProperty("default_magnetic_brakes_count", round(train_data.get_value("magnetic_brakes_count", 0) / train_data.get_value("bogies_count", 1)))
        self.win.setProperty("default_foucault_brakes_count", round(train_data.get_value("foucault_brakes_count", 0) / train_data.get_value("bogies_count", 1)))

        # Puis met à jour les différentes limites
        self.win.setProperty("max_bogies_per_railcar", max(self.parent.page.property("max_bogies_per_railcar"), 2))
        self.win.setProperty("max_axles_per_bogies", self.parent.page.property("max_axles_per_bogie"))
        self.win.setProperty("max_axles_power", self.parent.page.property("max_axles_power"))
        self.win.setProperty("max_pad_brakes_per_axle", self.parent.page.property("max_pad_brakes_per_axle"))
        self.win.setProperty("max_disk_brakes_per_axle", self.parent.page.property("max_disk_brakes_per_axle"))
        self.win.setProperty("max_magnetic_brakes_per_axle", self.parent.page.property("max_magnetic_brakes_per_axle"))

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
        """"""

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
