# Librairies par défaut
import os.path
import sys
import traceback
import time


# Librairies graphiques
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
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
    active_settings_page = -1       #Stocke la page de paramètres active de 1 à 8

    # Variable stockant si le simulateur va être lancé
    launch_simulator = False

    def __init__(self):
        """initialise toutes les fenêtre du programme d'initialisation du simulateur sardine

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
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)
        self.engine = QQmlApplicationEngine()
        self.engine.load(PROJECT_DIR + "src\\initialisation\\initialisation_window.qml")

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile(PROJECT_DIR + "src\\initialisation\\initialisation_window.qml"):
            raise FileNotFoundError("Le fichier .qml pour la fenêtre d\'initialisation n\'a pas été trouvé.")
        elif not self.engine.rootObjects() and os.path.isfile(PROJECT_DIR + "src\\initialisation\\initialisation_window.qml"):
            raise SyntaxError("Le fichier .qml pour la fenêtre d\'initialisation contient des erreurs.")

        # Si le fichier qml a été compris, récupère la fenêtre et initialise les différents boutons et pages
        self.win = self.engine.rootObjects()[0]
        #self.win.aboutToQuit()
        #self.win.visibilityChanged.connect(lambda: self.app.quit()) # FIXME : ferme l'application quand celle-ci est mise en plein écran
        self.bottom_buttons = bb.BottomButtons(self)
        self.right_buttons = rb.RightButtons(self)

        # Charge le fichier de paramètres défault.settings s'il existe
        # FEATURE:  ajouter un paramètre de la position et de la taille de la fenêtre
        if os.path.isfile(PROJECT_DIR + "settings\\general_settings\\default.settings"):
            log.info("Chargement des paramètres du fichier default.settings.\n")
            self.bottom_buttons.on_open_clicked(self, PROJECT_DIR + "settings\\general_settings\\default.settings") #FIXME : à améliorer
        else:
            log.info("Aucun fichier paramètres default.settings. Tous les éléments par défaut seront pris\n")

        # Indique le temps de chargement de l'application
        log.info("Application d'initialisation chargée en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

        # Charge la logique de la première page de paramètres
        if self.active_settings_page != -1:
            # Dans le cas ou au moins une page a été chargée entièrement, change le préfix et appelle son ouverture
            log.change_log_prefix("page_rb" + str(self.active_settings_page))
            log.info("Ouverture de la page de paramètres page_rb" + str(self.active_settings_page) + ".\n")

            if self.is_fully_loaded[self.active_settings_page - 1] and \
                    "on_page_opened" in dir(self.visible_pages[self.active_settings_page - 1]):
                # Si c'est le cas, appelle la fonction d'ouverture de la page
                try:
                    self.visible_pages[self.active_settings_page - 1].on_page_opened(self)
                except Exception as error:
                    log.error("La fonction on_page_opened de la page " + str(self.active_settings_page) +
                              " contient une erreur.\n\t\t" +
                              "Erreur de type : " + str(type(error)) + "\n\t\t" +
                              "Avec comme message d\'erreur : " + str(error.args) + "\n\n\t\t" +
                              "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
            else:
                log.debug("Aucune fonction on_page_opened page " + str(self.active_settings_page) + "\n")

        # Lance l'application
        self.win.show()
        self.app.exec()

        # Quand l'application est fermée, cache la fenêtre de l'application d'initialisation et ses fenêtres annexes
        self.win.hide()

    def get_values(self):
        """Récupère les paramètres des différentes pages de paramètres en appelant chaque fonction get_values()

        Returns
        -------
        parameters : `dictionary`
            un dictionaire de paramètres avec tous les paramètres du simulateur
        """
        initial_time = time.time()
        log.info("Tentative de récupération des paramètres.\n")
        parameters = {}     # OPTIMIZE: changer pour un dictionnaire de paramètres

        # Récupère la traduction anglaise car certains paramètres (exemple : chemins de fichiers) sont en anglais
        translation_data = {}   # OPTIMIZE: passer pour un dictionnaire de paramètres
        try:
            translation_data = self.read_language_file(self.language, "English")
        except Exception as error:
            # Rattrape une potentielle erreur lors de la création du dictionaire de traduction
            log.error("Erreur lors de la récupération du dictionaire de traduction dans get_values. " +
                      "Certains arguments ne pourront pas être enregistrés." +
                      "\n\t\tErreur de type : " + str(type(error)) +
                      "\n\t\tAvec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                      "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

        # Pour chaque page ayant une partie logique fonctionnelle :
        for page in (x for x in self.visible_pages if x is not None and not isinstance(x, type(self.engine))):
            # Vérifie que la page contient bien une fonction get_values()
            if "get_values" in dir(page):
                try:
                    # Appelle la fonction get_values de la page et si celle-ci fonctionne, récupère ses paramètres
                    parameters.update(page.get_values(translation_data))
                except Exception as error:
                    # Permet de rattraper une potentielle erreur dans la fonction get_values()
                    log.warning("Erreur lors de la récupération des paramètres pour la page : " + str(page.index) +
                                "\n\t\tErreur de type : " + str(type(error)) +
                                "\n\t\tAvec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                                "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
            else:
                log.warning("La page " + str(page.index) + " n'a pas de fonction get_values.\n")

        # Retourne le dictionnaire complété grâce aux différentes valeurs des get_values() de chaques pagesee
        log.info("Récupération de " + str(len(parameters)) + " paramètres sur l'application d'initialisation en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")
        return parameters

    def set_values(self, data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        data: `dict`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        """
        initial_time = time.time()
        log.info("Tentative de changement des paramètres.\n")
        count = 0
        translation_data = {}

        # Si la combobox pour choisir la langue existe (page_rb1 chargée), alors change la langue dans cette combobox
        # La langue de l'application d'initialisation sera changée automatiquement
        if self.visible_pages[0] is not None and not isinstance(self.visible_pages[0], type(self.engine)):
            language_combo = self.visible_pages[0].page.findChild(QObject, "language_combo")
            try:
                # Si la langue est différente essaye de changer la langue du simulateur
                if language_combo.property("text") != data["Langue"]:
                    language_combo.change_selection(data["Langue"])
            # Si le paramètre "Langue" n'apparait pas, laisse juste un message de debug
            except KeyError:
                log.debug("Impossible de changer la langue du simulateur car : \"Langue\" est manquant.\n")
            # Dans tous les cas récupère un dictionaire avec la langue actuelle (ou changée juste avant)
            try:
                translation_data = self.read_language_file("English", self.language)
            except Exception as error:
                # Rattrape une potentielle erreur lors de la création du dictionaire de traduction
                log.error("Erreur lors de la récupération du dictionaire de traduction. " +
                          "Certains arguments ne pourront pas être changés." +
                          "\n\t\tErreur de type : " + str(type(error)) +
                          "\n\t\tAvec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                          "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

        # Pour chaque page ayant une partie logique fonctionnelle :
        for page in (x for x in self.visible_pages if x is not None and not isinstance(x, type(self.engine))):
            # Vérifie que la page contient bien une fonction set_values()
            if "set_values" in dir(page):
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
            else:
                log.warning("La page " + str(page.index) + " n'a pas de fonction set_values.\n")

            # Indique le nombre de pages dont les paramètres on été changés
        log.info("Paramètres changés sur " + str(count) + " pages en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

    def read_language_file(self, current_language, new_language):   # FIXME : bouger dans le Misc settings dictionnary
        """Fonction permettant de lire le fichier de traduction et d'en resortir un dictionnaire de traduction

        Parameters
        ----------
        current_language: `str`
            langage actuel du texte à traduire
        new_language: `str`
            langage dans lequel le texte doit être traduit

        Returns
        -------
        translation_data: `dict`
            dictionaire contenant les traductions (clés = langage actuel ; valeurs = traductions)

        Raises
        ------
        FileNotFoundError
            Erreur émise si le fichier de traduction n'est pas trouvé
        ValueError
            Erreur émise si l'une des langues fournis n'existe pas
        """
        translation_data = {}

        # Ouvre le fichier et récupère la liste des langues
        file = open(PROJECT_DIR + "settings\\language_settings\\initialisation.lang", "r", encoding='utf-8-sig')
        language_list = file.readline().upper().rstrip('\n').split(";")

        # Récupère les index des langues
        current_index = language_list.index(current_language.upper())
        new_index = language_list.index(new_language.upper())

        # Récupère toutes les traductions
        for line in file:
            # Si la ligne est vide la saute, sinon récupère les traductions des mots
            if line != "\n" and line[0] != "#":
                translations = line.rstrip('\n').split(";")
                # Si la ligne est complète l'ajoute dans le dictionaire (clé = langue actuelle, valeur = traduction)
                if len(translations) == len(language_list):
                    #FEATURE : faire une classe pour rendre le dictionnaire case insensitive
                    translation_data[translations[current_index]] = translations[new_index]
                # S'il n'y a pas autant de traductions que de langue, cela signifie que la ligne est incomplète
                else:
                    log.debug("Certaines traductions manquantes sur la ligne suivante (langues attendus, mots) :" +
                              "\n\t\t" + ";".join(language_list) + "\n\t\t" + line)
        file.close()
        return translation_data

    def change_language(self, translation_data):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de l'application d'initialisation

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive
        """
        initial_time = time.time()
        log.info("Changement du choix de langue, mise à jour de l'application d'initialisation.\n")

        # Appel de la fonction set_languages pour les boutons du bas
        self.bottom_buttons.change_language(self, translation_data)

        # Essaye de changer la langue pour chaque page ayant une partie fonctionnelle
        for page in (x for x in self.visible_pages if x is not None and not isinstance(x, type(self.engine))):
            if "change_language" in dir(page):
                try:
                    # Appelle la fonction get_values de la page et récupère une potentielle erreur sur la fonction
                    page.change_language(translation_data)
                except Exception as error:
                    # Permet de rattraper une potentielle erreur dans la fonction get_values()
                    log.warning("Erreur lors du changement de langue pour la page : " + str(page.index) +
                                "\n\t\tErreur de type : " + str(type(error)) +
                                "\n\t\tAvec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                                "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
            else:
                log.warning("La page " + str(page.index) + " n'a pas de fonction change_language.\n")

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
