import os.path
import sys
import logging
import traceback

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
        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)
        self.engine = QQmlApplicationEngine()
        self.engine.load('initialisation/initialisation_window.qml')

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile('initialisation/initialisation_window.qml'):
            raise FileNotFoundError('Le fichier .qml pour la fenêtre d\'initialisation n\'a pas été trouvé')
        elif not self.engine.rootObjects() and os.path.isfile('initialisation/initialisation_window.qml'):
            raise SyntaxError('Le fichier .qml pour la fenêtre d\'initialisation contient des erreurs.')

        # Si le fichier qml a été compris, récupère la fenêtre et initialise les différents boutons et pages
        self.win = self.engine.rootObjects()[0]
        self.bottom_buttons = bb.BottomButtons(self)
        self.right_buttons = rb.RightButtons(self)

        # Lance l'application
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
            if self.right_buttons.is_fully_loaded[index - 1]:
                page_path = "initialisation/signals/page_rb/page_rb" + str(index) + ".py"
                try:
                    # Import localement le fichier de la page
                    # Appelle la fonction get_values()
                    exec("from initialisation.signals.page_rb import page_rb" + str(index) + "\n"
                         + "parameters.update(" +
                         "self.right_buttons.is_signals_loaded[" + str(index - 1) + "].get_values())")
                except AttributeError as error:
                    # Erreur appelée si jamais la page n'a pas de fonction get_values()
                    logging.warning("La page : " + page_path + "n\'a pas de fonction get_values()"
                                    + "\n\t\t Assurez-vous que la fonction est implémentée"
                                    + "\n\t\t Les paramêtres d la page ne seront pas pris en comptre\n")
                except Exception as error:
                    # Permet de rattraper une autre potentielle erreur par sécurité (dû au exec())
                    logging.warning("Erreur inconnu lors de la récupération des donnés " + page_path
                                    + "\n\t\tErreur de type : " + str(type(error))
                                    + "\n\t\tAvec comme message d\'erreur : " + error.args[0]
                                    + ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '\n\t\t') + "\n")

        # Retourne le dictionnaire complété grâce aux différentes valeurs des get_values() de chaques pages
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
        for index in range(1, 9):
            # Vérifie d'abord si la page a des signals handlers (et donc potentiellement des valeurs à récupérer)
            if self.right_buttons.is_fully_loaded[index - 1]:
                page_path = "initialisation/signals/page_rb/page_rb" + str(index) + ".py"
                try:
                    # Import localement le fichier de la page
                    # Appelle la fonction set_values()
                    exec("from initialisation.signals.page_rb import page_rb" + str(index) + "\n"
                         + "self.right_buttons.is_signals_loaded[" + str(index - 1) + "].set_values(data)")
                except AttributeError as error:
                    # Erreur appelée si jamais la page n'a pas de fonction get_values()
                    logging.warning("La page : " + page_path + "n\'a pas de fonction set_values()"
                                    + "\n\t\t Assurez-vous que la fonction est implémentée"
                                    + "\n\t\t Les paramêtres de la page ne seront pas pris en comptre\n")
                except Exception as error:
                    # Permet de rattraper une autre potentielle erreur par sécurité (dû au exec())
                    logging.warning("Erreur inconnu lors de du changement des donnés sur " + page_path
                                    + "\n\t\tErreur de type : " + str(type(error))
                                    + "\n\t\tAvec comme message d\'erreur : " + error.args[0]
                                    + ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '\n\t\t') + "\n")
