# Librairies par défaut
import os
import sys


# Librairies graphiques
from PyQt5.QtCore import QObject


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.initialisation.initialisation_window as ini
import src.misc.settings_dictionary.settings as sd
import src.misc.translation_dictionary.translation as td
import src.misc.log.log as log
import src.misc.decorators.decorators as decorators


class PageRB1:
    """Classe pour la page de paramètres 1"""

    # variables nécessaire au bon fonctionnement de la page
    index = 1  # Attention dans les tableaux l'index commence à 0
    name = "Général"
    engine = None
    page = None
    current_button = None

    # constantes de conversion entre le text du log_switchbutton et le niveau de registre associé
    log_converter = {"Complet": log.Level.DEBUG,
                     "Suffisant": log.Level.INFO,
                     "Minimal": log.Level.WARNING,
                     "Aucun": log.Level.NOTSET
                     }

    # Chemin vers les différents dossiers nécessaire au fonctionnement de la page
    command_board_folder_path = f"{PROJECT_DIR}src\\train\\command_board"
    dmi_folder_path = f"{PROJECT_DIR}src\\train\\DMI"

    def __init__(self, application, engine, index, current_button, translation_data):
        """Fonction d'initialisation de la page de paramtètres 1 (page paramètres général)

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        engine: `QQmlApplicationEngine`
            La QQmlApplicationEngine de la page à charger
        index: `int`
            index de la page (1 pour le bouton d'en haut -> 8 pour le bouton d'en bas
        current_button: `QObject`
            Le bouton auquel sera relié la page (généralement d'id : page_rb + index)
        translation_data: `td.TranslationDictionary`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive
            Utile pour traduire les noms de dossiers et de fenêtres sauvegardés en anglais
        """
        # Stocke les informations nécessaires au fonctionnement de la page
        self.index = index
        self.current_button = current_button
        self.current_button.setProperty("text", self.name)
        self.page = engine.rootObjects()[0]
        self.engine = engine

        try:
            # Essaye de charger la combo langue
            file = open(application.translation_file_path, "r", encoding='utf-8-sig')
        except (FileNotFoundError, OSError):
            # Ne change charge pas  la combo langues dans le cas ou le combo n'est pas chargé
            log.warning(f"Le fichier de traduction de langue de l'initialisation n'existe pas." +
                        f"assurez vous qu'il existe.\n\t{application.translation_file_path}")
        # Sinon lit la première ligne pour récupérer la liste des langues
        else:
            # Récupère la liste des langues (ligne 1 du fichier initialisation.lang)
            language_combo = self.page.findChild(QObject, "language_combo")
            language_list = file.readline().rstrip('\n').split(";")

            # S'assure que le français est bien dedans, sinon c'est qu'il y a un soucis
            if application.language.lower() in [lang.lower() for lang in language_list]:
                # Met la liste des langues dans la combo et connecte une fonction pour changer la langue
                log.info(f"{len(language_list)} langues trouvées ({language_list}) dans le fichier. \n\t" +
                         application.translation_file_path)
                language_combo.setProperty("elements", language_list)
                language_combo.change_selection(application.language)
                language_combo.selection_changed.connect(lambda: self.on_language_changed(application))
            else:
                # Sinon désactive la combobox et laisse un message de warning
                language_combo.setProperty("is_activable", False)
                log.warning(f"La langue : {application.language} n'est' pas dans la liste de langue : {language_list}" +
                            f"du fichier :\n\t{application.translation_file_path}")

        # Charge tous les dossiers dans src.train.command_board, les traduits et les indiques comme potentiels pupitres
        command_boards = [translation_data[f.replace("_", " ")] for f in os.listdir(self.command_board_folder_path)
                          if os.path.isdir(os.path.join(self.command_board_folder_path, f))
                          and f != "__pycache__" and f != "Generic"]
        self.page.findChild(QObject, "command_board_combo").setProperty("elements", command_boards)
        log.info(f"{len(command_boards)} pupitres trouvés ({command_boards}) dans :\n\t{self.command_board_folder_path}")

        # Charge tous les DMI présents dans src.train.DMI, les traduits et les indiques comme DMI sélectionables
        dmi_list = [translation_data[f.replace("_", " ")] for f in os.listdir(self.dmi_folder_path)
                    if os.path.isdir(os.path.join(self.dmi_folder_path, f))]
        self.page.findChild(QObject, "dmi_combo").setProperty("elements", dmi_list)
        log.info(f"{len(dmi_list)} IHM trouvés ({dmi_list}) dans :\n\t{self.dmi_folder_path}")

        # Initialise la liste des niveaux de registre et l'envoie au log_switchbutton
        self.page.findChild(QObject, "log_switchbutton").setProperty("elements", list(self.log_converter))

    def get_values(self, translation_data):
        """Récupère les paramètres de la page de paramètres page_rb1

        Parameters
        ----------
        translation_data: `td.TranslationDictionary`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) 

        Returns
        -------
        parameters : `sd.SettingsDictionary`
            un dictionaire de paramètres de la page de paramètres page_rb1
        """
        page_parameters = sd.SettingsDictionary()

        # Paramètre du pupitre
        command_board = self.page.findChild(QObject, "command_board_combo").property("selection_text")
        page_parameters["command_board"] = translation_data[command_board].replace(" ", "_")

        # Paramètre si connecté à Renard
        page_parameters["renard"] = self.page.findChild(QObject, "renard_check").property("is_checked")

        # Paramètre si caméra connecté pour Renard (ou alors visu direct sur renard)
        page_parameters["camera"] = self.page.findChild(QObject, "camera_check").property("is_checked")

        # Paramètre choix du DMI
        dmi_selection = self.page.findChild(QObject, "dmi_combo").property("selection_text")
        page_parameters["dmi"] = translation_data[dmi_selection].replace(" ", "_")

        # Paramètre niveau de logging
        log_text = self.page.findChild(QObject, "log_switchbutton").property("selection_text")
        page_parameters["log_level"] = self.log_converter[log_text]

        # Paramètre langue
        page_parameters["language"] = self.page.findChild(QObject, "language_combo").property("selection_text")

        # Paramètre si PCC connecté
        page_parameters["ccs"] = self.page.findChild(QObject, "ccs_check").property("is_checked")

        # Paramètres si affichage des données en direct (vitesse, ...)
        page_parameters["live_data"] = self.page.findChild(QObject, "data_check").property("is_checked")
        page_parameters["dashboard"] = self.page.findChild(QObject, "dashboard_check").property("is_checked")
        page_parameters["save_data"] = self.page.findChild(QObject, "data_save_check").property("is_checked")

        return page_parameters

    def set_values(self, data, translation_data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        data: `sd.SettingsDictionary`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        translation_data: `td.TranslationDictionary`
            Un dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue)
        """
        # Paramètre du pupitre (quel pupitre sera utilisé)
        if data.get_value("command_board") is not None:
            command_board = translation_data[str(data["command_board"]).replace("_", " ")]
            self.page.findChild(QObject, "command_board_combo").change_selection(command_board)

        # Paramètre pour Renard (savoir si le pupitre est connecté à Renard)
        data.update_parameter(self.page, "renard_check", "is_checked", "renard")

        # Paramètre pour la caméra (savoir si elle est connecté ou si on a un visu direct sur Renard)
        data.update_parameter(self.page, "camera_check", "is_checked", "camera")

        # Paramètre pour le DMI (savoir quelle Interface sera utilisée pour le pupitre
        if data.get_value("dmi") is not None:
            dmi = translation_data[str(data["dmi"]).replace("_", " ")]
            self.page.findChild(QObject, "command_board_combo").change_selection(dmi)

        # Paramètre niveau de registre (pour suivre les potentiels bugs lors de la simulation)
        if data.get_value("log_level") is not None:
            new_log_level = [key for key, value in self.log_converter.items()
                             if value == log.Level[data["log_level"][6:]]]
            if new_log_level:
                self.page.findChild(QObject, "log_switchbutton").change_selection(new_log_level[0])
            else:
                log.debug(f"Le niveau de registre du fichier de paramètre \"{data['log_level']}\" n'existe pas.\n")

        # Paramètre pour le PCC (savoir s'il sera activé)
        data.update_parameter(self.page, "ccs_check", "is_checked", "ccs")

        # Paramètres pour l'affichage des données en direct (genre vitesse, ...)
        data.update_parameter(self.page, "data_check", "is_checked", "live_data")
        data.update_parameter(self.page, "dashboard_check", "is_checked", "dashboard")
        data.update_parameter(self.page, "data_save_check", "is_checked", "save_data")

    def change_language(self, translation_data):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de la page de paramètres

        Parameters
        ----------
        translation_data: `td.TranslationDictionary`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitiv
        """
        # Traduit le nom de la catégorie
        self.current_button.setProperty("text", translation_data[self.current_button.property("text")])

        # Traduit le titre de tous les widgets qui en ont un
        for widget_id in ["data_check", "dashboard_check", "data_save_check", "ccs_check", "log_switchbutton",
                          "language_combo", "dmi_combo", "renard_check", "camera_check", "command_board_combo"]:
            widget = self.page.findChild(QObject, widget_id)
            widget.setProperty("title", translation_data[widget.property("title")])

        # Traduit les clés du log_converter (Les valeurs sur le composant sont traduites juste en dessous)

        keys = list(self.log_converter)
        self.log_converter = {translation_data[keys[0]]: self.log_converter[keys[0]],
                              translation_data[keys[1]]: self.log_converter[keys[1]],
                              translation_data[keys[2]]: self.log_converter[keys[2]],
                              translation_data[keys[3]]: self.log_converter[keys[3]]
                              }

        # Pour les combobox et switchbutton traduit chaque élément qui contient une traduction et remet la sélection
        for widget_id in ["log_switchbutton", "command_board_combo", "dmi_combo"]:
            widget = self.page.findChild(QObject, widget_id)
            selection_index = widget.property("selection_index")
            widget.setProperty("elements", [translation_data[e] for e in widget.property("elements").toVariant()])
            widget.change_selection(selection_index)

    @decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
    def on_language_changed(self, application):
        """Fonction permettant de changer la langue de l'application d'initialisation.
        Permet aussi de choisir la langue pour le DMI du pupitre
        Parameters
        ----------
        application: `ini.InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        # Appelle la fonction de changement de langue de l'application avec la nouvelle langue sélectionnée
        application.change_language(self.page.findChild(QObject, "language_combo").property("selection_text"))
