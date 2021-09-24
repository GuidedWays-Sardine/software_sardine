import logging
import os
import traceback

from PyQt5.QtCore import QObject


class PageRB1:
    """Classe pour la page de paramètres 1"""

    # variables nécessaire au bon fonctionnement de la page
    index = 1   # Attention dans les tableaux l'index commence à 0
    name = "Général"
    page = None
    current_button = None

    # constantes nécessaires au fonctionnement
    next_log_level = {"Complet": "Suffisant",
                      "Suffisant": "Minimal",
                      "Minimal": "Aucun",
                      "Aucun": "Complet"
                      }

    log_type_converter = {"Aucun": logging.NOTSET,
                          "Minimal": logging.ERROR,
                          "Suffisant": logging.INFO,
                          "Complet": logging.DEBUG
                          }
    log_type_converter.update(dict([reversed(i) for i in log_type_converter.items()]))
    # Permet de faire un dictionaire bi-directionel

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
            Le bouton auquel sera relié la page (généralement d'id : page_rb + index)
        """
        # Stocke les informations nécessaires au fonctionnement de la page
        self.index = index
        self.page = page
        self.current_button = current_button
        self.current_button.setProperty("text", self.name)

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
            self.language = language_combobox.property("selection_text")

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
                    command_boards[index] = translation_data[command_boards[index]]
                except KeyError:
                    logging.debug("pas de traduction française pour : " + command_boards[index] + "\n")
        self.page.findChild(QObject, "command_board_combo").setProperty("elements", command_boards)

        # Charge les DMI, les traduits en Français et les remets dans la combobox (similairement aux pupitres)
        dmi_list = [f.replace("_", " ") for f in os.listdir("DMI") if os.path.isdir(os.path.join('DMI', f))]
        if found_translation:
            for index in range(len(dmi_list)):
                try:
                    dmi_list[index] = translation_data[dmi_list[index]]
                except KeyError:
                    logging.debug("pas de traduction française pour : " + dmi_list[index] + "\n")
        self.page.findChild(QObject, "dmi_combo").setProperty("elements", dmi_list)

        # Rend le checkbutton renard et le checkbutton caméra fonctionnel
        renard = self.page.findChild(QObject, "renard_check")
        renard.clicked.connect(self.on_renard_selected)
        self.page.findChild(QObject, "camera_check").setProperty("is_activable", renard.property("is_checked"))

        # Rend le bouton registre fonctionel (quand cliqué, indique le registre suivant)
        self.page.findChild(QObject, "log_button").clicked.connect(self.on_log_button_clicked)
        # Définit la page comme validée (toutes les valeurs par défaut suffisent)
        application.is_completed[0] = True

    def get_values(self, translation_data):
        """Récupère les paramètres de la page de paramètres page_rb1

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive

        Returns
        -------
        parameters : `dictionary`
            un dictionaire de paramètres de la page de paramètres page_rb1
        """
        page_parameters = {}

        # Paramètre du pupitre
        command_board = self.page.findChild(QObject, "command_board_combo").property("selection_text")
        try:
            command_board = translation_data[command_board].replace(" ", "_")
        except KeyError:
            logging.debug("Traduction pour le pupitre non trouvée.\n")
            command_board = command_board.replace(" ", "_")
        page_parameters["Pupitre"] = command_board

        # Paramètre si connecté à Renard
        page_parameters["Renard"] = self.page.findChild(QObject, "renard_check").property("is_checked")

        # Paramètre si caméra connecté pour Renard (ou alors visu direct sur renard)
        page_parameters["Caméra"] = self.page.findChild(QObject, "camera_check").property("is_checked")

        # Paramètre choix du DMI
        dmi_selection = self.page.findChild(QObject, "dmi_combo").property("selection_text")
        try:
            dmi_selection = translation_data[dmi_selection].replace(" ", "_")
        except KeyError:
            logging.debug("traduction pour le dmi non trouvée.\n")
            dmi_selection = dmi_selection.replace(" ", "_")
        page_parameters["DMI"] = dmi_selection

        # Paramètre niveau de logging
        log_text = self.page.findChild(QObject, "log_button").property("text")
        page_parameters["Registre"] = self.log_type_converter[log_text]

        # Paramètre langue
        page_parameters["Langue"] = self.page.findChild(QObject, "language_combo").property("selection_text")

        # Paramètre si PCC connecté
        page_parameters["PCC"] = self.page.findChild(QObject, "pcc_check").property("is_checked")

        # Paramètre si affichage des données en direct (vitesse, ...)
        page_parameters["DonnéesDirect"] = self.page.findChild(QObject, "data_check").property("is_checked")

        return page_parameters

    def set_values(self, data, translation_data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        data: `dict`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive
        """
        # Paramètre du pupitre (quel pupitre sera utilisé)
        try:
            command_board = data["Pupitre"].replace("_", " ")
        except KeyError:
            logging.debug("Impossible de changer le paramètre: \"Pupitre\" manquant dans le fichier ouvert.\n")
        else:
            try:
                self.page.findChild(QObject, "command_board_combo").change_selection(translation_data[command_board])
            except KeyError:
                logging.debug("La traduction du paramètre: \"Pupitre\" : " + data["Pupitre"] + " est manquate.\n\t\t" +
                              "Il est possible que le pupitre ne soit pas changé pour celui du fichier ouvert.\n")
                self.page.findChild(QObject, "command_board_combo").change_selection(command_board)

        # Paramètre pour Renard (savoir si le pupitre est connecté à Renard)
        try:
            self.page.findChild(QObject, "renard_check").setProperty("is_checked", data["Renard"] == "True")
        except KeyError:
            logging.debug("Impossible de changer le paramètre : \"Renard\" manquant dans le fichier ouvert.\n")

        # Paramètre pour la caméra (savoir si elle est connecté ou si on a un visu direct sur Renard)
        try:
            self.page.findChild(QObject, "camera_check").setProperty("is_checked", data["Caméra"] == "True")
        except KeyError:
            logging.debug("Impossible de changer le paramètre : \"Caméra\" manquant dans le fichier ouvert.\n")
        self.on_renard_selected()

        # Paramètre pour le DMI (savoir quelle Interface sera utilisée pour le pupitre
        try:
            dmi = data["DMI"].replace("_", " ")
        except KeyError:
            logging.debug("Impossible de changer le paramètre: \"Pupitre\" manquant dans le fichier ouvert.\n")
        else:
            try:
                self.page.findChild(QObject, "dmi_combo").change_selection(translation_data[dmi])
            except KeyError:
                logging.debug("La traduction du paramètre : \"DMI\" : " + data["DMI"] + " est manquante.\n\t\t" +
                              "Il est possible que le DMI ne soit pas changé pour celui du fichier ouvert.\n")
                self.page.findChild(QObject, "dmi_combo").change_selection(dmi)

        # Paramètre niveau de registre (pour suivre les potentiels bugs lors de la simulation)
        try:
            self.page.findChild(QObject, "log_button").setProperty("text", self.log_type_converter[int(data["Registre"])])
        except KeyError:
            logging.debug("Impossible de changer le paramètre : \"Registre\" manquant dans le fichier ouvert.\n")

        # Paramètre pour le PCC (savoir s'il sera activé)
        try:
            self.page.findChild(QObject, "pcc_check").setProperty("is_checked", data["PCC"] == "True")
        except KeyError:
            logging.debug("Impossible de changer le paramètre : \"PCC\" manquant dans le fichier ouvert.\n")

        # Paramètre pour l'affichage des données en direct (genre vitesse, ...)
        try:
            self.page.findChild(QObject, "data_check").setProperty("is_checked", data["DonnéesDirect"] == "True")
        except KeyError:
            logging.debug("Impossible de changer le paramètre : \"DonnéesDirect\" manquant dans le fichier ouvert.\n")

    def change_language(self, translation_data):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de la page de paramètres

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitiv
        """
        # Traduit le nom de la catégorie
        try:
            self.current_button.setProperty("text", translation_data[self.current_button.property("text")])
        except KeyError:
            logging.debug("Impossible de traduire le nom de la catégorie de la page_rb1.\n")

        # Essaye de traduire chaque textes au dessus des widgets et check_button
        for text in ["command_board_text", "dmi_text", "log_text", "language_text",
                     "renard_check", "camera_check", "pcc_check", "data_check"]:
            widget = self.page.findChild(QObject, text)
            try:
                widget.setProperty("text", translation_data[widget.property("text")])
            except KeyError:
                logging.debug("Pas de traduction pour le widget : " + text + ", traduction sautée.\n")

        # Pour les combobox du pupitre et du DMI, essaye de traduire chaque éléments, et remet l'index sélectioné
        # La combobox langue ne nécessite aucune traduction car les langes sont dans leur langue d'origine
        for combo in ["command_board_combo", "dmi_combo"]:
            widget = self.page.findChild(QObject, combo)
            selection_text = widget.property("selection_text")
            new_list = []

            # Pour chaque combobox récupère chaque éléments et essaye de les traduire
            for element in widget.property("elements").toVariant():
                try:
                    new_list.append(translation_data[element])
                # Si la traduction n'existe pas, laisse un message de debug et remet l'élément dans sa langue d'origine
                except KeyError:
                    logging.debug("Pas de traduction pour l'élément " + element + " du widget " + combo + ".\n")
                    new_list.append(element)

            # Enfin, remet la nouvelle list dans la combobox et change l'index
            widget.setProperty("elements", new_list)
            try:
                widget.change_selection(translation_data[selection_text])
            except KeyError:
                widget.change_selection(selection_text)

        # Pour le bouton registre, laissé à part car son fonctionnement est particulier
        keys = list(self.next_log_level.keys())
        if all(key in translation_data for key in keys):
            # Si toutes les clés ont un traduction, traduit le log_type_converter et next_log_level
            self.log_type_converter = {translation_data[keys[0]]: self.log_type_converter[keys[0]],
                                       translation_data[keys[1]]: self.log_type_converter[keys[1]],
                                       translation_data[keys[2]]: self.log_type_converter[keys[2]],
                                       translation_data[keys[3]]: self.log_type_converter[keys[3]]
                                       }
            self.log_type_converter.update(dict([reversed(i) for i in self.log_type_converter.items()]))

            # Modification du changeur de niveau de log
            self.next_log_level = \
                {translation_data[keys[0]]: translation_data[self.next_log_level[keys[0]]],
                 translation_data[keys[1]]: translation_data[self.next_log_level[keys[1]]],
                 translation_data[keys[2]]: translation_data[self.next_log_level[keys[2]]],
                 translation_data[keys[3]]: translation_data[self.next_log_level[keys[3]]]
                 }
        else:
            logging.warning("Au moins un des niveaux de registre n'a pas de traduction, bouton registre sauté.\n")

            # Change la langue du registre indiqué sur le bouton
            log_button = self.page.findChild(QObject, "log_button")
            log_button.setProperty("text", translation_data[log_button.property("text")])

    def on_language_change(self, application):
        """Fonction permettant de changer la langue de l'application d'initialisation.
        Permet aussi de choisir la langue pour le DMI du pupitre

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        # Récupère le dictionaire de traduction et change la langue de l'application d'initialisation et du DMI
        new_language = self.page.findChild(QObject, "language_combo").property("selection_text")
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

    def on_log_button_clicked(self):
        """Fonction appelée lorsque le bouton log_button est cliqué.
        Permet de changer le niveau de registre affiché sur le bouton (et récupéré)
        """
        log_button = self.page.findChild(QObject, "log_button")
        log_button.setProperty("text", self.next_log_level[log_button.property("text")])
