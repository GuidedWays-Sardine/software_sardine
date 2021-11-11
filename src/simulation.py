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

        # A partir d'ici initialise tous les modules un par un sans les lancer
        # Ils seront tous lancés ensuite. Cela permet de tout faire apparaitre en même temps

        # Initialise le DMI
        try:
            exec("import src.train.DMI." + data["dmi"] + ".dmi as DMI\n" +
                 "self.components.append(DMI.DriverMachineInterface(self, data))")
        except KeyError:
            # Dans le cas où aucun DMI n'a été sélectionné, essaye de charger le DMI ETCS
            log.info("Pas de DMI récupéré. Tentative de chargement du DMI ETCS.", prefix="chargement DMI")              # FIXME : charger le DMI ETCS si l'autre DMI n'est pas trouvé ?
            try:
                exec("import src.train.DMI.ETCS.dmi as DMI\n" +
                     "self.components.append(DMI.DriverMachineInterface(self, data))")
            except Exception as error:
                # Si même le DMI ETCS ne peut pas se charger, ne charge aucun DMI
                log.error("Impossible de charger le DMI : ETCS (mode secours). Aucun DMI ne sera chargé.\n\t\t" +
                          "Erreur de type : " + str(type(error)) + "\n\t\t" +
                          "Avec comme message d\'erreur : " + str(error.args) + "\n\n\t\t" +
                          "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                          prefix="initialisation simulation")
        except Exception as error:
            # Si une erreur est survenur lors du chargement du DMI, ne charge pas de DMI
            log.error("Impossible de charger le DMI : " + data["dmi"] + ". Aucun DMI ne sera chargé.\n\t\t" +
                      "Erreur de type : " + str(type(error)) + "\n\t\t" +
                      "Avec comme message d\'erreur : " + str(error.args) + "\n\n\t\t" +
                      "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                      prefix="initialisation simulation")

        # FEATURE : initialiser le PCC ici d'une façon similaire au DMI
        # FEATURE : initialiser les courbes d'une façon similaire mais simplifiée au DMI
        # FEATURE : lancer la partie ligne (et mettre any_launched a true si bien lancé)

        # Indique le temps de chargement de la simulation avant de lancer tous les modules
        log.info("Simulation (" + str(len(self.components)) + " modules) chargée en " +
                 str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n",
                 prefix="initialisation simulation")

        # Montre les écrans d'immersion (si le mode a été désactivé, aucune fenêtre n'apparaitra
        self.run_off_screens()

        any_launched = False
        for component in self.components:
            if "run" in dir(component):
                component.run()
                any_launched = True
            else:
                log.error("Impossible d'éxécuter le module : " + type(component) + " qui n'a pas de fonction run().\n")

        # FEATURE : lancer la boucle de dynamique du train sur un thread
        # FEATURE : lancer la bboucle de l'EVC (ETCS) sur un thread

        # Vérifie qu'au moins un module graphique c'est lancé
        if not any_launched:
            raise ModuleNotFoundError("Aucun des modules de simulations n'a pu être chargé correctement.\n\n")

    def initialize_off_screens(self):
        try:
            if self.parameters["immersion"]:
                # Récupère les potentiels indexs des écrans à ne pas éteindre (dû à un logiciel tierce utilisé)
                # FEATURE : indiquer ici les potentielles exceptions sur les fenêtre nécessitant une autre application
                exception_list = []
                # Vérification pour le module de la ligne virtuelle (sur Unreal Engine 5)
                try:
                    if self.parameters["sardine simulator.virtual line (ue5).screen_index"] != 0:
                        exception_list.append(self.parameters["sardine simulator.virtual line (ue5).screen_index"] - 1)
                except KeyError:
                    pass

                # Génère toutes les fenêtres noir pour le mode immersion
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
        for screen in self.black_screens:
            screen.show()
