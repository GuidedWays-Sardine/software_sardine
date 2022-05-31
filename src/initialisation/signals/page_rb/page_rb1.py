# Librairies par défaut
import os
import sys


# Librairies graphiques
from PyQt5.QtCore import QObject


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.initialisation.initialisation_window as ini
import src.misc.settings_dictionary as sd
import src.misc.translation_dictionary as td
import src.misc.log as log
import src.misc.decorators as decorators


class PageRB1:
    """Classe pour la page de paramètres 1"""

    # variables nécessaire au bon fonctionnement de la page
    index = 1  # Attention dans les tableaux l'index commence à 0
    name = "Général"
    engine = None
    page = None
    page_button = None

    # constantes de conversion entre le text du log_switchbutton et le niveau de registre associé
    log_converter = {"Complet": log.Level.DEBUG,
                     "Suffisant": log.Level.INFO,
                     "Minimal": log.Level.WARNING,
                     "Aucun": log.Level.NOTSET
                     }

    # Chemin vers les différents dossiers nécessaire au fonctionnement de la page
    command_board_folder_path = f"{PROJECT_DIR}src\\train\\command_board"
    dmi_folder_path = f"{PROJECT_DIR}src\\train\\DMI"

    def __init__(self, application, engine, index, page_button, translations):
        """Initialise la page de paramtètres 1.

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            Instance source de l'application d'initialisation ;
        engine: `QQmlApplicationEngine`
            QQmlApplicationEngine de la page à charger ;
        index: `int`
            Index de la page (1 pour le bouton haut -> 8 pour le bouton bas) ;
        page_button: `QObject`
            Bouton auquel sera relié la page (id : page_rb + index) ;
        translations : ``td.TranslationDictionary`
            Traductions (clés = anglais -> valeurs = langue actuelle) pour traduire les noms de dossiers et de modules.
        """
        # Stocke les informations nécessaires au fonctionnement de la page
        self.index = index
        self.engine = engine
        self.page = engine.rootObjects()[0]
        self.page_button = page_button
        self.page_button.setProperty("text", self.name)

        # Récupère la liste des langues dans le fichier de traduction de l'application d'initialisation
        language_list = list(td.get_language_list(application.translation_file_path))
        language_combo = self.page.findChild(QObject, "language_combo")

        # Si la langue actuelle (Français) se trouve dans la liste des langues, active le combobox langues
        if application.language.lower() in [lang.lower() for lang in language_list]:
            language_combo.setProperty("elements", language_list)
            language_combo.change_selection(application.language)
            language_combo.selection_changed.connect(lambda: self.on_language_changed(application))
        else:
            language_combo.setProperty("is_activable", False)

        # Charge tous les dossiers dans src.train.command_board, les traduits et les indiques comme potentiels pupitres
        command_boards = [translations[f.replace("_", " ")] for f in os.listdir(self.command_board_folder_path)
                          if os.path.isdir(os.path.join(self.command_board_folder_path, f))
                          and f not in ["__pycache__", "__init__.py", "Generic"]]
        self.page.findChild(QObject, "command_board_combo").setProperty("elements", command_boards)
        log.info(f"{len(command_boards)} pupitre{'s' if len(command_boards) > 1 else ''} {command_boards} " +
                 f"dans le dossier :\n\t{self.command_board_folder_path}")

        # Charge tous les DMI présents dans src.train.DMI, les traduits et les indiques comme DMI sélectionables
        dmi_list = [translations[f.replace("_", " ")] for f in os.listdir(self.dmi_folder_path)
                    if os.path.isdir(os.path.join(self.dmi_folder_path, f))]
        self.page.findChild(QObject, "dmi_combo").setProperty("elements", dmi_list)
        log.info(f"{len(dmi_list)} IHM {dmi_list} dans le dossier :\n\t{self.dmi_folder_path}")

        # Initialise la liste des niveaux de registre et l'envoie au log_switchbutton
        self.page.findChild(QObject, "log_switchbutton").setProperty("elements", list(self.log_converter))

    def get_settings(self, translations):
        """Récupère les paramètres de la page de paramètres page_rb1.

        Parameters
        ----------
        translations: `td.TranslationDictionnary`
            traductions (clés = langue actuelle -> valeurs = anglais).

        Returns
        -------
        page_settings : `sd.SettingsDictionnary`
            Dictionnaire de paramètres de la page de paramètres page_rb1.
        """
        page_settings = sd.SettingsDictionary()

        # Paramètre du pupitre
        command_board = self.page.findChild(QObject, "command_board_combo").property("selection_text")
        page_settings["command_board"] = translations[command_board].replace(" ", "_")

        # Paramètre si connecté à Renard
        page_settings["renard"] = self.page.findChild(QObject, "renard_check").property("is_checked")

        # Paramètre si caméra connecté pour Renard (ou alors visu direct sur renard)
        page_settings["camera"] = self.page.findChild(QObject, "camera_check").property("is_checked")

        # Paramètre choix du DMI
        dmi_selection = self.page.findChild(QObject, "dmi_combo").property("selection_text")
        page_settings["dmi"] = translations[dmi_selection].replace(" ", "_")

        # Paramètre niveau de logging
        log_text = self.page.findChild(QObject, "log_switchbutton").property("selection_text")
        page_settings["log_level"] = self.log_converter[log_text]

        # Paramètre langue
        page_settings["language"] = self.page.findChild(QObject, "language_combo").property("selection_text")

        # Paramètre si PCC connecté
        page_settings["ccs"] = self.page.findChild(QObject, "ccs_check").property("is_checked")

        # Paramètres si affichage des données en direct (vitesse, ...)
        page_settings["live_data"] = self.page.findChild(QObject, "data_check").property("is_checked")
        page_settings["dashboard"] = self.page.findChild(QObject, "dashboard_check").property("is_checked")
        page_settings["save_data"] = self.page.findChild(QObject, "data_save_check").property("is_checked")

        return page_settings

    def set_settings(self, settings, translations, resize_popup=False):
        """Change les paramètres de la page de paramètres page_rb1.

        Parameters
        ----------
        settings: `sd.SettingsDictionary`
            Dictionnaire contenant les nouveaux paramètres à utiliser ;
        translations: `td.TranslationDictionary`
            Traductions (clés = anglais -> valeurs = langue actuelle) ;
        resize_popup: `bool`
            Si les popups doivent être redimensionnées.
        """
        # Paramètre du pupitre (quel pupitre sera utilisé)
        if settings.get_value("command_board") is not None:
            command_board = translations[str(settings["command_board"]).replace("_", " ")]
            self.page.findChild(QObject, "command_board_combo").change_selection(command_board)

        # Paramètre pour Renard (savoir si le pupitre est connecté à Renard)
        settings.update_ui_parameter(self.page.findChild(QObject, "renard_check"), "is_checked", "renard")

        # Paramètre pour la caméra (savoir si elle est connecté ou si on a un visu direct sur Renard)
        settings.update_ui_parameter(self.page.findChild(QObject, "camera_check"), "is_checked", "camera")

        # Paramètre pour le DMI (savoir quelle Interface sera utilisée pour le pupitre
        if settings.get_value("dmi") is not None:
            dmi = translations[str(settings["dmi"]).replace("_", " ")]
            self.page.findChild(QObject, "command_board_combo").change_selection(dmi)

        # Paramètre niveau de registre (pour suivre les potentiels bugs lors de la simulation)
        if settings.get_value("log_level") is not None:
            new_log_level = [key for key, value in self.log_converter.items()
                             if value == log.Level[settings["log_level"][6:]]]
            if new_log_level:
                self.page.findChild(QObject, "log_switchbutton").change_selection(new_log_level[0])
            else:
                log.debug(f"Le niveau de registre du fichier de paramètre \"{settings['log_level']}\" n'existe pas.\n")

        # Paramètre pour le PCC (savoir s'il sera activé)
        settings.update_ui_parameter(self.page.findChild(QObject, "ccs_check"), "is_checked", "ccs")

        # Paramètres pour l'affichage des données en direct (genre vitesse, ...)
        settings.update_ui_parameter(self.page.findChild(QObject, "data_check"), "is_checked", "live_data")
        settings.update_ui_parameter(self.page.findChild(QObject, "dashboard_check"), "is_checked", "dashboard")
        settings.update_ui_parameter(self.page.findChild(QObject, "data_save_check"), "is_checked", "save_data")

    def change_language(self, translations):
        """A partir d'un dictionnaire de paramètres, change les paramètres des différentes pages.

        Parameters
        ----------
        translations: `td.TranslationDictionary`
            Traductions (clés = langue actuelle -> valeurs = nouvelle langue).
        """
        # Traduit le nom de la catégorie
        translations.translate_widget_property(widget=self.page_button, property_name="text")

        # Traduit le titre de tous les widgets qui en ont un
        for widget_id in ["data_check", "dashboard_check", "data_save_check", "ccs_check", "log_switchbutton",
                          "language_combo", "dmi_combo", "renard_check", "camera_check", "command_board_combo"]:
            translations.translate_widget_property(parent=self.page, widget_name=widget_id,
                                                   property_name="title")

        # Traduit le texte du bouton d'ouverture du popup de pupitre
        translations.translate_widget_property(parent=self.page, widget_name="command_board_popup_button",
                                               property_name="text")

        # Traduit les clés du log_converter (Les valeurs sur le composant sont traduites juste en dessous)
        keys = list(self.log_converter)
        self.log_converter = {translations[keys[0]]: self.log_converter[keys[0]],
                              translations[keys[1]]: self.log_converter[keys[1]],
                              translations[keys[2]]: self.log_converter[keys[2]],
                              translations[keys[3]]: self.log_converter[keys[3]]
                              }

        # Pour les combobox et switchbutton traduit chaque élément qui contient une traduction et remet la sélection
        for widget_id in ["log_switchbutton", "command_board_combo", "dmi_combo"]:
            translations.translate_widget_property(parent=self.page, widget_name=widget_id,
                                                   property_name="elements")

    @decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
    def on_language_changed(self, application):
        """Change la langue du simulateur selon la sélection de l'utilisateur.
        Appelé lorsque la sélection du combobox change.

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            Instance source de l'application d'initialisation, pour les widgets.
        """
        # Appelle la fonction de changement de langue de l'application avec la nouvelle langue sélectionnée
        application.change_language(self.page.findChild(QObject, "language_combo").property("selection_text"))
