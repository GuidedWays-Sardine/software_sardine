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
import src.initialisation.signals.page_rb.pagerb2.complex_popup as cp
import src.initialisation.signals.page_rb.pagerb2.complex_data as cd
import src.misc.settings_dictionary.settings as sd
import src.misc.translation_dictionary.translation as td
import src.misc.log.log as log
import src.misc.decorators.decorators as decorators


class PageRB2:
    """Classe pour la page de paramètres 2"""

    # variables nécessaire au bon fonctionnement de la page
    index = 2   # Attention dans les tableaux l'index commence à 0
    name = "Train"
    engine = None
    page = None
    current_button = None
    data_widgets = {}      # Dictionaire avec tous les composants contenant des valeurs sur le train
    train_name_widget = None  # "train_name_stringinput". Permet une optimisation

    # Variables nécessaires à l'indication du mode de paramétrage actuel
    class Mode(Enum):
        SIMPLE = False
        COMPLEX = True
    current_mode = Mode.SIMPLE      # /!\ Le mode complexe est activé quand le train a été généré

    # Page de paramètres complexes (situé dans pagerb2/complex_popup.py)
    complex_popup = None

    # Page de paramètres de freinage (situé dans pagerb2/braking_popup.py)
    brake_popup = None
    # FEATURE : ajouter la classe les import et les fichiers graphiques et logiques nécessaires
    
    # Chemin vers les fichiers de paramètres train
    train_settings_folder_path = f"{PROJECT_DIR}settings\\train_settings\\"

    def __init__(self, application, engine, index, current_button, translation_data):
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

        # Commence par associer chaque widget à son widget_id (permettant une optimisation dû au surplus de composants)
        for widget_id in ["weight_floatinput", "length_floatinput", "coaches_integerinput",
                          "bogies_count_integerinput", "axles_per_bogies_integerinput", "motorized_axles_count_integerinput",
                          "motorized_axle_weight_floatinput", "axle_power_floatinput", "power_floatinput",
                          "a_floatinput", "b_floatinput", "c_floatinput", "pantograph_check", "thermic_check",
                          "pad_brake_integerinput", "magnetic_brake_integerinput", "regenerative_check",
                          "disk_brake_integerinput", "foucault_brake_integerinput", "dynamic_check"]:
            self.data_widgets[widget_id] = self.page.findChild(QObject, widget_id)
        self.train_name_widget = self.page.findChild(QObject, "train_name_stringinput")

        # Initialise la combobox avec les types de trains
        self.page.findChild(QObject, "mission_type_combo").setProperty("elements", [translation_data[key.value] for key in cd.MissionType])

        # Tente d'initialiser la fenêtre de paramétrage complexe
        try:
            self.complex_popup = cp.ComplexPopup(self)
        except Exception as error:
            log.error("Erreur lors du chargement de la popup complexe (page_rb2).",
                      exception=error, prefix="Initialisation popup paramétrage train")
        finally:
            # Vérifie que celle-ci a été chargée et si oui, active le changement de mode et le connecte à son signal
            if self.complex_popup is not None and self.complex_popup.loaded:
                mode_switchbutton = self.page.findChild(QObject, "mode_switchbutton")
                mode_switchbutton.setProperty("is_activable", True)
                mode_switchbutton.setProperty("is_positive", True)
                mode_switchbutton.clicked.connect(self.on_mode_switchbutton_clicked)

        # Tente d'initialiser la fenêtre de paramétrage freinage
        try:
            raise NotImplementedError("La fenêtre de paramétrage freinage n'a pas été implémentée")
            # FEATURE : Créer la page de paramètrages des systèmes de freinages
        except Exception as error:
            log.error("Erreur lors du chargement de la popup freinage (page_rb2).",
                      exception=error, prefix="Initialisation popup paramétrage freinage")
        finally:
            # Vérifie que celle-ci a été chargée et si oui, active le paramétrage des systèmes de freinages
            if self.brake_popup is not None and self.brake_popup.loaded:
                brake_button = self.page.findChild(QObject, "brake_button")
                brake_button.setProperty("is_activable", True)
                brake_button.setProperty("is_positive", True)
                # brake_button.clicked.connect(...) # FEATURE : remplacer ... par le signal

        # Connecte le bouton ouvrir et sauvegarder (d'un fichier de paramètres de train
        self.page.findChild(QObject, "open_button").clicked.connect(self.on_open_button_clicked)
        self.page.findChild(QObject, "save_button").clicked.connect(self.on_save_button_clicked)

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

        # Vérifie si le fichier a eu un nom donné
        file_name = self.train_name_widget.property("text")
        if file_name:
            # Rajoute l'extension si nécessaire et appelle la fonction de sauvegarde (definit plus bas)
            file_name += ".train" if file_name and not file_name.lower().endswith(".train") else ""
            self.save_train_data_file(f"{self.train_settings_folder_path}{file_name}")

            # Ajoute le nom du fichier dans le dictionnaire de paramètres
            page_parameters["train_name"] = self.train_name_widget.property('text')
        else:
            log.warning("Impossible de sauvegarder le fichier de paramètres train, aucun nom de fichier entré.\n",
                        prefix="Sauvegarde des données train")

        return page_parameters

    def save_train_data_file(self, file_path):
        """Fonction permettant de sauvegarder les données du train

        Parameters
        ----------
        file_path: `str`
            chemin d'accès vers le fichier de sauvegarde
        """
        initial_time = time.perf_counter()
        log.info(f"Tentative de sauvegarde des paramètres trains dans : {file_path}\n",
                 prefix="Sauvegarde des données train")

        train_data = sd.SettingsDictionary()
        train_data["train_name"] = self.train_name_widget.property('text')

        # Commence par ajouter le mode de paramétrage
        train_data["mode"] = str(self.current_mode)

        try:
            # Ajoute les paramètres simples et complexes si le mode a été activé
            train_data.update(self.get_simple_mode_values())
            if self.current_mode == self.Mode.COMPLEX:
                train_data.update(self.complex_popup.get_complex_mode_values())

            #FEATURE : Ajouter la récupération des valeurs de freinage ici
        except Exception as error:
            # Dans le cas où une erreur se produit, laisse un message d'erreur (et sauvegarde le fichier tout de même
            log.warning("Erreur lors de la sauvegarde des données train. Le fichier de paramètres sera incomplet.\n",
                        exception=error, prefix="Sauvegarde des données train")
        finally:
            # Sauvegarde le fichier et indique le temps nécessaire pour la récupération et la sauvegarde des données
            train_data.save(file_path)
            log.info(f"Récupération et sauvegarde de {len(train_data)} paramètres train en " +
                     f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.\n",
                     prefix="Sauvegarde des données train")

    def set_values(self, data, translation_data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        data: `sd.SettingsDictionary`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        translation_data: `td.TranslationDictionary`
            Un dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue)
        """
        # Récupère le nom du fichier train (et regard si le paramètre existe)
        file_name = data.get_value("train_name")
        if file_name is not None:
            # Vérifie que le fichier de paramètres existe
            file_name += ".train" if file_name and not file_name.lower().endswith(".train") else ""
            if os.path.exists(f"{self.train_settings_folder_path}{file_name}"):
                # Si c'est le cas, l'ouvre et change les différentes valeurs du paramétrage train sur la page
                self.open_train_data_file(f"{self.train_settings_folder_path}{file_name}")
            else:
                # Sinon laisse un message d'erreur
                log.warning(f"le fichier de paramètres : {file_name} , n'existe plus.\n" +
                            f"\t\t{self.train_settings_folder_path}{file_name}",
                            prefix="Ouverture des données train")

    def open_train_data_file(self, file_path):
        """Fonction permettant d'ouvrir et de lire un fichier de paramètre train et de mettre à jour l'initialisation

        Parameters
        ----------
        file_path: `str`
            Cemin d'accès vers le fichier à ouvrir (doit exister)
        """
        initial_time = time.perf_counter()
        train_data = sd.SettingsDictionary()

        # Ouvre le fichier de paramètres envoyé et récupère les différents paramètres
        train_data.open(file_path)

        # Si aucun paramètres n'a été récupéré (fichier inexistant ou vide) retourne)
        if not train_data:
            return

        try:
            # Change les valeurs en mode simple
            self.set_simple_mode_values(train_data)

            # Change le mode actuel et vérifie s'il est en mode complexe et si le popup est chargé
            self.current_mode = self.Mode[train_data["mode"][5:]]
            if self.current_mode == self.Mode.COMPLEX and self.complex_popup is not None and self.complex_popup.loaded:
                # Si c'est le cas, passe en mode complexe (graphiquement et logiquement), et change les valeurs complexe
                self.page.findChild(QObject, "mode_switchbutton").change_selection(1)  # 1 représentant le mode complexe
                self.page.setProperty("generated", True)
                self.complex_popup.win.setProperty("generated", True)
                self.complex_popup.win.show()
                self.complex_popup.set_complex_mode_values(train_data)
            else:
                # Sinon repasse en mode paramétrage simple et réinitialise la popup complexe si nécessaire
                self.page.findChild(QObject, "mode_switchbutton").change_selection(0)
                self.page.setProperty("generated", False)
                if self.complex_popup is not None and self.complex_popup.loaded:
                    self.complex_popup.win.setProperty("generated", False)
                    self.complex_popup.reset()
        except Exception as error:
            # Si le changement des paramètre a eu un soucis, laisse un message d'erreur
            log.warning("Erreur survenu lors du changement des données train.\n",
                        exception=error, prefix="Ouverture des données train")
        else:
            # Change le nom du fichier train dans le train_name_stringinput et indique le temps de chargement
            file_name = file_path.replace("\\", "/").rsplit("/", maxsplit=1)[1][:-6]
            self.train_name_widget.change_value(file_name)

        # S'occupe pour finir du changement des paramètres de freinage
        try:
            raise NotImplementedError("La fenêtre de paramétrage freinage n'a pas été implémentée")
            # FEATURE : changer les valeurs de la fenêtre de paramétrage
        except Exception as error:
            # Si le changement des paramètre a eu un soucis, laisse un message d'erreur
            log.warning("Erreur survenu lors du changement des paramètres de freinage.\n",
                        exception=error, prefix="Ouverture des données train")

        log.info(f"Lecture et changement {len(train_data)} paramètres en " +
                 f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.\n",
                 prefix="Ouverture des données train")

    def change_language(self, translation_data):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de la page de paramètres

        Parameters
        ----------
        translation_data: `td.TranslationDictionary`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitiv
        """
        # Traduit le nom de la catégorie
        self.current_button.setProperty("text", translation_data[self.current_button.property("text")])

        # Traduit le placeholder texte ainsi que le titre pour le stringinput du nom du train
        self.train_name_widget.setProperty("placeholder_text",
                                           translation_data[self.train_name_widget.property("placeholder_text")])
        self.train_name_widget.setProperty("title",
                                           translation_data[self.train_name_widget.property("title")])

        # Traduit le nom de chacune des catégories de paramètres
        for category in ["general_data_text", "dynamic_data_text", "alimentation_data_text", "brake_data_text"]:
            self.page.setProperty(category, translation_data[self.page.property(category)])

        # Essaye de traduire chaque textes au dessus des widgets et check_button
        for widget_id, widget in self.data_widgets.items():
            widget.setProperty("title", translation_data[widget.property("title")])

        # Traduit toutes les clés pour le switchbutton du mode ainsi que pour le combobox
        for widget_id in ["mode_switchbutton", "mission_type_combo"]:
            widget = self.page.findChild(QObject, widget_id)
            selection_index = widget.property("selection_index")
            widget.setProperty("elements", [translation_data[e] for e in widget.property("elements").toVariant()])
            widget.change_selection(selection_index)
            
            # Fait un cas particulier pour le switchbutton qui a aussi un titre à traduire
            if widget_id == "mode_switchbutton":
                widget.setProperty("title", translation_data[widget.property("title")])

        # Traduit le texte des trois boutons (ouvrir, fermer, paramétrage freinage)
        for widget_id in ["open_button", "save_button", "brake_button"]:
            widget = self.page.findChild(QObject, widget_id)
            widget.setProperty("text", translation_data[widget.property("text")])

        # Traduit la fenêtre de paramétrage complexe
        if self.complex_popup is not None and self.complex_popup.loaded:
            self.complex_popup.change_language(translation_data)

        # Traduit la fenêtre de paramétrage de freinage
        if self.brake_popup is not None and self.brake_popup.loaded:
            pass
            # FEATURE : faire la fonction de changement de langue de la fenêtre de paramétrage du freinage

    def on_page_opened(self, application):
        """Fonction appelée lorsque la page de paramètres 8 est chargée.
        Permet d'afficher les fenêtre d'index et actualise les paramètres des écrans visibles

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Dans le cas où la popop de paramètre complexe a été chargée et mode complexe a été activé, montre la fenêtre
        if self.complex_popup is not None and self.complex_popup.loaded \
                and self.page.findChild(QObject, "mode_switchbutton").property("selection_index") == 1:
            self.complex_popup.win.show()

    def on_page_closed(self, application):
        """Fonction appelée quand la page de paramètres 8 est fermée.
        Permet de cacher les différentes fenêtres d'index

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Cache la popup de paramétrage complexe
        if self.complex_popup is not None and self.complex_popup.loaded:
            self.complex_popup.win.hide()

        if self.brake_popup is not None and self.brake_popup.loaded:
            self.brake_popup.win.hide()

    def is_page_valid(self):
        """Méthode permettant d'indiquer si la pagede paramètre est complétés

        Returns
        -------
        is_page_valid: `bool`
            Est ce que la page de paramètre est complétée ?
        """
        # Retourne vrai si le nom du fichier a été complété (autre variables complétés par défaut)
        if not self.train_name_widget.property("text"):
            self.train_name_widget.blink(None, None, None)
            return False

        return True

    def get_simple_mode_values(self):
        """Fonction permettant de récupérer toutes les informations de la configuration simple

        Returns
        ----------
        train_data: `sd.SettingsDictionary`
            Dictionaire de paramètre avec tous les paramètres simples du train
        """
        train_data = sd.SettingsDictionary()

        # Rajoute le type de mission
        train_data["mission"] = cd.mission_getter[self.page.findChild(QObject, "mission_type_combo").property("selection_index")]

        # Change les données de la fenêtre principale du paramétrage train
        for widget_id, widget in self.data_widgets.items():
            # Cas des valueinput (floatinput, integerinput), change la propriétée "value"
            if "_integerinput" in widget_id or "_floatinput" in widget_id:
                train_data[widget_id.rsplit("_", maxsplit=1)[0]] = widget.property("value")
            # Cas des checkbuttons
            elif "_check" in widget_id:
                train_data[widget_id.rsplit("_", maxsplit=1)[0]] = widget.property("is_checked")

        return train_data

    def set_simple_mode_values(self, train_data):
        """Fonction permettant de mettre à jour les données trains en mode simple

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Propriétés du train
        """
        # Change le type de mission (en récupérant l'index de l'élément sauvegardé et en le changeant sur le combobox
        mission_index = cd.MissionType[train_data.get_value("mission", str(cd.MissionType.PASSENGER))[12:]].value
        self.page.findChild(QObject, "mission_type_combo").change_selection(mission_index)

        # Change les données de la fenêtre principale du paramétrage train
        for widget_id, widget in self.data_widgets.items():
            # Cas des valueinput (floatinput, integerinput), change la propriétée "value"
            if "_integerinput" in widget_id or "_floatinput" in widget_id:
                widget.change_value(train_data.get_value(widget_id.rsplit("_", maxsplit=1)[0], widget.property("value")))
            # Cas des checkbuttons
            elif "_check" in widget_id:
                widget.setProperty("is_checked", train_data.get_value(widget_id.rsplit("_", maxsplit=1)[0], False))

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def on_save_button_clicked(self):
        """Signal activé lorsque le bouton sauvegardé (de la page de paramètres train) est activé.
        Demande à l'utilisateur de confirmer le nom du fichier, puis le sauvegarde
        """
        # Commence par créer le chemin vers le fichier
        file_name = self.train_name_widget.property("text")
        file_name += ".train" if file_name and not file_name.lower().endswith(".train") else ""

        # Ouvre la boite de dialoque pour confirmer l'enregistrement du fichier
        file_path = QFileDialog.getSaveFileName(caption="Sauvegarder un fichier de configuration train",
                                                directory=f"{self.train_settings_folder_path}{file_name}",
                                                filter="Fichiers de configuration train (*.train)")
        if file_path[0] != "":
            # Dans le cas où le nom du fichier a été changé à la sauvegarder, récupère le nouveau nom de fichier
            file_name = file_path[0].rsplit("/", maxsplit=1)[1][:-6]
            self.train_name_widget.change_value(file_name)

            # Sauvegarde le fichier de paramètres train
            self.save_train_data_file(file_path[0])

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def on_open_button_clicked(self):
        """Signal activé lorsque le bouton ouvrir (de la page de paramètres train) est activé.
        Demande à l'utilisateur de sélectionner un fichier de paramètres du train, puis l'ouvre et change les paramètres
        """
        # Ouvre la boite de dialoque pour l'ouverture du fichier
        file_path = QFileDialog.getOpenFileName(caption="Sauvegarder un fichier de configuration train",
                                                directory=self.train_settings_folder_path,
                                                filter="Fichiers de configuration train (*.train)")
        if file_path[0] != "":
            # Dans le cas où le nom du fichier a été changé à la sauvegarder, récupère le nouveau nom de fichier
            file_name = file_path[0].rsplit("/", maxsplit=1)[1][:-6]
            self.train_name_widget.change_value(file_name)

            # Sauvegarde le fichier de paramètres train
            self.open_train_data_file(file_path[0])

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def on_mode_switchbutton_clicked(self):
        """signal appelé lorsque le bouton du choix du mode de paramétrage est cliqué.
        S'occupe ou non d'afficher et de cacher la fenêtre de popup"""

        # Distingue deux cas : quand le mode est passé en mode complexe et en mode simple
        if self.page.findChild(QObject, "mode_switchbutton").property("selection_index") == 1:    # Mode complexe activé
            # Si la fenêtre de paramètres complex existe, la montrer (une page permettant de générer
            if self.complex_popup is not None and self.complex_popup.loaded:
                self.complex_popup.win.show()
        else:       # Mode simple activé
            # Si la popup complex existe, la cache et dégénère les paramètres complexe et réinitialise les données
            self.current_mode = self.Mode.SIMPLE
            if self.complex_popup is not None and self.complex_popup.loaded:
                self.complex_popup.win.hide()
                self.complex_popup.win.setProperty("generated", False)
                self.page.setProperty("generated", False)
                self.complex_popup.reset()

        # FEATURE : faire la fonction connectée au bouton "Freinage" pour ouvrir la fenêtre de paramétrage freinage