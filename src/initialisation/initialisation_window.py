# Librairies par défaut
import os
import sys
import time


# Librairies graphiques
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.immersion as immersion
import src.misc.settings_dictionary as sd
import src.misc.translation_dictionary as td
import src.misc.window_manager as wm
from src.initialisation.signals import right_buttons as rb
from src.initialisation.signals import bottom_buttons as bb


class InitialisationWindow:
    """Classe contenant tous les éléments pour la fenêtre d'initialisation simulateur"""

    # Eléments utiles à la fenêtre et les QWidgets contenus sur celle-ci
    engine = None
    win = None
    bottom_buttons = None
    right_buttons = None

    # Stocke si la page est chargée et si elle est complète (pour lancer le simulateur
    pages_list = [None] * 8     # Stocke les pages que l'utilisateur peut afficher

    # Variable stockant l'index de la fenêtre de paramètres actuellement chargée
    active_page_index = None       # Stocke l'index de la page de paramètres active de 1 à 8

    # Variable stockant la langue actuelle de l'application d'initialisation
    language = "Français"

    # Variables stockant les chemins d'accès vers le fichjier de traduction et de paramètres généraux
    translation_file_path = f"{PROJECT_DIR}settings\\language_settings\\initialisation.lang"
    general_settings_folder_path = f"{PROJECT_DIR}settings\\general_settings\\"
    default_settings_file_path = f"{general_settings_folder_path}default.settings"
    initialisation_window_file_path = f"{PROJECT_DIR}src\\initialisation\\initialisation_window.qml"

    # Variable stockant si le simulateur va être lancé
    launch_simulator = False

    def __init__(self):
        """initialise toutes les fenêtre du programme d'initialisation du simulateur sardine

        Parameters
        ----------
        app: `QApplication`
            L'application sur laquelle l'application d'initialisation va se lancer (un maximum par lancement)

        Raises
        ------
        FileNotFoundError
            Soulevé quand le fichier .qml de la fenêtre d'initialisation n'est pas trouvé
        SyntaxError
            Soulevé quand le fichier .qml de la fenêtre d'initialisation a une erreur de syntaxe et n'est pas lisible
        """
        initial_time = time.perf_counter()
        log.change_log_prefix("Chargement application d'initialisation")
        log.info(f"Début du chargement de l'application d'initialisation.")

        # Cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.engine = QQmlApplicationEngine()
        self.engine.load(self.initialisation_window_file_path)

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile(self.initialisation_window_file_path):
            raise FileNotFoundError(f"Le fichier .qml de la fenêtre d\'initialisation n\'a pas été trouvé.\n\t" +
                                    self.initialisation_window_file_path)
        elif not self.engine.rootObjects() and os.path.isfile(self.initialisation_window_file_path):
            raise SyntaxError(f"Le fichier .qml pour la fenêtre d\'initialisation contient des erreurs.\n\t" +
                              self.initialisation_window_file_path)
        else:
            self.win = self.engine.rootObjects()[0]
            self.win.closed.connect(lambda: QApplication.instance().quit())

        # Charge la traduction Anglais -> langue actuel (Français) et charge les pages de paramètres et les boutons.
        translations = td.TranslationDictionary()
        translations.create_translation(self.translation_file_path, "English", self.language)
        self.right_buttons = rb.RightButtons(self, translations)
        self.bottom_buttons = bb.BottomButtons(self)

        # Vérifie si un fichier de paramètres par défaut existe
        if os.path.isfile(self.default_settings_file_path):
            # S'il existe, l'ouvre, récupère ses données et les changent dans l'application d'initialisation
            log.info(f"Chargement des paramètres par défaut et mise à jour de l'application.",
                     prefix="Mise à jour paramètres, généraux")
            default_settings = sd.SettingsDictionary()
            if default_settings.open(self.default_settings_file_path):
                self.set_settings(default_settings, True)
            log.change_log_prefix("Chargement application d'initialisation")
        else:
            log.info(f"Aucun fichier de paramètres par défaut.\n\t{self.default_settings_file_path}")

        # Indique le temps de chargement de l'application
        log.info(f"Application d'initialisation chargée en " +
                 f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.\n")

        # Charge la logique de la première page de paramètres
        if self.active_page_index is not None:
            # Dans le cas ou au moins une page a été chargée entièrement, change le préfix et appelle son ouverture
            log.change_log_prefix(f"page_rb{self.active_page_index}")
            log.info(f"Ouverture de la page de paramètres page_rb{self.active_page_index}.")

            # Appelle la fonction d'ouverture logique de la page si celle-ci existe
            if "on_page_opened" in dir(self.pages_list[self.active_page_index - 1]):
                self.pages_list[self.active_page_index - 1].on_page_opened(self)

        # Montre la fenêtre principale,  et Lance l'application
        log.change_log_window_visibility(True)
        self.win.show()
        QApplication.instance().exec()

        # Quand l'application est fermée, cache la fenêtre de l'application d'initialisation et ses fenêtres annexes
        self.win.hide()

    def get_settings(self):
        """Récupère les paramètres des différentes pages de paramètres en appelant chaque fonction get_settings()

        Returns
        -------
        settings : `sd.SettingsDictionary`
            un dictionaire de paramètres avec tous les paramètres du simulateur
        """
        log.add_empty_lines()
        initial_time = time.perf_counter()
        settings = sd.SettingsDictionary()

        # Change le préfix pour indiquer que les paramètres vont être récupérés
        log.change_log_prefix("Récupération paramètres")

        # Dans le cas où des fonctions get_settings sont détectés, récupère les paramètres de l'application
        if any(["get_settings" in dir(page) for page in self.pages_list]):
            log.info(f"Récupération des paramètres de l'application d'initialisation.")

            # Récupère l'indication du clavier virtuel
            settings["virtual_keyboard"] = self.win.findChild(QObject, "virtual_keyboard_check").property("is_checked")

            # Récupère l'écran sur lequel se situe la fenêtre d'initialisation.
            wm.get_window_geometry(self.win, settings, "initialisation.")
            log.get_log_window_geometry(settings, "initialisation log window")

            # Récupère la traduction anglaise car les paramètres textuels sont stockés en anglais
            translations = td.TranslationDictionary()
            translations.create_translation(self.translation_file_path, self.language, "English")

            # Récupère le reste des données du simulateur (en appelant la fonction get_settings pour chaque page
            for page_index, page in ((i, p) for (i, p) in enumerate(self.pages_list) if "get_settings" in dir(p)):
                try:
                    settings.update(page.get_settings(translations))
                except Exception as error:
                    # Récupère une potentielle erreur dans la fonction d'écriture des valeurs
                    log.warning(f"Erreur lors de la récupération des paramètres sur la page_rb{page_index}.",
                                exception=error)

            log.info(f"Récupération de {len(settings)} paramètres dans l'application d'initialisation en" +
                     f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.")
        elif os.path.isfile(self.default_settings_file_path):
            # Sinon récupère les paramètres du fichier par défaut s'il existe
            settings.open(self.default_settings_file_path)
            log.warning("Aucune fonction \"get_settings\" détectée. Récupération des paramètres par défaut.\n")
        else:
            # Si même le fichier de paramètres par défaut n'existe pas, retourne un dictionnaire de paramètres vide
            log.warning("Aucune fonction \"get_settings\" détectée. Aucun fichier de paramètres par défaut détecté. " +
                        "Liste de paramètres retournée vide.\n")

        # Remet le préfix de la page de paramètres actuelle
        log.change_log_prefix(f"page_rb{self.active_page_index}")

        return settings

    def set_settings(self, settings, resize_popup=False):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        settings: `sd.SettingsDictionary`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        resize_popup: `bool`
            Les popups doivent-elles être redimensionnées ?
        """
        # Change le préfix pour indiquer que les paramètres vont être mis à jour
        log.change_log_prefix("Mise à jour paramètres, généraux")

        # Si le combobox pour choisir la langue existe (page_rb1 chargée), alors change la langue dans cette combobox
        if self.pages_list[0] is not None and not isinstance(self.pages_list[0], QQmlApplicationEngine) \
                and str(settings.get_value("language", self.language)).lower() != self.language.lower():
            self.pages_list[0].page.findChild(QObject, "language_combo").change_selection(settings.get_value("language", self.language))
            # Changer la valeur du combobox appelera automatquement la fonction change_language()
            log.change_log_prefix("Mise à jour paramètres, généraux")

        initial_time = time.perf_counter()
        count = 0

        # Récupère la traduction par rapport à l'anglais car les paramètres textuels sont stockés en anglais
        translations = td.TranslationDictionary()
        translations.create_translation(self.translation_file_path, "English", self.language)

        # Change la valeur pour indiquer si le checkbutton est activé
        if settings.get_value("virtual_keyboard") is not None:
            self.win.findChild(QObject, "virtual_keyboard_check").setProperty("is_checked", bool(settings["virtual_keyboard"]))

        # Pour chaque page ayant une partie logique fonctionnelle et une fonction set_settings:
        for page in (p for p in self.pages_list if "set_settings" in dir(p)):
            try:
                # Appelle la fonction get_settings de la page et récupère une potentielle erreur sur la fonction
                page.set_settings(settings, translations, resize_popup)
                count += 1
            except Exception as error:
                # Permet de rattraper une potentielle erreur dans la fonction get_settings()
                log.warning(f"Erreur lors de la mise à jour des paramètres sur la page_rb{page.index}.",
                            exception=error)

        # Si les fenêtre doivent être redimensionées, change la taille de la fenêtre principale et de registre
        if resize_popup:
            wm.set_window_geometry(self.win, settings, "initialisation.", (640, 480))
            log.set_log_window_geometry(settings, "initialisation log window")

        # Indique le nombre de pages dont les paramètres on été changés
        log.info(f"Paramètres correctement changés sur {count} page{'s' if count > 1 else ''} en " +
                 f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.\n")

        # Remet le préfix à la page de paramètres actuelle
        log.change_log_prefix(f"page_rb{self.active_page_index}")

    def change_language(self, new_language):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de l'application d'initialisation

        Parameters
        ----------
        new_language: `str`
            la nouvelle langue de l'application
        """
        # Dans le cas où la langue actuelle et la nouvelle langue sont les mêmes, l'indique et retourne
        if self.language.lower() == new_language.lower():
            log.debug(f"La langue actuelle de l'application d'initialisation est déjà \"{self.language}\".\n")
            return

        # Change le préfix temporairement pour indiquer la traduction de l'application d'initialisation
        initial_time = time.perf_counter()
        log.add_empty_lines()
        log.change_log_prefix("Traduction application d'initialisation")

        # Récupère les traductions
        translations = td.TranslationDictionary()
        translations.create_translation(self.translation_file_path, self.language, new_language)

        if translations:
            log.info(f"Traduction de l'application d'initialisation ({self.language} -> {new_language})")

            # Appel de la fonction set_languages pour les boutons du bas
            self.bottom_buttons.change_language(self, translations)

            # Essaye de changer la langue pour chaque page ayant une partie fonctionnelle
            for page in (p for p in self.pages_list if "change_language" in dir(p)):
                try:
                    # Appelle la fonction get_settings de la page et récupère une potentielle erreur sur la fonction
                    page.change_language(translations)
                except Exception as error:
                    # Permet de rattraper une potentielle erreur dans la fonction get_settings()
                    log.warning(f"Erreur lors de la traduction de la page_rb{page.index}.",
                                exception=error)

            # Indique le temps de traduction
            log.info(f"Traduction de l'application d'initialisation de \"{self.language}\" à \"{new_language}\" en " +
                     f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.\n")

            # change la langue actuelle pour la nouvelle langue envoyée
            self.language = new_language

        # Remet le préfix à celui de la page
        log.change_log_prefix(f"page_rb{self.active_page_index}")
