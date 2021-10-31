# Librairies par défaut
import os
import sys
import traceback
import time


# Librairies graphiques
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


class BottomButtons:
    """Classe s'occupant du chargement et du fonctionnement des boutons inférieurs de l'application d'initialisation"""

    def __init__(self, application):
        """Permet d'initialiser les boutons permanents (quitter, ouvrir, sauvegarder, lancer) en bas de la fenêtre.
        Connecte chaque bouton à sa fonctionalité (nécessaires au bon fonctionnement de l'application d'initialisation)

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        initial_time = time.time()
        log.info("Tentative de chargement des boutons inférieurs.\n")

        # Boutons quitter/lancer (obligatoires pour le lancement de l'application)
        application.win.findChild(QObject, "quit").clicked.connect(lambda: self.on_quit_clicked(application))
        application.win.findChild(QObject, "launch").clicked.connect(lambda: self.on_launch_clicked(application))

        # Boutons sauvegarder/ouvrir (non obligatoire pour le lancement de l'application)
        try:
            application.win.findChild(QObject, "open").clicked.connect(lambda: self.on_open_clicked(application))
            application.win.findChild(QObject, "save").clicked.connect(lambda: self.on_save_clicked(application))
        except Exception as error:
            log.warning("Problème lors du chargement du signal du bouton sauvegarder ou ouvrir.\n\t" +
                        "Erreur de type : " + str(type(error)) + "\n\t\t" +
                        "Avec comme message d\'erreur : " + str(error.args) + "\n\n\t\t" +
                        "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

        log.info("Boutons inférieurs chargés en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

    def on_quit_clicked(self, application):
        """Ferme la fenêtre d'initialisation

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        log.info("Fermeture de la page de paramètres page_rb" + str(application.active_settings_page) + ".\n\n")
        application.app.quit()

    def on_launch_clicked(self, application):
        """Ferme la fenêtre d'initialisation et indique au programme de récupérer les données entrées

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        # Vérifie que toutes les pages accessibles sont complètes
        is_completed = application.is_completed_by_default == application.is_fully_loaded

        # Dans le cas où toutes les pages ne sont pas complétés par défaut
        if not is_completed:
            # Vérifie chaque page nécessitant une vérification de validité
            is_completed = True
            # Les pages sont vérifiés en décomptant pour qu'en cas de plusieurs pages non complétées, charger la première
            for index in range(8, 0, -1):
                # Si la page a été chargée entièrement mais qu'elle n'est pas valide par défaut
                if application.is_completed_by_default[index - 1] is not application.is_fully_loaded[index - 1]:
                    # Si la page a une fonction is_page_valid, permettant de vérifier sa validité
                    if "is_page_valid" in dir(application.visible_pages[index - 1]):
                        try:
                            if not application.visible_pages[index - 1].is_page_valid(application):
                                is_completed = False
                                application.right_buttons.on_new_page_selected(application,
                                                                               application.visible_pages[index - 1].engine,
                                                                               index)
                        except Exception as error:
                            # Si une erreur a été détectée, l'enregistre, et définit l'application comme non complétée
                            log.warning("Erreur lors de la validation de la page de paramètres : " + str(index) +
                                        "\n\t\tErreur de type : " + str(type(error)) + "\n\t\t" +
                                        "Avec comme message d\'erreur : " + str(error.args) + "\n\n\t\t" +
                                        "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
                            is_completed = False
                            application.right_buttons.on_new_page_selected(application,
                                                                           application.visible_pages[index - 1].engine,
                                                                           index)
                    else:
                        # Sinon laisse la page comme complétée (pour pouvoir lancer la simulation)
                        # laisse une erreur et charge la page
                        log.error("page de paramètres page_rb" + str(index) + " notée comme non valide par défaut" +
                                  " mais sans aucune fonction is_page_valid().")
                        application.right_buttons.on_new_page_selected(application,
                                                                       application.visible_pages[index - 1].engine,
                                                                       index)

        # Vérifie que toutes les pages accessibles sont complètes
        if is_completed:
            # Si au moins une page a été correctement chargée
            if application.active_settings_page != -1:
                # Appelle la fonction de fermeture de page de la page actuelle active et change le préfix du registre
                if application.is_fully_loaded[application.active_settings_page - 1] and \
                        "on_page_closed" in dir(application.visible_pages[application.active_settings_page - 1]):
                    # Si c'est le cas, appelle la fonction de fermeture de la page
                    try:
                        application.visible_pages[application.active_settings_page - 1].on_page_closed(application)
                    except Exception as error:
                        log.error("La fonction on_page_closed de la page " + str(application.active_settings_page) +
                                  " contient une erreur\n\t\t" +
                                  "Erreur de type : " + str(type(error)) + "\n\t\t" +
                                  "Avec comme message d\'erreur : " + str(error.args) + "\n\n\t\t" +
                                  "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
                else:
                    log.debug("Aucune fonction on_page_closed page " + str(application.active_settings_page) + "\n")

                # Indique que la page a été fermée et change le préfix
                log.info("Fermeture de la page de paramètres page_rb" + str(application.active_settings_page) + ".\n\n")
                log.change_log_prefix("Récupération des données")

            # Indique que le simulateur va être lancée et ferme l'application
            application.launch_simulator = True
            application.app.quit()

    def on_open_clicked(self, application, default_file=""):
        """Fonction appelée lorsque le bouton ouvrir est cliqué.
        Permet l'ouverture d'un fichier texte et la récupération de ses paramètres.

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        default_file: `string`
            fichier à ouvrir, s'il est vide, la fenêtre d'ouverture de fichier apparaitra
        """
        # Ouvre la fenêtre d'ouverture de fichier si default_file est vide, sinon utilise default_file comme chemin
        if default_file == "":
            file_path = QFileDialog.getOpenFileName(caption="Ouvrir un fichier de configuration",
                                                    directory=PROJECT_DIR + "settings\\general_settings",
                                                    filter="Fichiers de configuration Sardine (*.settings)")
        else:
            file_path = [default_file]

        # Si un fichier a bien été sélectionné
        if file_path[0] != "":      # OPTIMIZE bouger dans la classe de settingsdictionnary
            # Change le préfixe du registre pour indiquer que les données de l'applications d'initialisation sont changées
            log.change_log_prefix("Changement des données")

            # Récupère les donnés du fichier text et mets à jour les différentes pages de paramètres
            try:
                data = {}

                # Essaye d'ouvrir le fichier envoyer, et jette une erreur si le fichier n'exsite pas
                file = open(file_path[0], "r", encoding='utf-8-sig')

                # Lit chaque ligne du fichier
                for line in file:
                    # Si la ligne ne contient pas le délimiteur (ici ;) l'indique dans les logs
                    if ";" not in line:
                        log.debug("Ligne sautée. Délimiteur : \";\" manquant dans la ligne : " + line + '\n')
                    else:
                        line = line.rstrip('\n').split(";")
                        data[line[0]] = line[1]

                # Ferme le fichier et retourne le dictionnaire avec les valeurs récupérées
                file.close()
            except FileNotFoundError:
                log.error("Le fichier ouvert n'existe plus. Aucun paramètre ne sera modifié.\n")
            except OSError:
                log.error("Le fichier n'a pas pu être ouvert. Assurez vous qu'il ne soit pas déjà ouvert.\n")
            else:
                # Si le dictionnaire de donnés n'a aucune valeur, un message d'erreur est levé sur le fichier
                if len(data) != 0:
                    application.set_values(data)
                else:
                    log.warning(file_path[0] + " n'a aucune donné ou n'est pas dans un format compatible.\n")

            # Remet le préfixe de registre de la page active
            log.change_log_prefix("page_rb" + str(application.active_settings_page) + "")

    def on_save_clicked(self, application):
        """Fonction appelée lorsque le bouton sauvegarder est cliqué.
        Permet la sauvegarde d'un fichier avec les settings.

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        # Ouvre la fenêtre de sauvegarde et enregegistre le fichier si un nom a été donné
        file_path = QFileDialog.getSaveFileName(caption="Sauvegarder un fichier de configuration",
                                                directory=PROJECT_DIR + "settings\\general_settings",
                                                filter="Fichiers de configuration Sardine (*.settings)")
        if file_path[0] != "":  # OPTIMIZE passer dans la classe settings dict
            # Change le préfixe du registre pour indiquer que les données de l'applications d'initialisation sont sauvegardées
            log.change_log_prefix("Sauvegarde des données")

            # Récupère les donnés des différentes pages de paramètres et les écrit dans le fichier
            data = application.get_values()
            try:
                # Essaye d'ouvrir le fichier envoyer, et jette une erreur si le fichier n'exsite pas
                file = open(file_path[0], "w", encoding="utf-8-sig")

                # Récupère chaque clé/valeur du dictionnaire
                for key in data.keys():
                    # Ecrit une ligne contenant la clé et la valeur séparé par le délimiteur (ici ;)
                    file.write(str(key) + ";" + str(data[key]) + "\n")

                # Ferme le fichier
                file.close()

            # Exception soulevée dans le cas où le fichier ne peut pas être créé ou modifié
            except OSError:
                log.error("Vous n'avez pas les droit d'enregistrer un fichier dans cet emplacement.\n")
            else:
                # Dans le cas où aucune donnée n'a été récupérée, le signale dans les logs
                if len(data) == 0:
                    log.warning("Aucune valeur récupérée, le fichier créé sera vide.\n")

            # Remet le préfixe de registre de la page active
            log.change_log_prefix("page_rb" + str(application.active_settings_page))

    def change_language(self, application, translation_data):
        """Permet à partir d'un dictionnaire de traduction de traduire le textes des 4 boutons inférieurs.

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        translation_data: `dict`
            dictionaire contenant en clé les mots de la langue actuelle et en valeurs, leurs traductions
        """
        # Liste les id de chaque boutons pour simplifier la structure
        buttons_id = ["quit", "launch", "open", "save"]

        # Pour chaque boutons : récupère le texte, prend sa traduction dans translation_data et change son texte
        for id in buttons_id:
            # Récupère le bouton et vérifie s'il a bien été récupéré
            widget = application.win.findChild(QObject, id)
            # Récupère le bouton et vérifie s'il a bien été récupéré et essaye de traduire son texte
            try:
                application.win.findChild(QObject, id).setProperty("text", translation_data[widget.property("text")])
            # Si la clé n'existe pas c'est que le mot n'existe pas dans le dictionnaire ou qu'il est mal traduit.
            except KeyError:
                log.debug("aucune traduction de : " + widget.property("text") + " n'existe pas.\n")
