import logging
import os
import traceback

from PyQt5.QtCore import QObject


class PageRB1:

    index = 1   # Attention dans les tableaux l'index comment à 0 donc index_tab = index - 1
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

        # Rend le checkbutton renard et le checkbutton caméra fonctionnel
        renard = self.page.findChild(QObject, "renard_checkbutton")
        renard.clicked.connect(self.on_renard_selected)
        self.page.findChild(QObject, "camera_checkbutton").setProperty("isActivable", renard.property("isChecked"))

        # Rend le bouton registre fonctionel (quand cliqué, indique le registre suivant)
        log_button = self.page.findChild(QObject, "log_button")
        log_button.clicked.connect(lambda l=log_button: l.setProperty("text", self.next_log_level[l.property("text")]))

        # Définit la page comme validée (toutes les valeurs par défaut suffisent)
        application.is_completed[0] = True

    def get_values(self, translation_data):
        """Récupère les paramètres de la page de paramètres page_rb1

        Returns
        -------
        parameters : `dictionary`
            un dictionaire de paramètres de la page de paramètres page_rb1
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) /!\\ clés en majuscules"""
        page_parameters = {}

        # Paramètre du pupitre
        command_board = self.page.findChild(QObject, "command_board_combo").property("selection")
        try:
            command_board = translation_data[command_board.upper()].replace(" ", "_")
        except KeyError:
            logging.debug("Traduction pour le pupitre non trouvée.\n")
            command_board = command_board.replace(" ", "_")
        page_parameters["Pupitre"] = command_board

        # Paramètre si connecté à Renard
        page_parameters["Renard"] = self.page.findChild(QObject, "renard_checkbutton").property("isChecked")

        # Paramètre si caméra connecté pour Renard (ou alors visu direct sur renard)
        page_parameters["Caméra"] = self.page.findChild(QObject, "camera_checkbutton").property("isChecked")

        # Paramètre choix du DMI
        dmi_selection = self.page.findChild(QObject, "dmi_combo").property("selection")
        try:
            dmi_selection = translation_data[dmi_selection.upper()].replace(" ", "_")
        except KeyError:
            logging.debug("traduction pour le dmi non trouvée.\n")
            dmi_selection = dmi_selection.replace(" ", "_")
        page_parameters["DMI"] = dmi_selection

        # Paramètre niveau de logging
        log_text = self.page.findChild(QObject, "log_button").property("text")
        page_parameters["Registre"] = self.log_type_converter[log_text]

        # Paramètre langue
        page_parameters["Langue"] = self.page.findChild(QObject, "language_combo").property("selection")

        # Paramètre si PCC connecté
        page_parameters["PCC"] = self.page.findChild(QObject, "pcc_checkbutton").property("isChecked")

        # Paramètre si affichage des données en direct (vitesse, ...)
        page_parameters["DonnéesDirect"] = self.page.findChild(QObject, "data_checkbutton").property("isChecked")

        return page_parameters

    def set_values(self, data, translation_data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        data: `dict`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) /!\\ clés en majuscules"""
        # Changement de la langue dans la combobox (la langue a été changée dans set_values de InitialisationWindow)
        try:
            # Si la langue indiquée est incorrect, change_selection ne changera rien, aucune précautions à prendre
            self.page.findChild(QObject, "language_combo").change_selection(data["Langue"])
        # Si aucun paramètre Langue, cela sera indiqué lors de la traduction. Aucune manoeuvre supplémentaire nécessaire
        except KeyError:
            pass

        # Paramètre du pupitre (quel pupitre sera utilisé)
        try:
            command_board = data["Pupitre"].replace("_", " ").upper()
        except KeyError:
            logging.debug("Impossible de changer le paramètre: \"Pupitre\" manquant dans le fichier ouvert.\n")
        else:
            try:
                self.page.findChild(QObject, "command_board_combo").change_selection(translation_data[command_board])
            except KeyError:
                logging.debug("Impossible de changer la donnée : \"Pupitre\" car sa traduction est manquante.\n")

        # Paramètre pour Renard (savoir si le pupitre est connecté à Renard)
        try:
            self.page.findChild(QObject, "renard_checkbutton").setProperty("isChecked", data["Renard"] == "True")
        except KeyError:
            logging.debug("Impossible de changer le paramètre : \"Renard\" manquant dans le fichier ouvert.\n")

        # Paramètre pour le PCC (savoir s'il sera activé)
        try:
            self.page.findChild(QObject, "pcc_checkbutton").setProperty("isChecked", data["PCC"] == "True")
        except KeyError:
            logging.debug("Impossible de changer le paramètre : \"PCC\" manquant dans le fichier ouvert.\n")

        # Paramètre pour le DMI (savoir quel Interface sera utilisée pour le pupitre
        try:
            dmi = data["DMI"].replace("_", " ").upper()
        except KeyError:
            logging.debug("Impossible de changer le paramètre: \"Pupitre\" manquant dans le fichier ouvert.\n")
        else:
            try:
                self.page.findChild(QObject, "dmi_combo").change_selection(translation_data[dmi])
            except KeyError:
                logging.debug("Impossible de changer la donnée : \"DMI\" car sa traduction est manquante.\n")

        # Paramètre niveau de registre (pour suivre les potentiels bugs lors de la simulation)
        try:
            self.page.findChild(QObject, "log_button").setProperty("text", self.log_type_converter[int(data["Registre"])])
        except KeyError:
            logging.debug("Impossible de changer le paramètre : \"Registre\" manquant dans le fichier ouvert.\n")

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

    def on_renard_selected(self):
        """Fonction appelée lorsque le checkbutton renard_checkbutton est sélectioné.
        Permet d'activer ou de désactiver le checkbutton pour la caméra"""
        # Récupère si le checkbutton de renard est activé ainsi que le checkbutton caméra
        connected = self.page.findChild(QObject, "renard_checkbutton").property("isChecked")
        camera_checkbutton = self.page.findChild(QObject, "camera_checkbutton")

        # Cas où renard est activé -> le bouton est sélectionable
        if connected:
            camera_checkbutton.setProperty("isActivable", True)
        # Cas où renard est désactivé -> le bouton n'est pas sélectionable et est désactivé
        else:
            camera_checkbutton.setProperty("isActivable", False)
            camera_checkbutton.setProperty("isChecked", False)
