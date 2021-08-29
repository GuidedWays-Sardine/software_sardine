import os.path
import sys
import logging
import traceback
import time

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

from initialisation.signals import right_buttons as rb
from initialisation.signals import bottom_buttons as bb


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
    is_completed = [False] * 8     # Détecte si la page est complété (égale à self.visible_pages si tout est complété)

    # Variable stockant l'index de la fenêtre de paramètres actuellement chargée
    active_settings_page = -1

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
        logging.info("Début du chargement de l'application d'intialisation\n\n")

        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)
        self.engine = QQmlApplicationEngine()
        self.engine.load('initialisation/initialisation_window.qml')

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile("initialisation/initialisation_window.qml"):
            raise FileNotFoundError("Le fichier .qml pour la fenêtre d\'initialisation n\'a pas été trouvé.")
        elif not self.engine.rootObjects() and os.path.isfile("initialisation/initialisation_window.qml"):
            raise SyntaxError("Le fichier .qml pour la fenêtre d\'initialisation contient des erreurs.")

        # Si le fichier qml a été compris, récupère la fenêtre et initialise les différents boutons et pages
        self.win = self.engine.rootObjects()[0]
        self.win.visibilityChanged.connect(lambda: self.app.quit())
        self.bottom_buttons = bb.BottomButtons(self)
        self.right_buttons = rb.RightButtons(self)

        # Lance l'application
        logging.info("Application d'initialisation chargée en " +
                     str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")
        self.win.show()
        self.app.exec()

    def get_values(self):
        """Récupère les paramètres des différentes pages de paramètres en appelant chaque fonction get_values()

        Returns
        -------
        parameters : `dictionary`
            un dictionaire de paramètres si le simulateur a été lancé, sinon None"""
        initial_time = time.time()
        logging.info("Tentative de récupération des paramètres.\n")
        parameters = {}

        # Pour chaque page ayant une partie logique fonctionnelle :
        for page in (x for x in self.visible_pages if x is not None and not isinstance(x, type(self.engine))):
            # Vérifie que la page contient bien une fonction get_values()
            if "get_values" in dir(page):
                try:
                    # Appelle la fonction get_values de la page et si celle-ci fonctionne, récupère ses paramètres
                    page.get_values()
                except Exception as error:
                    # Permet de rattraper une potentielle erreur dans la fonction get_values()
                    logging.warning("Erreur lors de la récupération des paramètres pour la page : " + str(page.index) +
                                    "\n\t\tErreur de type : " + str(type(error)) +
                                    "\n\t\tAvec comme message d'erreur : " + error.args[0] + "\n\n\t\t" +
                                    "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
            else:
                logging.warning("La page " + str(page.index) + " n'a pas de fonction get_values.\n")

        # Retourne le dictionnaire complété grâce aux différentes valeurs des get_values() de chaques pagesee
        logging.info("Récupération de " + str(len(parameters)) + " paramètres sur l'application d'initialisation en " +
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
        logging.info("Tentative de changement des paramètres.\n")
        count = 0

        # Pour chaque page ayant une partie logique fonctionnelle :
        for page in (x for x in self.visible_pages if x is not None and not isinstance(x, type(self.engine))):
            # Vérifie que la page contient bien une fonction set_values()
            if "set_values" in dir(page):
                try:
                    # Appelle la fonction get_values de la page et récupère une potentielle erreur sur la fonction
                    page.set_values(data)
                    count += 1
                except Exception as error:
                    # Permet de rattraper une potentielle erreur dans la fonction get_values()
                    logging.warning("Erreur lors du changement des paramètres pour la page : " + str(page.index) +
                                    "\n\t\tErreur de type : " + str(type(error)) +
                                    "\n\t\tAvec comme message d'erreur : " + error.args[0] + "\n\n\t\t" +
                                    "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
            else:
                logging.warning("La page " + str(page.index) + " n'a pas de fonction set_values.\n")

            # Indique le nombre de pages dont les paramètres on été changés
            logging.info("Paramètres changés sur " + str(count) + " pages en " +
                         str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

    def change_language(self, translation_data):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de l'application d'initialisation

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) /!\\ clés en majuscules"""
        initial_time = time.time()
        logging.info("Changement du choix de langue, mise à jour de l'application d'initialisation.\n")

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
                    logging.warning("Erreur lors du changement de langue pour la page : " + str(page.index) +
                                    "\n\t\tErreur de type : " + str(type(error)) +
                                    "\n\t\tAvec comme message d'erreur : " + error.args[0] + "\n\n\t\t" +
                                    "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
                else:
                    logging.warning("La page " + str(page.index) + " n'a pas de fonction change_language.\n")

        logging.info("La langue du simulateur (et de l'application d'initialisation) a été changée en " +
                     str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n")
