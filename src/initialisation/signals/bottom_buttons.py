# Librairies par défaut
import os
import sys
import time
import re


# Librairies graphiques
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog, QApplication


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary as sd
import src.misc.log as log
import src.misc.decorators as decorators
import src.misc.virtual_keyboard as vk
import src.initialisation.initialisation_window as ini


class BottomButtons:
    """Classe s'occupant du chargement et du fonctionnement des boutons inférieurs de l'application d'initialisation"""

    def __init__(self, application):
        """Initialise les boutons permanents (quitter, ouvrir, sauvegarder, lancer) en bas de la fenêtre ainsi que les
        différents éléments d'ouverture et de sauvegarde fichiers.

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            Instance source de l'application d'initialisation, (pour intérargir avec l'application).
        """
        initial_time = time.perf_counter()
        log.info("Chargement des boutons inférieurs (Quitter, Ouvrir, Sauvegarder, Lancer).")

        # Boutons quitter/lancer (obligatoires pour le lancement de l'application)
        application.win.findChild(QObject, "quit_button").clicked.connect(lambda: self.on_quit_clicked(application))
        application.win.findChild(QObject, "launch_button").clicked.connect(lambda: self.on_launch_clicked(application))

        # Boutons sauvegarder/ouvrir (présent uniquement si au moins une page est chargée correctement)
        if any([page is not None and not isinstance(page, QObject) for page in application.pages_list]):
            application.win.findChild(QObject, "open_button").clicked.connect(lambda: self.on_open_clicked(application))
            application.win.findChild(QObject, "save_button").clicked.connect(lambda: self.on_save_clicked(application))
            application.win.findChild(QObject, "confirm_button").clicked.connect(lambda: self.on_save_popup_confirm_clicked(application))

            # Connecte le clavier virtuel à l'entrée de valeur du popup save (si aucun clavier physique)
            application.win.findChild(QObject, "file_name_stringinput").focus_gained.connect(
                lambda: vk.show_keyboard(window=application.win,
                                         widget=application.win.findChild(QObject, "save_popup"),
                                         language=application.language,
                                         skip_list=["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]))
            application.win.findChild(QObject, "file_name_stringinput").focus_lost.connect(vk.hide_keyboard)

            log.info("Au moins une page de paramètres correctement chargée. Boutons ouvrir et sauvegarder activés.")
        else:
            # Sinon, cache les boutons
            application.win.findChild(QObject, "open_button").setProperty("visible", False)
            application.win.findChild(QObject, "save_button").setProperty("visible", False)
            log.info("Aucune page de paramètres correctement chargée. Boutons ouvrir et sauvegarder cachés.")

        # Connecte le checkbutton pour le clavier virtuel à la fonction correspondante
        application.win.findChild(QObject, "virtual_keyboard_check").value_changed.connect(lambda: self.on_virtual_keyboard_checked(application))
        self.on_virtual_keyboard_checked(application)

        log.info(f"Boutons inférieurs chargés en " +
                 f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.\n")

    @decorators.QtSignal(log_level=log.Level.CRITICAL, end_process=True)
    def on_quit_clicked(self, application):
        """Ferme la fenêtre d'initialisation.
        Appelé lorsque le bouton fermer est cliqué.

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            Instance source de l'application d'initialisation, pour les widgets.
        """
        # ferme la page puis l'application
        if "on_page_closed" in dir(application.pages_list[application.active_page_index - 1]):
            application.pages_list[application.active_page_index - 1].on_page_closed(application)
        log.info(f"Fermeture de la page de paramètres page_rb{application.active_page_index}.\n")
        log.change_log_prefix("")
        QApplication.instance().quit()

    @decorators.QtSignal(log_level=log.Level.CRITICAL, end_process=True)
    def on_launch_clicked(self, application):
        """Ferme la fenêtre d'initialisation et indique au programme de récupérer les données entrées.
        Appelé lorsque le bouton de lancer est cliqué.

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            Instance source de l'application d'initialisation, pour les widgets.
        """
        # Récupère la liste des pages complétées ou non. Une page est compléte si :
        # - la page n'a pas de partie logique (elle sera donc de type QObject ou None)
        # - la page a une partie logique mais pas de fonctions "is_page_valid"
        # - la page a une partie logique et la fonbction is_page_valid retourne true
        page_complete = [(page is None or isinstance(page, QObject)) or
                         ("is_page_valid" not in dir(page)) or
                         (page.is_page_valid())
                         for page in application.pages_list]

        # Vérifie que toutes les pages sont complétées
        if all(page_complete):
            # Si c'est le cas, ferme correctement la page actuelle, récupère les paramètres et lance la simulation
            if "on_page_closed" in dir(application.pages_list[application.active_page_index - 1]):
                application.pages_list[application.active_page_index - 1].on_page_closed(application)
            log.info(f"Fermeture de la page de paramètres page_rb{application.active_page_index}.\n")

            application.launch_simulator = True
            QApplication.instance().quit()
        else:
            # Sinon récupère les pages non complètes, laisse un message de registre et se met sur la page non complétée
            non_completed_pages = tuple(index + 1 for index, completed in enumerate(page_complete) if not completed)
            if len(non_completed_pages) == 1:
                log.debug(f"La page de paramètre page_rb{non_completed_pages[0]} est incomplète.")
            else:
                log.debug(f"Les pages de paramètres {[f'page_rb{i}' for i in non_completed_pages]} sont incomplètes.")
            application.right_buttons.on_new_page_selected(application,
                                                           application.pages_list[non_completed_pages[0] - 1].engine,
                                                           non_completed_pages[0])

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def on_open_clicked(self, application):
        """Ouvre le dialogue d'ouverture de fichier.
        Appelé lorsque le bouton ouvrir est cliqué.

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            Instance source de l'application d'initialisation, pour les widgets.
        """
        # Ouvre la fenêtre d'ouverture de fichier pour sélectionner le fichier à ouvrir
        file_path = QFileDialog.getOpenFileName(caption="Ouvrir un fichier de configuration",
                                                directory=application.general_settings_folder_path,
                                                filter="Fichiers de configuration Sardine (*.settings)")

        # Si un fichier a bien été sélectionné
        if file_path[0] != "":
            # Récupère les données dans le fichier sélectionné et les envoies à set_settings
            file_path = re.split(r"[/\\]+", file_path)[-1].split(".")[0]
            settings = sd.SettingsDictionary()
            log.add_empty_lines()
            if settings.open(file_path[0]):
                log.info(f"Chargement des paramètres \"{file_path}\" et mise à jour de l'application.",
                         prefix="Mise à jour paramètres généraux")
                application.set_settings(settings)

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def on_save_clicked(self, application):
        """Ouvre le dialogue de sauvegarde de fichier, ou le popup de sauvegare dans le cas du clavier virtuel.
        Appelée lorsque le bouton sauvegarder est cliqué.

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            Instance source de l'application d'initialisation, pour les widgets.
        """
        # Si le clavier virtuel est activé
        if application.win.findChild(QObject, "virtual_keyboard_check").property("is_checked"):
            # Récupère et vide le stringinput du popup
            application.win.findChild(QObject, "file_name_stringinput").clear()

            # Affiche le popup pour entrer le nom du fichier et le sauvegarder
            save_popup = application.win.findChild(QObject, "save_popup")
            save_popup.open()
        # Sinon, affiche la fenêtre de sauvegarde du fichier
        else:
            # Récupère le nom du fichier à travers le sauvegardeur de windows
            file_path = QFileDialog.getSaveFileName(caption="Sauvegarder un fichier de configuration",
                                                    directory=application.general_settings_folder_path,
                                                    filter="Fichiers de configuration Sardine (*.settings)")

            # Si un fichier a bien été sélectionné
            if file_path[0] != "":
                # Récupère les paramètres de l'application d'initialisation, les enregistres dans le fichier
                settings = sd.SettingsDictionary()
                settings.update(application.get_settings())
                settings.save(file_path[0])

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def on_save_popup_confirm_clicked(self, application):
        """Récupère le nom de fichier entrer dans le popup.
        Appelé lorsque le bouton confirmer du popup de sauvegarder fichier avec clavier virtuel est cliqué.

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            Instance source de l'application d'initialisation, pour les widgets.
        """
        # Ferme le popup
        application.win.findChild(QObject, "save_popup").close()

        # Récupère le nom du fichier et vide l'entrée
        file_popup_name = application.win.findChild(QObject, "file_name_stringinput")
        file_name = file_popup_name.property("value")
        file_popup_name.clear()

        # Si le nom de fichier ne finit pas avec la bonne extension, l'ajoute
        file_name += ".settings" if not file_name.endswith(".settings") else ""

        # Récupère le nom du fichier à travers le sauvegardeur de windows
        file_path = QFileDialog.getSaveFileName(caption="Sauvegarder un fichier de configuration",
                                                directory=f"{PROJECT_DIR}settings\\general_settings\\{file_name}",
                                                filter="Fichiers de configuration Sardine (*.settings)")

        # Si un fichier a bien été sélectionné
        if file_path[0] != "":
            # Récupère les paramètres de l'application d'initialisation, les enregistres dans le fichier
            settings = sd.SettingsDictionary()
            settings.update(application.get_settings())
            settings.save(file_path[0])

    @decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
    def on_virtual_keyboard_checked(self, application):
        """Change la possibilité d'afficher le clavier ou non selon la demande de l'utilisateur.

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            Instance source de l'application d'initialisation, pour les widgets.
        """
        # Appelle la fonction pour changer l'activabilité du clavier virtuel, selon la valeur du checkbutton
        virtual_keyboard_active = application.win.findChild(QObject, "virtual_keyboard_check").property("is_checked")
        vk.change_keyboard_activability(activable=virtual_keyboard_active)

    def change_language(self, application, translations):
        """Traduit le texte des différents boutons et popups à partir d'un dictionnaire de traductions.

        Parameters
        ----------
        application: `InitialisationWindow`
            Instance source de l'application d'initialisation, pour les widgets ;
        translations: `TranslationDictionary`
            Dictionnaire contenant les traductions.
        """
        # Pour chaque boutons : traduit le texte
        for button_id in ["quit_button", "launch_button", "open_button", "save_button", "confirm_button"]:
            translations.translate_widget_property(parent=application.win,
                                                   widget_name=button_id,
                                                   property_name="text")

        # Traduit le checkbutton du clavier virtuel
        translations.translate_widget_property(parent=application.win,
                                               widget_name="virtual_keyboard_check",
                                               property_name="title")

        # Traduit le placeholder_text
        translations.translate_widget_property(parent=application.win,
                                               widget_name="file_name_stringinput",
                                               property_name="placeholder_text")
