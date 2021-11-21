# Librairies par défaut
import os
import sys
import traceback


# Librairies graphiques
from PyQt5.QtCore import QObject


#Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.initialisation.initialisation_window as ini
import src.misc.settings_dictionary.settings as sd
import src.misc.translation_dictionary.translation as td
import src.misc.log.log as log

class PageRB1:
    """Classe pour la page de paramètres 1"""

    # variables nécessaire au bon fonctionnement de la page
    index = 1   # Attention dans les tableaux l'index commence à 0
    name = "Général"
    engine = None
    page = None
    current_button = None

    # constantes nécessaires au fonctionnement
    next_log_level = {"Complet": "Suffisant",
                      "Suffisant": "Minimal",
                      "Minimal": "Aucun",
                      "Aucun": "Complet"
                      }

    log_type_converter = {"Aucun": log.Level.NOTSET,
                          "Minimal": log.Level.WARNING,
                          "Suffisant": log.Level.INFO,
                          "Complet": log.Level.DEBUG
                          }

    def __init__(self, application, engine, index, current_button):
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
        """
        # Stocke les informations nécessaires au fonctionnement de la page
        self.index = index
        self.current_button = current_button
        self.current_button.setProperty("text", self.name)
        self.page = engine.rootObjects()[0]
        self.engine = engine

        try:
            # Essaye de charger la combobox langue
            file = open(PROJECT_DIR + "settings\\language_settings\\initialisation.lang", "r", encoding='utf-8-sig')
        except (FileNotFoundError, OSError):
            # Ne change charge pas  la combobox langues dans le cas ou le combobox n'est pas chargé
            log.warning("Le fichier de traduction de langue n'existe pas. assurez vous qu'il existe :\n\t\t" +
                        PROJECT_DIR + "settings\\language_settings\\initialisation.lang\n")
        # Sinon lit la première ligne pour récupérer la liste des langues
        else:
            # Récupère la liste des langues (ligne 1 du fichier initialisation.lang)
            language_list = file.readline().rstrip('\n').split(";")

            # Met la liste des langues dans la combobox et connecte une fonction pour changer la langue
            language_combobox = self.page.findChild(QObject, "language_combo")
            language_combobox.setProperty("elements", language_list)
            language_combobox.selection_changed.connect(lambda: self.on_language_change(application))

            # Si le premier language n'est pas le Français, traduit l'application
            if language_combobox.property("selection_text").lower() != application.language.lower():
                application.change_language(language_combobox.property("selection_text"))

        # Essaye de récupérer le dictionaire Anglais -> langue principale afin de traduire les répertoires par défaut en anglais
        t_data = td.TranslationDictionnary()
        t_data.create_translation(PROJECT_DIR + "settings\\language_settings\\initialisation.lang",
                                  "English", application.language)

        # Charge tous les dossiers dans src.train.command_board et les indiques comme pupitre sélectionables
        command_boards = [t_data[f.replace("_", " ")] for f in os.listdir(PROJECT_DIR + "src\\train\\command_board")
                          if os.path.isdir(os.path.join(PROJECT_DIR + "src\\train\\command_board", f))]
        self.page.findChild(QObject, "command_board_combo").setProperty("elements", command_boards)

        # Charge tous les DMI présents dans src.train.DMI et les indiques comme DMI sélectionables
        dmi_list = [t_data[f.replace("_", " ")] for f in os.listdir(PROJECT_DIR + "src\\train\\DMI")
                    if os.path.isdir(os.path.join(PROJECT_DIR + "src\\train\\DMI", f))]
        self.page.findChild(QObject, "dmi_combo").setProperty("elements", dmi_list)

        # Rend le checkbutton renard et le checkbutton caméra fonctionnel
        renard = self.page.findChild(QObject, "renard_check")
        renard.value_changed.connect(self.on_renard_selected)
        self.on_renard_selected()

        # Rend le checkbutton data, dashboard et data_save fonctionnel
        data = self.page.findChild(QObject, "data_check")
        data.value_changed.connect(self.on_data_selected)
        self.on_data_selected()

        # Rend le bouton registre fonctionel (quand cliqué, indique le registre suivant)
        self.page.findChild(QObject, "log_button").clicked.connect(self.on_log_button_clicked)

        # Définit la page comme validée (toutes les valeurs par défaut suffisent)
        application.is_completed_by_default[self.index - 1] = "is_page_valid" not in dir(self)

    def get_values(self, translation_data):
        """Récupère les paramètres de la page de paramètres page_rb1

        Parameters
        ----------
        translation_data: `td.TranslationDictionnary`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) 

        Returns
        -------
        parameters : `sd.SettingsDictionnary`
            un dictionaire de paramètres de la page de paramètres page_rb1
        """
        page_parameters = sd.SettingsDictionnary()

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
        log_text = self.page.findChild(QObject, "log_button").property("text")
        page_parameters["log_level"] = self.log_type_converter[log_text]

        # Paramètre langue
        page_parameters["Langue"] = self.page.findChild(QObject, "language_combo").property("selection_text")

        # Paramètre si PCC connecté
        page_parameters["ccs"] = self.page.findChild(QObject, "pcc_check").property("is_checked")

        # Paramètres si affichage des données en direct (vitesse, ...)
        page_parameters["live_data"] = self.page.findChild(QObject, "data_check").property("is_checked")
        page_parameters["dashboard"] = self.page.findChild(QObject, "dashboard_check").property("is_checked")
        page_parameters["save_data"] = self.page.findChild(QObject, "data_save_check").property("is_checked")

        return page_parameters

    def set_values(self, data, translation_data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        data: `sd.SettingsDictionnary`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        translation_data: `td.TranslationDictionnary`
            Un dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue)
        """
        # Paramètre du pupitre (quel pupitre sera utilisé)
        try:
            command_board = str(data["command_board"]).replace("_", " ")
        except KeyError:
            log.debug("Impossible de changer le paramètre: \"command_board\" manquant dans le fichier ouvert.\n")
        else:
            self.page.findChild(QObject, "command_board_combo").change_selection(translation_data[command_board])

        # Paramètre pour Renard (savoir si le pupitre est connecté à Renard)
        data.update_parameter(self.page, "renard_check", "is_checked", "renard")

        # Paramètre pour la caméra (savoir si elle est connecté ou si on a un visu direct sur Renard)
        data.update_parameter(self.page, "camera_check", "is_checked", "camera")

        # Paramètre pour le DMI (savoir quelle Interface sera utilisée pour le pupitre
        try:
            dmi = str(data["dmi"]).replace("_", " ")
        except KeyError:
            log.debug("Impossible de changer le paramètre: \"dmi\" manquant dans le fichier ouvert.\n")
        else:
            self.page.findChild(QObject, "command_board_combo").change_selection(translation_data[dmi])

        # Paramètre niveau de registre (pour suivre les potentiels bugs lors de la simulation)
        try:
            self.page.findChild(QObject, "log_button").setProperty("text",
                dict([reversed(i) for i in self.log_type_converter.items()])[log.Level[data["log_level"].replace("Level.", "")]])
        except KeyError as error:
            log.debug("Impossible de changer le paramètre : \"log_level\" manquant dans le fichier ouvert.\n" +
                     "Erreur de type : " + str(type(error)) + "\n\t\t" +
                     "Avec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                     "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

        # Paramètre pour le PCC (savoir s'il sera activé)
        data.update_parameter(self.page, "pcc_check", "is_checked", "ccs")

        # Paramètres pour l'affichage des données en direct (genre vitesse, ...)
        data.update_parameter(self.page, "data_check", "is_checked", "live_data")
        data.update_parameter(self.page, "dashboard_check", "is_checked", "dashboard")
        data.update_parameter(self.page, "data_save_check", "is_checked", "save_data")

    def change_language(self, translation_data):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de la page de paramètres

        Parameters
        ----------
        translation_data: `td.TranslationDictionnary`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitiv
        """
        # Traduit le nom de la catégorie
        self.current_button.setProperty("text", translation_data[self.current_button.property("text")])

        # Essaye de traduire chaque textes au dessus des widgets et check_button
        for widget_id in ["command_board_text", "dmi_text", "log_text", "language_text",
                          "renard_check", "camera_check", "pcc_check", "data_check", "dashboard_check", "data_save_check"]:
            widget = self.page.findChild(QObject, widget_id)
            widget.setProperty("text", translation_data[widget.property("text")])

        # Pour les combobox du pupitre et du DMI, traduit chaque élément qui contient une traduction et remet la sélection
        for combo in ["command_board_combo", "dmi_combo"]:
            widget = self.page.findChild(QObject, combo)
            selection_index = widget.property("selection_index")
            widget.setProperty("elements", list(translation_data[e] for e in widget.property("elements").toVariant()))
            widget.change_selection(selection_index)

        # Traduit les clés dans le log_type converter et dans le convertiseur de niveau de registre
        keys = list(self.next_log_level)
        self.log_type_converter = {translation_data[keys[0]]: self.log_type_converter[keys[0]],
                                   translation_data[keys[1]]: self.log_type_converter[keys[1]],
                                   translation_data[keys[2]]: self.log_type_converter[keys[2]],
                                   translation_data[keys[3]]: self.log_type_converter[keys[3]]
                                   }

        # Modification du changeur de niveau de log
        self.next_log_level = \
            {translation_data[keys[0]]: translation_data[self.next_log_level[keys[0]]],
             translation_data[keys[1]]: translation_data[self.next_log_level[keys[1]]],
             translation_data[keys[2]]: translation_data[self.next_log_level[keys[2]]],
             translation_data[keys[3]]: translation_data[self.next_log_level[keys[3]]]
             }

        # Change la langue du registre indiqué sur le bouton
        log_button = self.page.findChild(QObject, "log_button")
        log_button.setProperty("text", translation_data[log_button.property("text")])

    def on_language_change(self, application):
        """Fonction permettant de changer la langue de l'application d'initialisation.
        Permet aussi de choisir la langue pour le DMI du pupitre

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        # Appelle la fonction de changement de langue de l'application avec la nouvelle langue sélectionnée
        application.change_language(self.page.findChild(QObject, "language_combo").property("selection_text"))

    def on_renard_selected(self):
        """Fonction appelée lorsque le checkbutton renard_check est sélectioné.
        Permet d'activer ou de désactiver le checkbutton pour la caméra.
        """
        # Récupère si le checkbutton de renard est activé ainsi que le checkbutton caméra
        connected = self.page.findChild(QObject, "renard_check").property("is_checked")
        camera_check = self.page.findChild(QObject, "camera_check")

        # Cas où renard est activé -> le bouton est sélectionable
        if connected:
            camera_check.setProperty("is_activable", True)
        # Cas où renard est désactivé -> le bouton n'est pas sélectionable et est désactivé
        else:
            camera_check.setProperty("is_activable", False)
            camera_check.setProperty("is_checked", False)

    def on_data_selected(self):
        """Fonction appelée lorsque le checkbutton renard_check est sélectioné.
        Permet d'activer ou de désactiver le checkbutton pour la caméra.
        """
        # Récupère si le checkbutton de la visualisation des données est activé ainsi que le checkbutton dashboard
        connected = self.page.findChild(QObject, "data_check").property("is_checked")
        self.page.findChild(QObject, "dashboard_check").setProperty("is_activable", connected)

    def on_log_button_clicked(self):
        """Fonction appelée lorsque le bouton log_button est cliqué.
        Permet de changer le niveau de registre affiché sur le bouton (et récupéré).
        """
        log_button = self.page.findChild(QObject, "log_button")
        log_button.setProperty("text", self.next_log_level[log_button.property("text")])
