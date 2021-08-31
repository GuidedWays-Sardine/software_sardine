import logging
import os
import traceback

from PyQt5.QtCore import QObject


class PageRB1:

    index = 1   # Attention dans les tableaux l'index comment à 0 donc index_tab = index - 1
    page = None
    current_button = None

    def __init__(self, application, page, index, current_button):
        """Fonction d'initialisation de la page de paramtètres 1 (page paramètres général)

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        page: `QQmlApplicationEngine`
            La QQmlApplicationEngine de la page à charger
        index: `int`
            index de la page (1 pour le bouton d'en haut -> 8 pour le bouton d'en bas
        current_button: `QObject`
            Le bouton auquel sera relié la page (généralement d'id : page_rb + index)"""
        # Change les valeurs initiales de la page
        self.index = index
        self.page = page
        self.current_button = current_button

        # Charge les langues disponibles pour le DMI
        language_list = None
        try:
            file = open("../settings/language_settings/translation.settings", "r", encoding='utf-8-sig')
        # Récupère les exceptions dans le cas où le fichier de traduction n'existe pas ou est mal placé
        except (FileNotFoundError, OSError):
            logging.warning("Impossible d'ouvrir le fichier settings/language_settings/translation.settings\n\t\t" +
                            "Assurez vous que celui-ci existe. Le Français sera choisis par défaut\n")
        # Sinon lit la première ligne pour récupérer la liste des langues
        else:
            # Récupère la liste des langues (ligne 1 du fichier translation.settings)
            language_list = file.readline().rstrip('\n').split(";")

            # Met la liste des langues dans la combobox et connecte une fonction pour changer la langue
            language_combobox = self.page.findChild(QObject, "language_combo")
            language_combobox.setProperty("elements", language_list)
            language_combobox.selection_changed.connect(lambda: self.on_language_change(application))
            self.language = language_combobox.property("selection")

        # Essaye de récupérer le dictionaire Anglais -> Français afin de traduire les répertoires par défaut en anglais
        found_translation = False
        try:
            translation_data = application.read_language_file("English", "Français")
            found_translation = True
        except Exception as error:
            # Rattrape une potentielle erreur lors de la création du dictionaire de traduction
            logging.warning("Erreur lors de la récupération du dictionaire de traduction dans l'initialisation. " +
                            "Certains éléments de la page seront par défaut en anglais." +
                            "\n\t\tErreur de type : " + str(type(error)) +
                            "\n\t\tAvec comme message d'erreur : " + error.args[0] + "\n\n\t\t" +
                            "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

        # Charge les pupitres, les traduits en Français et les remets dans la combobox
        command_boards = [f.replace("_", " ") for f in os.listdir("command_board")
                          if os.path.isdir(os.path.join('command_board', f))]
        if found_translation:
            for index in range(len(command_boards)):
                try:
                    command_boards[index] = translation_data[command_boards[index].upper()]
                except KeyError:
                    logging.debug("pas de traduction française pour : " + command_boards[index] + "\n")
        self.page.findChild(QObject, "command_board_combo").setProperty("elements", command_boards)

        # Charge les DMI, les traduits en Français et les remets dans la combobox (similairement aux pupitres)
        dmi_list = [f.replace("_", " ") for f in os.listdir("DMI") if os.path.isdir(os.path.join('DMI', f))]
        if found_translation:
            for index in range(len(dmi_list)):
                try:
                    dmi_list[index] = translation_data[dmi_list[index].upper()]
                except KeyError:
                    logging.debug("pas de traduction française pour : " + dmi_list[index] + "\n")
        self.page.findChild(QObject, "dmi_combo").setProperty("elements", dmi_list)

        # Définit la page comme validée (toutes les valeurs par défaut suffisent)
        application.is_completed[0] = True

    def on_language_change(self, application):
        """Fonction permettant de changer la langue de l'application d'initialisation.
        Permet aussi de choisir la langue pour le DMI du pupitre

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets"""
        # Récupère le dictionaire de traduction et change la langue de l'application d'initialisation et du DMI
        new_language = self.page.findChild(QObject, "language_combo").property("selection")
        if application.language.upper() != new_language.upper():
            try:
                translation_data = application.read_language_file(application.language, new_language)
            except Exception as error:
                # Rattrape une potentielle erreur lors de la création du dictionaire de traduction
                logging.warning("Erreur lors de la récupération du dictionaire de traduction"
                                "\n\t\tErreur de type : " + str(type(error)) +
                                "\n\t\tAvec comme message d'erreur : " + error.args[0] + "\n\n\t\t" +
                                "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
            else:
                application.change_language(translation_data)

        # Définit la nouvelle langue comme celle sélectionée
        application.language = new_language
