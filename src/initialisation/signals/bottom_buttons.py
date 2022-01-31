# Librairies par défaut
import os
import sys
import time


# Librairies graphiques
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary.settings as sd
import src.misc.log.log as log
import src.misc.decorators.decorators as decorators


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
        initial_time = time.perf_counter()
        log.info("Tentative de chargement des boutons inférieurs.\n")

        # Boutons quitter/lancer (obligatoires pour le lancement de l'application)
        application.win.findChild(QObject, "quit_button").clicked.connect(lambda: self.on_quit_clicked(application))
        application.win.findChild(QObject, "launch_button").clicked.connect(lambda: self.on_launch_clicked(application))

        # Boutons sauvegarder/ouvrir (non obligatoire pour le lancement de l'application)
        try:
            application.win.findChild(QObject, "open_button").clicked.connect(lambda: self.on_open_clicked(application))
            application.win.findChild(QObject, "save_button").clicked.connect(lambda: self.on_save_clicked(application))
        except Exception as error:
            log.warning(f"Problème lors du chargement du signal du bouton sauvegarder ou ouvrir.\n",
                        exception=error)

        log.info(f"Boutons inférieurs chargés en " +
                 f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.\n\n")

    @decorators.QtSignal(log_level=log.Level.CRITICAL, end_process=True)
    def on_quit_clicked(self, application):
        """Ferme la fenêtre d'initialisation

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        log.info(f"Fermeture de la page de paramètres page_rb{application.active_settings_page}.\n\n")
        application.app.quit()

    @decorators.QtSignal(log_level=log.Level.FATAL, end_process=True)
    def on_launch_clicked(self, application):
        """Ferme la fenêtre d'initialisation et indique au programme de récupérer les données entrées

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        # Récupère la liste des pages complétées ou non. Une page est compléte si :
        # - la page n'a pas de partie logique (elle sera donc de type QObject ou None)
        # - la page a une partie logique mais pas de fonctions "is_page_valid"
        # - la page a une partie logique et la fonbction is_page_valid retourne true
        page_complete = [(page is None or isinstance(page, QObject)) or
                         ("is_page_valid" not in dir(page)) or
                         (page.is_page_valid())
                         for page in application.visible_pages]

        # Vérifie que toutes les pages sont complétées
        if all(page_complete):
            # Si c'est le cas, ferme correctement la page actuelle, récupère les paramètres et lance la simulation
            if "on_page_closed" in dir(application.visible_pages[application.active_settings_page - 1]):
                application.visible_pages[application.active_settings_page - 1].on_page_closed()

            log.change_log_prefix("Récupération des données")
            application.launch_simulator = True
            application.app.quit()
        else:
            # Sinon récupère les pages non complètes, laisse un message de registre et se met sur la page non complétée
            non_completed_pages = [index for index, completed in enumerate(page_complete) if not completed]
            log.debug(f"Pages de paramètres : {' ; '.join([str(n + 1) for n in non_completed_pages])} non complétés.\n")
            application.right_buttons.on_new_page_selected(application,
                                                           application.visible_pages[non_completed_pages[0]].engine,
                                                           non_completed_pages[0] + 1)

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
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
            data = sd.SettingsDictionary()
            data.open(file_path[0])
            application.set_values(data)

            # Remet le préfixe de registre de la page active
            log.change_log_prefix(f"page_rb{application.active_settings_page}")

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
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
            data = sd.SettingsDictionary()
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
        for button_id in ["quit_button", "launch_button", "open_button", "save_button"]:
            # Récupère le bouton associé à l'id et change son texte
            button = application.win.findChild(QObject, button_id)
            button.setProperty("text", translation_data[button.property("text")])
