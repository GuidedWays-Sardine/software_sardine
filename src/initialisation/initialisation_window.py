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

        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)
        self.engine = QQmlApplicationEngine()
        self.engine.load('initialisation/initialisation_window.qml')

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile('initialisation/initialisation_window.qml'):
            raise FileNotFoundError('Le fichier .qml pour la fenêtre d\'initialisation n\'a pas été trouvé.')
        elif not self.engine.rootObjects() and os.path.isfile('initialisation/initialisation_window.qml'):
            raise SyntaxError('Le fichier .qml pour la fenêtre d\'initialisation contient des erreurs.')

        # Si le fichier qml a été compris, récupère la fenêtre et initialise les différents boutons et pages
        self.win = self.engine.rootObjects()[0]
        self.bottom_buttons = bb.BottomButtons(self)
        self.right_buttons = rb.RightButtons(self)

        # Lance l'application
        logging.info("Application d'initialisation chargée en " +
                     str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n")
        self.win.show()
        self.app.exec()

    def get_values(self):
        """Récupère les valeurs entrées dans

        Returns
        -------
        parameters : `dictionary`
            un dictionaire de paramètres si le simulateur a été lancé, sinon None"""
        parameters = {}

        # Vérifie pour chaque page existante si une fonction get_values existe.
        # Si oui, récupère les valeurs et les rajoutes à un dictionnaire
        # Sinon, met un message d'erreur dans le fichier log et passe à la page suivante
        for index in range(1, 9):
            # Vérifie d'abord si la page a des signals handlers (et donc potentiellement des valeurs à récupérer)
            if self.is_fully_loaded[index - 1]:
                page_path = "initialisation/signals/page_rb/page_rb" + str(index) + ".py"

                # Ensuite vérifie que la page contient bien une fonction get_values()
                if "get_values" in dir(self.visible_pages[index - 1]):
                    try:
                        # Appelle la fonction get_values de la page et récupère une potentielle erreur sur la fonction
                        self.visible_pages[index - 1].get_values()
                    except Exception as err:
                        # Permet de rattraper une autre potentielle erreur par sécurité (dû au exec())
                        logging.warning("Erreur inconnu lors de la récupération des donnés pour : " + page_path +
                                        "\n\t\tErreur de type : " + str(type(err)) +
                                        "\n\t\tAvec comme message d\'erreur : " + err.args[0] + "\n\n\t\t" +
                                        ''.join(traceback.format_tb(err.__traceback__)).replace('\n', '\n\t\t') + "\n")
                else:
                    logging.warning("La page " + str(index) + "de paramètre : " + page_path + "n\'a pas get_values.\n")

        # Retourne le dictionnaire complété grâce aux différentes valeurs des get_values() de chaques pages
        logging.info("Récupération de " + str(len(parameters)) + " paramètres sur l'application d'initialisation.\n")
        return parameters

    def set_values(self, data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        data: `dict`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        """
        # Vérifie pour chaque page existante si une fonction set_values existe.
        # Si oui, appelle la fonction en envoyant le dictionnaire
        # Sinon, met un message d'erreur dans le fichier log et passe à la page suivante
        count = 0
        for index in range(1, 9):
            # Ensuite vérifie que la page contient bien une fonction set_values()
            if self.is_fully_loaded[index - 1]:
                page_path = "initialisation/signals/page_rb/page_rb" + str(index) + ".py"

                # Ensuite vérifie que la page contient bien une fonction set_values()
                if "set_values" in dir(self.visible_pages[index - 1]):
                    try:
                        # Appelle la fonction get_values de la page et récupère une potentielle erreur sur la fonction
                        self.visible_pages[index - 1].set_values(data)
                        count += 1
                    except Exception as error:
                        # Permet de rattraper une autre potentielle erreur par sécurité (dû au exec())
                        logging.warning("Erreur inconnu lors du changement des donnés pour : " + page_path
                                        + "\n\t\tErreur de type : " + str(type(error))
                                        + "\n\t\tAvec comme message d\'erreur : " + error.args[0]
                                        + ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '\n\t\t')
                                        + "\n")
                else:
                    logging.warning("La page " + str(index) + "de paramètre : " + page_path + "n\'a pas set_values.\n")

        # Indique le nombre de pages dont les paramètres on été changés
        logging.info("Paramètres changés sur " + str(count) + " pages.\n")


