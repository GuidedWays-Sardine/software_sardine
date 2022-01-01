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

        # Commence par associer chaque widget à son widget_id (permettant une optimisation surtout en mode complex) :
        for widget_id in ["weight_floatinput", "length_floatinput", "coaches_integerinput",
                          "bogies_count_integerinput", "axles_per_bogies_integerinput", "motorized_axles_count_integerinput",
                          "motorized_axle_weight_floatinput", "axle_power_floatinput", "power_floatinput",
                          "a_floatinput", "b_floatinput", "c_floatinput",
                          "pad_brake_integerinput", "magnetic_brake_integerinput",
                          "disk_brake_integerinput", "fouccault_brake_integerinput"]:
            self.valueinput[widget_id] = self.page.findChild(QObject, widget_id)

        # Initialise la combobox avec les types de trains
        # TODO : importer complex data et utiliser les valeurs dans mission_type

        # Initialise la popup de paramétrage complex
        self.complex_popup = complex.ComplexPopup(self)

        # Si la fenêtre a été chargée
        if self.complex_popup.loaded:
            # Rend le bouton mode_button activable et le connecte à son signal
            mode_button = self.page.findChild(QObject, "mode_button")
            mode_button.setProperty("is_activable", True)
            mode_button.clicked.connect(self.on_mode_button_clicked)
        else:
            # Rend le bouton mode_button non activabl
            self.page.findChild(QObject, "mode_button").setProperty("is_activable", False)

        # Connecte le bouton ouvrir et sauvegarder (d'un fichier de paramètres de train
        self.page.findChild(QObject, "open_button").clicked.connect(self.on_open_button_clicked)
        self.page.findChild(QObject, "save_button").clicked.connect(self.on_save_button_clicked)

        # Connecte le bouton de configuration de freinage
        #TODO : le connecter et créer la popup de freinage

        # Définit la page comme validée (toutes les valeurs par défaut suffisent)
        application.is_completed_by_default[self.index - 1] = "is_page_valid" not in dir(self)

    def get_values(self, translation_data):
        """Récupère les paramètres de la page de paramètres page_rb1

        Parameters
        ----------
        translation_data: `td.TranslationDictionary`
            dictionaire de traduction (clés = langue actuelle -> valeurs = anglais)

        Returns
        -------
        parameters : `sd.SettingsDictionary`
            un dictionaire de paramètres de la page de paramètres page_rb1
        """
        page_parameters = sd.SettingsDictionary()

        # Change le préfix de registre le temps de la sauvegarde du fichier paramètres train
        log.change_log_prefix("Sauvegarde des données train")

        # Vérifie si le fichier a eu un nom donné
        file_name = self.page.findChild(QObject, "train_name_stringinput").property("text")
        if file_name:
            # Rajoute l'extension si nécessaire et appelle la fonction de sauvegarde (definit plus bas)
            file_name += ".train" if file_name and not file_name.lower().endswith(".train") else ""
            self.save_train_data_file(f"{PROJECT_DIR}settings\\train_settings\\{file_name}")
        else:
            log.warning("Impossible de sauvegarder le fichier de paramètres train, aucun nom de fichier entré.\n")

        # Rechange le prefix pour la sauvegarde générale des données
        log.change_log_prefix("Sauvegarde des données")

        # Ajoute le nom du fichier dans le dictionnaire de paramètres
        page_parameters["train_data"] = self.page.findChild(QObject, 'train_name_text').property('text')

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
            #FIXME : voir pour la traduction de la configuration freinage (contenant \n)

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

    def is_page_valid(self):
        """Méthode permettant d'indiquer si la pagede paramètre est complétés

        Returns
        -------
        is_page_valid: `bool`
            Est ce que la page de paramètre est complétée ?
        """
        # Retourne vrai si le nom du fichier a été complété (autre variables complétés par défaut)
        return self.page.findChild(QObject, "train_name_stringinput").property("text")

    def on_save_button_clicked(self):
        """Signal activé lorsque le bouton sauvegardé (de la page de paramètres train) est activé.
        Demande à l'utilisateur de confirmer le nom du fichier, puis le sauvegarde
        """
        # Commence par créer le chemin vers le fichier
        train_name_widget = self.page.findChild(QObject, "train_name_stringinput")
        file_name = train_name_widget.property("text")
        file_name += ".train" if file_name and not file_name.lower().endswith(".train") else ""

        # Ouvre la boite de dialoque pour confirmer l'enregistrement du fichier
        file_path = QFileDialog.getSaveFileName(caption="Sauvegarder un fichier de configuration train",
                                                directory=f"{PROJECT_DIR}settings\\train_settings\\{file_name}",
                                                filter="Fichiers de configuration train (*.train)")
        if file_path[0] != "":
            print(file_path)

            # Dans le cas où le nom du fichier a été changé à la sauvegarder, récupère le nouveau nom de fichier
            file_name = file_path[0].rsplit("/", maxsplit=1)[1][:-6]
            train_name_widget.change_text(file_name)

            # Sauvegarde le fichier de paramètres train
            self.save_train_data_file(file_path[0])

    def save_train_data_file(self, file_path):
        """Fonction permettant de sauvegarder les données du train"""
        train_parameters = sd.SettingsDictionary()

        # Commence par ajouter le mode de paramétrage
        train_parameters["mode"] = str(self.current_mode)

        # Ajoute les paramètres simples (à ajouter même en mode complex)
        train_parameters.update(self.get_simple_mode_values())

        # Si le mode complexe est activé, sauvegarde aussi les données complexes
        if self.current_mode == self.Mode.COMPLEX:
            train_parameters.update(self.complex_popup.get_complex_mode_values())

        train_parameters.save(file_path)

    def get_simple_mode_values(self):
        """Fonction permettant de récupérer toutes les informations de la configuration simple

        Returns
        ----------
        train_parameters: `sd.SettingsDictionary`
            Dictionaire de paramètre avec tous les paramètres simples du train
        """
        parameters = sd.SettingsDictionary()

        initial_time = time.perf_counter()

        # Récupère chacune des données stockées dans un floatinput ou integerinput
        for widget_id in ["weight_floatinput", "length_floatinput", "coaches_integerinput",
                          "bogies_count_integerinput", "axles_per_bogies_integerinput", "motorized_axles_count_integerinput",
                          "motorized_axle_weight_floatinput", "axle_power_floatinput", "power_floatinput",
                          "a_floatinput", "b_floatinput", "c_floatinput",
                          "pad_brake_integerinput", "magnetic_brake_integerinput",
                          "disk_brake_integerinput", "fouccault_brake_integerinput"]:
            parameters[widget_id.rsplit("_", maxsplit=1)[0]] = self.valueinput[widget_id].property("value")

        # Récupère chacune des données stockées dans un checkbutton
        for widget_id in ["regenerative_check", "dynamic_check", "pantograph_check", "thermic_check"]:
            parameters[widget_id.replace("_check", "")] = self.page.findChild(QObject, widget_id).property("is_checked")

        print((time.perf_counter() - initial_time) * 1000)

        return parameters

    def on_mode_button_clicked(self):
        """signal appelé lorsque le bouton du choix du mode de paramétrage est cliqué.
        S'occupe ou non d'afficher et de cacher la fenêtre de popup"""
        mode_button = self.page.findChild(QObject, "mode_button")

        # Inverse le mode du bouton
        mode_button.setProperty("text", self.mode_switch[mode_button.property("text")])

        # Distingue deux cas : quand le mode est passé en mode complexe et en mode simple
        if mode_button.property("text") == list(self.mode_switch.keys())[1]:    # Mode complexe activé
            # Si la fenêtre de paramètres complex existe, la montrer (une page permettant de générer
            if self.complex_popup.loaded:
                self.complex_popup.win.show()
                self.complex_popup.win.setProperty("generated", (self.current_mode == self.Mode.COMPLEX))
        else:       # Mode simple activé
            # Si  la popup complex existe, la cache et dégénère les paramètres complexe
            if self.complex_popup.loaded:
                self.complex_popup.win.hide()
                self.complex_popup.win.setProperty("generated", False)
                self.page.setProperty("generated", False)

                # TODO : réinitialiser les données