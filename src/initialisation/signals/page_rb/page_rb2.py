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
import src.initialisation.signals.page_rb.pagerb2.complex_popup as complex
import src.misc.settings_dictionary.settings as sd
import src.misc.translation_dictionary.translation as td
import src.misc.log.log as log


class PageRB2:
    """Classe pour la page de paramètres 2"""

    # variables nécessaire au bon fonctionnement de la page
    index = 2   # Attention dans les tableaux l'index commence à 0
    name = "Train"
    engine = None
    page = None
    current_button = None

    # Page de paramètres complexes (situé dans pagerb2/complex_popup.py)
    complex_popup = None

    # Dictionnaire contenant tous les valueinput (ceux-ci seront beaucoup utilisés. Ceci est par soucis d'optimisation
    valueinput = {}

    # Variables utiles au fonctionnement de la page:
    class Mode(Enum):
        SIMPLE = False
        COMPLEX = True
    mode_switch = {"Simple": "Complexe",
                   "Complexe": "Simple"
                   }

    # Paramètre permettant de sauvegarder si le mode complexe a été initialisé ou non
    current_mode = Mode.SIMPLE

    def __init__(self, application, engine, index, current_button):
        """Fonction d'initialisation de la page de paramtètres 2 (page paramètres train)

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
        pass

    def change_language(self, translation_data):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de la page de paramètres

        Parameters
        ----------
        translation_data: `td.TranslationDictionary`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitiv
        """
        # Traduit le nom de la catégorie
        self.current_button.setProperty("text", translation_data[self.current_button.property("text")])

        # Traduit le placeholder texte pour le stringinput du nom du train
        widget = self.page.findChild(QObject, "train_name_stringinput")
        widget.setProperty("placeholder_text", translation_data[widget.property("placeholder_text")])

        # Essaye de traduire chaque textes au dessus des widgets et check_button
        for widget_id in ["train_name_text",  "general_data_name", "weight_text", "length_text", "coaches_text",
                          "bogies_count_text", "axles_per_bogies_text", "motorized_axles_count_text", "axle_power_text",
                          "motorized_axle_weight_text", "power_text", "dynamic_data_name", "alimentation_data_name",
                          "pantograph_check", "thermic_check", "brake_data_name", "pad_brake_text",
                          "magnetic_brake_text", "regenerative_check", "disk_brake_text", "fouccault_brake_text",
                          "dynamic_check", "mode_text", "open_button", "save_button", "brake_configuration"]:
            widget = self.page.findChild(QObject, widget_id)
            widget.setProperty("text", translation_data[widget.property("text")])

        # Traduction pour les modes de paramétrages (simple et complex) (mode_switch et texte du bouton)
        keys = list(self.mode_switch)
        self.mode_switch = {translation_data[keys[0]]: translation_data[self.mode_switch[keys[0]]],
                            translation_data[keys[1]]: translation_data[self.mode_switch[keys[1]]]
                            }
        mode_button = self.page.findChild(QObject, "mode_button")
        mode_button.setProperty("text", translation_data[mode_button.property("text")])

        # Traduction de la combobox des différents types de trains
        widget = self.page.findChild(QObject, "mission_type_combo")
        selection_index = widget.property("selection_index")
        widget.setProperty("elements", list(translation_data[e] for e in widget.property("elements").toVariant()))
        widget.change_selection(selection_index)
