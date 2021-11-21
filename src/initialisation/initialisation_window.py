# Librairies par défaut
import os.path
import sys
import traceback
import time


# Librairies graphiques
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
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
    visible_pages = [None] * 8     # Stocke les pages que l'utilisateur peut afficher
    is_fully_loaded = [False] * 8  # Stocke directement l'instance de la classe
    is_completed_by_default = [False] * 8     # Détecte si la page est complété (égale à self.visible_pages si tout est complété)

    # Variable stockant la langue actuelle de l'application d'initialisation
    language = "Français"

    # Variable stockant l'index de la fenêtre de paramètres actuellement chargée
    active_settings_page = None       #Stocke la page de paramètres active de 1 à 8

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
        initial_time = time.time()
        log.change_log_prefix("Initialisation")
        log.info("Début du chargement de l'application d'intialisation.\n\n")

        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.app = app
        self.engine = QQmlApplicationEngine()
        self.engine.load(PROJECT_DIR + "src\\initialisation\\initialisation_window.qml")

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile(PROJECT_DIR + "src\\initialisation\\initialisation_window.qml"):
            raise FileNotFoundError("Le fichier .qml pour la fenêtre d\'initialisation n\'a pas été trouvé.")
        elif not self.engine.rootObjects() and os.path.isfile(PROJECT_DIR + "src\\initialisation\\initialisation_window.qml"):
            raise SyntaxError("Le fichier .qml pour la fenêtre d\'initialisation contient des erreurs.")

        # Si le fichier qml a été compris, récupère la fenêtre et initialise les différents boutons et pages
        self.win = self.engine.rootObjects()[0]
        self.win.hide()
        self.bottom_buttons = bb.BottomButtons(self)
        self.right_buttons = rb.RightButtons(self)

        # Vérifie si un fichier de paramètres par défaut existe
        if os.path.isfile(PROJECT_DIR + "settings\\general_settings\\default.settings"):
            # S'il existe, l'ouvre, récupère ses données et les changent dans l'application d'initialisation
            log.info("Chargement des paramètres du fichier default.settings.\n")
            default_settings = sd.SettingsDictionnary()
            default_settings.open(PROJECT_DIR + "settings\\general_settings\\default.settings")
            self.set_values(default_settings)

            # De plus si les paramètres pour la taille et la position de la fenêtre existe, essaye de les récupérer
            dimensions = [None] * 4  # x, y, w, h
            try:
                # Récupère l'écran et calcule la position relative de la fenêtre
                screen = default_settings["initialisation.screen_index"]
                screen_dimensions = QDesktopWidget().screenGeometry(screen - 1).getCoords()
                dimensions[0] = screen_dimensions[0] + default_settings["initialisation.x"]
                dimensions[1] = screen_dimensions[1] + default_settings["initialisation.y"]

                # Pour les deux dimensiosn des fenêtres vérifie si :
                # La taille indiqué rentre dans l'écran sur lequel on se situe
                # Sinon si la dimensions restant de la fenêtre est suffisant pour faire rentrer la fenêtre
                if dimensions[0] + default_settings["initialisation.w"] + 1 <= screen_dimensions[2]:
                    dimensions[2] = default_settings["initialisation.w"]
                elif screen_dimensions[2] - dimensions[0] + 1 >= self.win.property("minimumWidth"):
                    dimensions[2] = screen_dimensions[2] - dimensions[0] + 1
                if dimensions[1] + default_settings["initialisation.h"] + 1 <= screen_dimensions[3]:
                    dimensions[3] = default_settings["initialisation.h"]
                elif screen_dimensions[3] - dimensions[1] + 1 >= self.win.property("minimumHeight"):
                    dimensions[3] = screen_dimensions[3] - dimensions[1] + 1

                # Si la position et la taille de la fenêtre a été calculé avec succès, place et dimensionne la fenêtre
                if not list(x for x in dimensions if x is None):
                    self.win.setPosition(dimensions[0], dimensions[1])
                    self.win.resize(dimensions[2],  dimensions[3])
                else:
                    log.debug("Les données pour la position et taille de la fenêtre d'initialisation sont incorect.\n\n")
            except KeyError:
                log.debug("Aucune information stocké sur la taille par défaut de la fenêtre d'initialisation.\n\n")
        else:
            log.info("Aucun fichier paramètres default.settings. Tous les éléments par défaut seront pris.\n\n")

        # Indique le temps de chargement de l'application
        log.info("Application d'initialisation chargée en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

        # Charge la logique de la première page de paramètres
        if self.active_settings_page is not None:
            # Dans le cas ou au moins une page a été chargée entièrement, change le préfix et appelle son ouverture
            log.change_log_prefix("page_rb" + str(self.active_settings_page))
            log.info("Ouverture de la page de paramètres page_rb" + str(self.active_settings_page) + ".\n")

            # Appelle la fonction d'ouverture logique de la page si celle-ci existe
            if self.is_fully_loaded[self.active_settings_page - 1] and \
                    "on_page_opened" in dir(self.visible_pages[self.active_settings_page - 1]):
                try:
                    self.visible_pages[self.active_settings_page - 1].on_page_opened(self)
                except Exception as error:
                    log.error("La fonction on_page_opened de la page " + str(self.active_settings_page) +
                              " contient une erreur.\n\t\t" +
                              "Erreur de type : " + str(type(error)) + "\n\t\t" +
                              "Avec comme message d\'erreur : " + str(error.args) + "\n\n\t\t" +
                              "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

        # Montre la fenêtre principale, indique que l'application doit se quitter quand celle-ci est fermée et Lance l'application
        self.win.show()
        self.win.closed.connect(lambda: self.app.quit())
        self.app.exec()

        # Quand l'application est fermée, cache la fenêtre de l'application d'initialisation et ses fenêtres annexes
        self.win.hide()

    def get_values(self):
        """Récupère les paramètres des différentes pages de paramètres en appelant chaque fonction get_values()

        Returns
        -------
        parameters : `sd.SettingsDictionnary`
            un dictionaire de paramètres avec tous les paramètres du simulateur
        """
        initial_time = time.time()
        log.info("Récupération des paramètres de l'application.\n")
        parameters = sd.SettingsDictionnary()

        screens = QDesktopWidget()
        screen_index = list(i for i in range(0, screens.screenCount())
                            if screens.screenGeometry(i).getCoords()[0] - 1 < self.win.x() <=
                            screens.screenGeometry(i).getCoords()[2]
                            and screens.screenGeometry(i).getCoords()[1] - 1 < self.win.y() <=
                            screens.screenGeometry(i).getCoords()[3])
        if screen_index:
            sg = screens.screenGeometry(screen_index[0]).getCoords()
            parameters["initialisation.screen_index"] = screen_index[0] + 1
            parameters["initialisation.x"] = self.win.x() - sg[0]
            parameters["initialisation.y"] = self.win.y() - sg[1]
            parameters["initialisation.w"] = (self.win.width() if (self.win.x() + self.win.width() <= sg[2] + 1)
                                                               else self.win.property("minimumWidth"))
            parameters["initialisation.h"] = (self.win.height() if (self.win.y() + self.win.height() <= sg[3] + 1)
                                                                else self.win.property("minimumHeight"))
        else:
            log.warning("Impossible de localiser la fenêtre d'initialisation.\n")

        # Vérifie si au moins une page est chargé graphiquement. (sinon tente de charger les paramètres défaut.settings)
        if not any(self.is_fully_loaded) and os.path.isfile(PROJECT_DIR + "settings\\general_settings\\default.settings"):
            # Si aucune page n'est chargée correctement et que le fichier default.settings existe
            parameters.open(PROJECT_DIR + "settings\\general_settings\\default.settings")
        elif any(self.is_fully_loaded):
            # Récupère ma traduction anglaise car les paramètres textuels sont stockés en anglais
            translation_data = td.TranslationDictionnary()
            translation_data.create_translation(PROJECT_DIR + "settings\\language_settings\\initialisation.lang",
                                                self.language, "English")

            # Pour chaque page ayant une partie logique fonctionnelle et une fonction get_values:
            for page in (p for p in self.visible_pages if "get_values" in dir(p)):
                try:
                    # Appelle la fonction get_values de la page et si celle-ci fonctionne, récupère ses paramètres
                    parameters.update(page.get_values(translation_data))
                except Exception as error:
                    # Permet de rattraper une potentielle erreur dans la fonction get_values()
                    log.warning("Erreur lors de la récupération des paramètres pour la page : " + str(page.index) +
                                "\n\t\tErreur de type : " + str(type(error)) +
                                "\n\t\tAvec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                                "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

        # Retourne le dictionnaire complété grâce aux différentes valeurs des get_values() de chaques pages
        log.info("Récupération de " + str(len(parameters)) + " paramètres sur l'application d'initialisation en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")
        return parameters

    def set_values(self, data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        data: `sd.SettingsDictionnary`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        """
        # Si la combobox pour choisir la langue existe (page_rb1 chargée), alors change la langue dans cette combobox
        # La langue de l'application d'initialisation sera changée automatiquement
        if self.visible_pages[0] is not None and not isinstance(self.visible_pages[0], type(self.engine)):
            language_combo = self.visible_pages[0].page.findChild(QObject, "language_combo")
            try:
                # Si la langue est différente essaye de changer la langue du simulateur
                if language_combo.property("text") != data["Langue"]:
                    language_combo.change_selection(data["Langue"])
            except KeyError:
                # Si le paramètre "Langue" n'apparait pas, laisse juste un message de debug
                log.debug("Impossible de changer la langue du simulateur car : \"Langue\" est manquant.\n")

        initial_time = time.time()
        log.info("Tentative de changement des paramètres.\n")
        count = 0

        # Récupère la traduction par rapport à l'anglais car les paramètres textuels sont stockés en anglais
        translation_data = td.TranslationDictionnary()
        translation_data.create_translation(PROJECT_DIR + "settings\\language_settings\\initialisation.lang",
                                            "English", self.language)

        # Pour chaque page ayant une partie logique fonctionnelle et une fonction set_values:
        for page in (p for p in self.visible_pages if "set_values" in dir(p)):
            try:
                # Appelle la fonction get_values de la page et récupère une potentielle erreur sur la fonction
                page.set_values(data, translation_data)
                count += 1
            except Exception as error:
                # Permet de rattraper une potentielle erreur dans la fonction get_values()
                log.warning("Erreur lors du changement des paramètres pour la page : " + str(page.index) +
                            "\n\t\tErreur de type : " + str(type(error)) +
                            "\n\t\tAvec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                            "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

            # Indique le nombre de pages dont les paramètres on été changés
        log.info("Paramètres correctement changés sur " + str(count) + " pages en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

    def change_language(self, new_language):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de l'application d'initialisation

        Parameters
        ----------
        new_language: `str`
            la nouvelle langue de l'application
        """
        initial_time = time.time()
        log.info("Changement du choix de langue, mise à jour de l'application d'initialisation.\n")

        translation_data = td.TranslationDictionnary()
        translation_data.create_translation(PROJECT_DIR + "settings\\language_settings\\initialisation.lang",
                                            self.language, new_language)

        # Appel de la fonction set_languages pour les boutons du bas
        self.bottom_buttons.change_language(self, translation_data)

        # Essaye de changer la langue pour chaque page ayant une partie fonctionnelle
        for page in (p for p in self.visible_pages if "change_language" in dir(p)):
            try:
                # Appelle la fonction get_values de la page et récupère une potentielle erreur sur la fonction
                page.change_language(translation_data)
            except Exception as error:
                # Permet de rattraper une potentielle erreur dans la fonction get_values()
                log.warning("Erreur lors du changement de langue pour la page : " + str(page.index) +
                            "\n\t\tErreur de type : " + str(type(error)) +
                            "\n\t\tAvec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                            "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

        # Si la traduction a été réalisée correctement (traduction trouvée) alors change la langue actuelle
        self.language = new_language if translation_data else self.language

        log.info("La langue du simulateur (et de l'application d'initialisation) a été changée en " +
                 str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n")


def main():
    log.initialise(PROJECT_DIR + "log", "1.1.0", log.Level.DEBUG)

    #Lance l'application d'initialisation
    application = InitialisationWindow()

    if application.launch_simulator:
        log.info(str(application.get_values()), prefix="Données Collectées")


if __name__ == "__main__":
    main()
