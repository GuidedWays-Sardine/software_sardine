# Librairies par défaut
import os
import sys
import traceback
import time


# Librairies graphiques
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary.settings as sd
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
            log.warning(f"""Problème lors du chargement du signal du bouton sauvegarder ou ouvrir.
                        \t\tErreur de type : {type(error)}
                        \t\tAvec comme message d'erreur : {error.args}\n\n\t\t""" +
                        "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

        log.info(f"Boutons inférieurs chargés en " +
                 f"{((time.time() - initial_time)*1000):.2f} millisecondes.\n\n")

    def on_quit_clicked(self, application):
        """Ferme la fenêtre d'initialisation

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        log.info(f"Fermeture de la page de paramètres page_rb{application.active_settings_page}.\n\n")
        application.app.quit()

    def on_launch_clicked(self, application):
        """Ferme la fenêtre d'initialisation et indique au programme de récupérer les données entrées

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        try:
            # Vérifie si toutes les pages sont complètes et stocke les pages qui ne sont pas complétées
            non_completed_pages = list(i for i in range(0, 8)
                                       if application.is_completed_by_default[i] != application.is_fully_loaded[i]
                                       and not application.visible_pages[i].is_page_valid())
        except Exception as error:
            # Si une erreur a été détectée dans une des fonction de validation, l'indique et ne complète pas l'initialisation
            log.warning(f"""Erreur lors de la validation d'une des pages de paramètres.
                        \t\tErreur de type : {type(error)}
                        \t\tAvec comme message d'erreur : {error.args}\n\n\t\t""" +
                        "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
        else:
            # Dans le cas où toutes les pages ont été vérifiées avec succès
            if not non_completed_pages:
                # Dans le cas où aucune page est incomplète (et donc que toutes les pages sont complètes)
                if "on_page_closed" in dir(application.visible_pages[application.active_settings_page - 1]):
                    try:
                        # Appelle la fonction de fermeture de page (si celle-ci existe)
                        application.visible_pages[application.active_settings_page - 1].on_page_closed(application)
                    except Exception as error:
                        # Si la fonction de fermeture de page contient une erreur, l'indique
                        log.error(f"""La fonction on_page_closed de la page_rb{application.active_settings_page} contient une erreur
                                  \t\tErreur de type : {type(error)}
                                  \t\tAvec comme message d'erreur : {error.args}\n\n\t\t""" +
                                  "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

                # Indique que le simulateur va être lancée et ferme l'application (les données seront alors récupérées
                log.change_log_prefix("Récupération des données")
                application.launch_simulator = True
                application.app.quit()
            else:
                # Si toutes les pages ne sont pas complétées, indique en niveau debug les pages qui ne le sont pas
                log.debug(f"Pages de paramètres : {' ; '.join([str(n + 1) for n in non_completed_pages])} non complétés.\n")

                # Et change la page de paramètres active sur la première page non complète
                application.right_buttons.on_new_page_selected(application,
                                                               application.visible_pages[non_completed_pages[0]].engine,
                                                               non_completed_pages[0] + 1)

    def on_open_clicked(self, application):
        """Fonction appelée lorsque le bouton ouvrir est cliqué.
        Permet l'ouverture d'un fichier texte et la récupération de ses paramètres.

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        # Ouvre la fenêtre d'ouverture de fichier pour sélectionner le fichier à ouvrir
        file_path = QFileDialog.getOpenFileName(caption="Ouvrir un fichier de configuration",
                                                directory=f"{PROJECT_DIR}settings\\general_settings",
                                                filter="Fichiers de configuration Sardine (*.settings)")

        # Si un fichier a bien été sélectionné
        if file_path[0] != "":
            # Change le préfixe du registre pour indiquer que les données de l'applications d'initialisation sont changées
            log.change_log_prefix("Changement des données")

            #Récupère les données dans le fichier sélectionné et les envoies à set_values
            data = sd.SettingsDictionnary()
            data.open(file_path[0])
            application.set_values(data)

            # Remet le préfixe de registre de la page active
            log.change_log_prefix(f"page_rb{application.active_settings_page}")

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
                                                directory=f"{PROJECT_DIR}settings\\general_settings",
                                                filter="Fichiers de configuration Sardine (*.settings)")

        # Si un fichier a bien été sélectionné
        if file_path[0] != "":
            # Change le préfixe du registre pour indiquer que les données de l'applications d'initialisation sont sauvegardées
            log.change_log_prefix("Sauvegarde des données")

            # Récupère les paramètres de l'application d'initialisation, les stockes et les enregistres dans le fichier
            data = sd.SettingsDictionnary()
            data.update(application.get_values())
            data.save(file_path[0])

            # Remet le préfixe de registre de la page active
            log.change_log_prefix(f"page_rb{application.active_settings_page}")

    def change_language(self, application, translation_data):
        """Permet à partir d'un dictionnaire de traduction de traduire le textes des 4 boutons inférieurs.

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        translation_data: `TranslationDictionary`
            dictionaire contenant les traductions
        """
        # Pour chaque boutons : récupère le texte, prend sa traduction dans translation_data et change son texte
        for button_id in ["quit", "launch", "open", "save"]:
            # Récupère le bouton associé à l'id et change son texte
            button = application.win.findChild(QObject, button_id)
            button.setProperty("text", translation_data[button.property("text")])
