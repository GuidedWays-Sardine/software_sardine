# Librairies par défaut
import os
import sys
import time


# Librairies graphiques
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.immersion.immersion as immersion
import src.misc.settings_dictionary.settings as sd
import src.misc.translation_dictionary.translation as td
from src.initialisation.signals import right_buttons as rb
from src.initialisation.signals import bottom_buttons as bb


class InitialisationWindow:
    """Classe contenant tous les éléments pour la fenêtre d'initialisation simulateur"""

    # Eléments utiles à la fenêtre et les QWidgets contenus sur celle-ci
    app = None
    engine = None
    win = None
    bottom_buttons = None
    right_buttons = None

    # Stocke si la page est chargée et si elle est complète (pour lancer le simulateur
    pages_list = [None] * 8     # Stocke les pages que l'utilisateur peut afficher
    screens_dimensions = []        # Données sur les écrans connectés : format : [[x, y], [w, h], ...]

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

    def __init__(self, app):
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
        log.change_log_prefix("Initialisation application d'initialisation")
        log.info(f"Début du chargement de l'application d'intialisation.")

        # Commence par initialiser le mode immersion en mode EMPTY
        immersion.change_mode(immersion.Mode.EMPTY)

        # Charge tous les écrans connectés à l'ordinateur (utile pour la positionnement de certaines popup)
        for screen_index in range(0, QDesktopWidget().screenCount()):
            # Charge les informations de l'écran (au format [x_min, y_min, x_max, y_max]
            sg = QDesktopWidget().screenGeometry(screen_index).getCoords()

            # Les stockes au bon format [[x, y], [w, h]]
            self.screens_dimensions.append([[sg[0], sg[1]], [sg[2] - sg[0] + 1, sg[3] - sg[1] + 1]])
        log.info(f"Détection de {len(self.screens_dimensions)} écrans connectés à l'ordinateur.")

        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.app = app
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
            self.win.hide()

        # Charge la traduction Anglais -> langue actuel (Français) et charge les pages de paramètres et les boutons.
        translations = td.TranslationDictionary()
        translations.create_translation(self.translation_file_path, "English", self.language)
        self.right_buttons = rb.RightButtons(self, translations)
        self.bottom_buttons = bb.BottomButtons(self)

        # Vérifie si un fichier de paramètres par défaut existe
        if os.path.isfile(self.default_settings_file_path):
            # S'il existe, l'ouvre, récupère ses données et les changent dans l'application d'initialisation
            log.change_log_prefix("Ouverture fichier default.settings")
            log.info(f"Chargement des paramètres par défauts du fichier default.settings")
            default_settings = sd.SettingsDictionary()
            default_settings.open(self.default_settings_file_path)
            self.set_settings(default_settings)

            # De plus si les paramètres pour la taille et la position de la fenêtre existent, essaye de les récupérer
            if all([(f"initialisation.{p}" in default_settings) for p in ["screen_index", "x", "y", "w", "h"]]):
                try:
                    # Récupère l'index de l'écran et le met à 1 si pas assez d'écrans sont connectés
                    screen_index = default_settings["initialisation.screen_index"]
                    if not (1 <= default_settings["initialisation.screen_index"] <= len(self.screens_dimensions)):
                        log.debug(f"L'écran {screen_index} n'existe pas ({len(self.screens_dimensions)} écrans).")
                        screen_index = 1

                    # Commence par calculer la taille théorique maximale selon la position de la fenêtre et la taille écran
                    max_window_size = [self.screens_dimensions[screen_index - 1][1][0] - default_settings["initialisation.x"],
                                       self.screens_dimensions[screen_index - 1][1][1] - default_settings["initialisation.y"]]

                    # Puis garde la dimensions la plus faible entre sa taille demandée et la taille maximale possible
                    window_size = [min(max_window_size[0], default_settings["initialisation.w"]),
                                   min(max_window_size[1], default_settings["initialisation.h"])]

                    # S'assure que la fenêtre (de taille minimale 640*480) rentre bien là où elle doit être placée
                    if window_size[0] >= 640 and window_size[1] >= 480:
                        # Repositione et redimensionne la fenêtre
                        self.win.setPosition(self.screens_dimensions[screen_index - 1][0][0] + default_settings["initialisation.x"],
                                             self.screens_dimensions[screen_index - 1][0][1] + default_settings["initialisation.y"])
                        self.win.resize(window_size[0], window_size[1])
                    else:
                        log.debug(f"La fenêtre ne rentre pas à l'écran. ({window_size} au lieu de [640, 480] minimum).")
                except Exception as error:
                    # Récupère une exception si l'une des données n'est pas au bon format
                    log.warning("Erreur lors du redimensionement de la fenêtre d'initialisation (surement dû aux paramètres)",
                                exception=error)
            # Sinon laisse un message de debug indiquant que certaines données sont manquantes
            else:
                log.debug(f"Aucune information stocké sur la taille par défaut de la fenêtre d'initialisation.")

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
        self.win.show()
        self.win.closed.connect(lambda: self.app.quit())
        self.app.exec()

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

        # Dans le cas où des fonctions get_settings sont détectés, récupère les paramètres de l'application
        if any(["get_settings" in dir(page) for page in self.pages_list]):
            log.info(f"Récupération des paramètres de l'application.")

            # Récupère l'écran sur lequel se situe la fenêtre d'initialisation.
            screens = QDesktopWidget()
            screen_index = [i for i in range(0, screens.screenCount())
                            if screens.screenGeometry(i).getCoords()[0] - 1 < self.win.x() <=
                            screens.screenGeometry(i).getCoords()[2]
                            and screens.screenGeometry(i).getCoords()[1] - 1 < self.win.y() <=
                            screens.screenGeometry(i).getCoords()[3]]

            # Si la fenêtre d'initialisation a été détecté sur un écran, récupère et stocke ses coordonées
            if screen_index:
                sg = screens.screenGeometry(screen_index[0]).getCoords()
                settings["initialisation.screen_index"] = screen_index[0] + 1
                settings["initialisation.x"] = self.win.x() - sg[0]
                settings["initialisation.y"] = self.win.y() - sg[1]
                settings["initialisation.w"] = (self.win.width() if (self.win.x() + self.win.width() <= sg[2] + 1)
                                                  else self.win.property("minimumWidth"))
                settings["initialisation.h"] = (self.win.height() if (self.win.y() + self.win.height() <= sg[3] + 1)
                                                  else self.win.property("minimumHeight"))

                log.info("emplacement de la fenêtre d'initialisation récupéré avec succès : " +
                         str([settings[f"initialisation.{p}"] for p in ["screen_index", "x", "y", "w", "h"]]))
            else:
                log.warning(f"Impossible de localiser la fenêtre d'initialisation.")

            # Récupère la traduction anglaise car les paramètres textuels sont stockés en anglais
            translations = td.TranslationDictionary()
            translations.create_translation(self.translation_file_path, self.language, "English")

            # Récupère le reste des données du simulateur (en appelant la fonction get_settings pour chaque page
            for page_index, page in ((i, p) for (i, p) in enumerate(self.pages_list) if "get_settings" in dir(p)):
                try:
                    settings.update(page.get_settings(translations))
                except Exception as error:
                    # Récupère une potentielle erreur dans la fonction d'écriture des valeurs
                    log.warning(f"Erreur lors de la récupération des paramètres pour la page_rb{page_index}.",
                                exception=error)

            log.info(f"Chargement de {len(settings)} paramètres en" +
                     f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.\n")
        elif os.path.isfile(self.default_settings_file_path):
            # Sinon récupère les paramètres du fichier par défaut s'il existe
            settings.open(self.default_settings_file_path)
            log.add_empty_lines()
        else:
            log.warning("Aucune page de paramètres correctement chargée et pas de fichier default.settings.\n")

        return settings

    def set_settings(self, settings):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        settings: `sd.SettingsDictionary`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        """
        log.info(f"Changement de paramètres sur l'application d'initialisation.")

        # Si la combobox pour choisir la langue existe (page_rb1 chargée), alors change la langue dans cette combobox
        # La langue de l'application d'initialisation sera changée automatiquement
        if self.pages_list[0] is not None and not isinstance(self.pages_list[0], QQmlApplicationEngine):
            # Si la langue est différente essaye de changer la langue du simulateur
            language_combo = self.pages_list[0].page.findChild(QObject, "language_combo")
            language_combo.change_selection(settings.get_value("language", language_combo.property("text")))

        initial_time = time.perf_counter()
        count = 0

        # Récupère la traduction par rapport à l'anglais car les paramètres textuels sont stockés en anglais
        translations = td.TranslationDictionary()
        translations.create_translation(self.translation_file_path, "English", self.language)

        # Pour chaque page ayant une partie logique fonctionnelle et une fonction set_settings:
        for page in (p for p in self.pages_list if "set_settings" in dir(p)):
            try:
                # Appelle la fonction get_settings de la page et récupère une potentielle erreur sur la fonction
                page.set_settings(settings, translations)
                count += 1
            except Exception as error:
                # Permet de rattraper une potentielle erreur dans la fonction get_settings()
                log.warning(f"Erreur lors du changement des paramètres pour la page_rb{page.index}.",
                            exception=error)

        # Indique le nombre de pages dont les paramètres on été changés
        log.info(f"Paramètres correctement changés sur {count} pages en " +
                 f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.\n")

    def change_language(self, new_language):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de l'application d'initialisation

        Parameters
        ----------
        new_language: `str`
            la nouvelle langue de l'application
        """
        initial_time = time.perf_counter()
        log.info(f"Changement de la langue, mise à jour de la langue de l'application d'initialisation.")

        translations = td.TranslationDictionary()
        translations.create_translation(self.translation_file_path, self.language, new_language)

        if translations:
            # Appel de la fonction set_languages pour les boutons du bas
            self.bottom_buttons.change_language(self, translations)

            # Essaye de changer la langue pour chaque page ayant une partie fonctionnelle
            for page in (p for p in self.pages_list if "change_language" in dir(p)):
                try:
                    # Appelle la fonction get_settings de la page et récupère une potentielle erreur sur la fonction
                    page.change_language(translations)
                except Exception as error:
                    # Permet de rattraper une potentielle erreur dans la fonction get_settings()
                    log.warning(f"Erreur lors du changement de langue pour la page_rb{page.index}.",
                                exception=error)

            # change la langue actuelle pour la nouvelle langue envoyée
            self.language = new_language

            log.info(f"La langue de l'application d'initialisation a été changée en " +
                     f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.\n")
        else:
            log.warning("Traduction impossible, aucune traduction trouvées.\n")


def main():
    log.initialise(log_level=log.Level.DEBUG, save=True)

    # Lance l'application d'initialisation
    app = QApplication(sys.argv)
    application = InitialisationWindow(app)

    if application.launch_simulator:
        log.info(str(application.get_settings()), prefix="Données Collectées")


if __name__ == "__main__":
    main()
