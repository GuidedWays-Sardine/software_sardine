# Librairies par défaut
import sys
import os
import traceback
import time


# Librairies graphiques
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow
from PyQt5.QtCore import Qt


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


class Simulation:
    """Classe utile à l'initialisation et au lancement de la simulation"""

    # Constante permettant de gérer le temps alloué à chaque tick (temps entre chaque mise à jour de tous les modules)
    DELAY = 0.250   # en s

    # Elements utiles à toutes les GUIs (fenêtres graphiques or ligne)
    app = None
    components = []
    parameters = {}
    running = True

    #Différentes bases de données utiles au fonctionnement du simulateur
    train_database = None
    line_database = None

    # Elément stockant la liste des fenêtre permettant d'éteindre les écrans en mode immersion
    black_screens = []

    def __init__(self, app, data):

        # Indique le début de l'initialisation de la simulation
        initial_time = time.time()
        log.change_log_prefix("initialisation simulation")
        log.info("Début de l'initialisation de la simulation.\n\n")

        # Initialise l'application
        self.app = app
        self.app.setQuitOnLastWindowClosed(True)
        self.parameters = data

        # Initialise les différents modules
        self.initialize()

        # Indique le temps de chargement de la simulation avant de lancer tous les modules
        middle_time = time.time()
        log.info("Simulation (" + str(len(self.components)) + " modules) initialisés en " +
                 str("{:.2f}".format((middle_time - initial_time) * 1000)) + " millisecondes.\n\n",
                 prefix="initialisation simulation")

        # Lance tous les modules (en appelant la fonction run) et vérifie qu'au moins un module a été chargé
        self.run()

        log.info("Lancements des modules de simulation en " +
                 str("{:.2f}".format((time.time() - middle_time) * 1000)) + " millisecondes.\n\t\t" +
                 "Simulation entièrement chargée (initialisation ° lancement) en " +
                 str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n",
                 prefix="initialisation simulation")

        self.app.exec()

    def initialize(self):
        # Initialise les fenêtre éteintes (Si elles le mode immersion a été activé)
        self.initialize_off_screens()

        # Initialisation des bases de données
        # FEATURE : initialiser la base de données train
        # FEATURE : initialiser la base de données ligne

        # A partir d'ici initialise tous les modules un par un sans les lancer
        # Ils seront tous lancés ensuite. Cela permet de tout faire apparaitre en même temps

        # Initialise le DMI
        self.launch_dmi()

        # FEATURE : lancer la partie graphique de la ligne (UE5 ou train caméra) de façon similaire au DMI
        # FEATURE : initialiser le PCC ici d'une façon similaire au DMI
        # FEATURE : initialiser les courbes d'une façon similaire mais simplifiée au DMI
        # FEATURE : initialiser le module dynamique du train similairement au DMI
        # FEATURE : initialiser l'EVC similairement au DMI

    def run(self):
        """Lance tous les modules initialisés.

        Raises
        ------
        AttributeError:
            Soulevée si un des modules n'a pas de fonction run() (Les autres modules ne seront pas lancés).
        ModuleNotFoundError:
            Soulevée dans le cas où aucun module n'a été initialisé.
        Exception
            Soulevée dans le cas où
        """
        # Si aucun module de simulation n'a été lancé
        if not self.components:
            raise ModuleNotFoundError("Aucun des modules n'a correctement été initialisé. Impossible de lancer la simulation.")

        # Montre les écrans d'immersion (si le mode a été désactivé, aucune fenêtre n'apparaitra
        self.run_off_screens()

        # Lance tous les modules en appelant la fonction run()
        for component in self.components:
            component.run()

    def initialise_dmi(self):
        """Fonction permettant d'initialiser le DMI.

        Raises
        ------
        ModuleNotFoundError
            soulevée lorsque la clé "dmi" n'est pas dans les paramètres et que le module est obligatoire pour la simulation.
        Exception
            soulevée lorsqu'une erreur se trouve dans la fonction d'initialisation du dmi.
        """
        try:
            # Importe le module du DMI, essaye de l'initialiser et l'ajouter aux "components" (modules) initialisés
            exec("import src.train.DMI." + str(self.parameters["dmi"]) + ".dmi as DMI\n" +
                 "self.components.append(DMI.DriverMachineInterface(self))")
        except KeyError:
            # Dans le cas où le DMI n'a pas été trouvé, crash si le dmi est obligatoire, laisse un message d'erreur sinon
            if self.parameters["sardine simulator.central dmi.mandatory"]:
                raise ModuleNotFoundError("Le paramètre \"dmi\" n'existe pas alors qu'il est obligatoire.\n")
            else:
                log.error("Impossible de charger le DMI, la paramètre \"dmi\" est introuvable. Aucun D%I ne sera chargé.\n")
        except Exception as error:
            # Dans le cas où l'initialisation contient une erreur, crash si le dmi est obligatoire sinon laisse un message d'erreur
            if self.parameters["sardine simulator.central dmi.mandatory"]:
                raise
            else:
                log.error("Impossible de charger le DMI : " + self.parameters["dmi"] + ". Aucun DMI ne sera chargé.\n\t\t" +
                          "Erreur de type : " + str(type(error)) + "\n\t\t" +
                          "Avec comme message d\'erreur : " + str(error.args) + "\n\n\t\t" +
                          "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                          prefix="initialisation simulation")

    def initialise_off_screens(self):
        """Permet d'initialiser toutes les fenêtres d'immersions (fenêtres noires en plein écran).
        Si le mode immersion est introuvable ou est désactivé, aucune fenêtre ne sera initialisée.
        """
        try:
            if self.parameters["immersion"]:
                # crée une liste d'exception. Celle-ci évitera d'éteindre les écrans contenant des modules indépendant
                # du python (tel que la ligne virtuelle sur UE5 ou le train caméra).
                exception_list = []

                # Vérifie pour chaque exception si elle existe et où elle se situe
                # FEATURE : indiquer ici les potentielles exceptions sur les fenêtre nécessitant une autre application
                try:
                    # Vérification pour la ligne virtuelle (sur UE5)
                    if self.parameters["sardine simulator.virtual line (ue5).screen_index"] != 0:
                        exception_list.append(self.parameters["sardine simulator.virtual line (ue5).screen_index"] - 1)
                except KeyError:
                    pass

                # Génère une fenêtre noire par écran n'étant pas dans la liste d'exceptions.
                for screen_index in (i for i in range(0, QDesktopWidget().screenCount()) if i not in exception_list):
                    sg = QDesktopWidget().screenGeometry(screen_index).getCoords()
                    self.black_screens.append(QMainWindow())
                    self.black_screens[screen_index].setWindowFlag(Qt.FramelessWindowHint)
                    self.black_screens[screen_index].setGeometry(sg[0], sg[1], sg[2] - sg[0] + 1, sg[3] - sg[1] + 1)
                    self.black_screens[screen_index].setStyleSheet("QMainWindow {background: 'black';}")
                    self.black_screens[screen_index].hide()
        except KeyError:
            log.debug("Pas de paramètres \"immersion\". Le mode immersion est désactivé par défaut.\n")

    def run_off_screens(self):
        """Fonction permettant de montrer toutes les fenêtres d'immersions (fenêtres noires en plein écran).
        Dans le cas où le mode immersion est désactivé ou qu'aucune fenêtre n'est à montrer, rien ne se produira.
        """
        for screen in self.black_screens:
            screen.show()
