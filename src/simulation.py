# Librairies par défaut
import sys
import os
import threading
import traceback
import time


# Librairies graphiques
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow
from PyQt5.QtCore import Qt


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary.settings as sd
import src.misc.log.log as log


class Simulation:
    """Classe utile à l'initialisation et au lancement de la simulation"""

    # Constante permettant de gérer le temps alloué à chaque tick (temps entre chaque mise à jour de tous les modules)
    DELAY = 0.250   # en s

    # Elements utiles à toutes les GUIs (fenêtres graphiques or ligne)
    app = None
    components = {}
    parameters = {}
    running = True

    # Informations sur la mise à jour, utile surtout du point de vue pratique et debug
    update_count = 0
    update_average_time = 0

    #Différentes bases de données utiles au fonctionnement du simulateur
    train_database = None
    line_database = None

    # Elément stockant la liste des fenêtre permettant d'éteindre les écrans en mode immersion
    black_screens = []

    def __init__(self, app, data):
        """Fonction de gestion de la simulation. S'occupe de l'initialisation, du lancemenet et de la mise à jour des
        différents modules de simulation.

        Parameters
        ----------
        app: `QApplication`
            L'application sur laquelle les modules graphiques de la simulation vont se lancer
        data: `sd.SettingsDictionnary`

        Raises
        ------
        ModuleNotFoundError
            Soulevée lorsque l'un des modules obligatoire n'a pas été correctement chargé ou lancé.
        Exception
            Soulevée lorsqu'une des fonctions d'initialisation, de lancement ou de mise à jour contient une erreur
        """
        # Indique le début de l'initialisation de la simulation
        initial_time = time.time()
        log.change_log_prefix("initialisation simulation")
        log.info("Début de l'initialisation de la simulation.\n\n")

        # Stocke les différents paramètres utiles à l'application
        self.app = app
        self.parameters = data
        # FEATURE : initialiser la base de données train ici
        # FEATURE : initialiser la base de données ligne ici (à partir de l'identifiant ligne)

        # Initialise les fenêtre éteintes (Si elles le mode immersion a été activé)
        self.initialise_off_screens()

        # A partir d'ici initialise tous les modules un par un (ils seront lancées dans la fonction run())
        # FEATURE : appeler les différentes fonctions d'initialisation de modules ici
        self.initialise_dmi()  # Initialisation du DMI

        # Si aucun module de simulation n'a été lancé
        if not self.components:
            raise ModuleNotFoundError("Aucun des modules n'a correctement été initialisé. Impossible de lancer la simulation.")

        # Indique le temps de chargement de la simulation avant de lancer tous les modules
        log.change_log_prefix("initialisation simulation")
        log.info("Simulation (" + str(len(self.components)) + " modules) initialisés en " +
                 str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n")

    def run(self):
        """Lance tous les modules initialisés.

        Raises
        ------
        AttributeError:
            Soulevée si un des modules n'a pas de fonction run() (Les autres modules ne seront pas lancés).
        Exception
            Soulevée dans le cas où la fonction run() d'un des modules contient une erreur
        """
        # Indique le début de l'initialisation de la simulation
        initial_time = time.time()
        log.change_log_prefix("lancement simulation")
        log.info("Début du lancement de la simulation.\n\n")

        # Montre les écrans d'immersion (si le mode a été désactivé, aucune fenêtre n'apparaitra
        self.run_off_screens()

        # Lance tous les modules en appelant la fonction run()
        for component in self.components:
            component.run()

        # Indique le temps de lancement de l'application (celui-ci doit être le plus court possible)
        log.info("Lancements des modules de simulation en " +
                 str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\t\t")

        # Lance le thread pour mettre à jour constament la simulation et lance la partié graphique
        update = threading.Thread(target=self.update)
        update.start()
        self.app.exec()

        # Dans le cas où une fenêtre graphique est fermée par l'utilisateur, arrête la mise à jour de la simulation
        # et attend que celle-ci finisse de se réaliser, avant de sortir de la fonction run().
        self.running = False
        update.join()

    def update(self):
        # Tant que la simulation est lancée
        try:
            while self.running:
                # Récupère le temps du début de la mise à jour (à pure titre de debug)
                update_initial_time = time.time()

                # Mets à jour tous les modules dans un ordre logique
                # FEATURE appeler toutes les fonctions update des modules dans un ordre logique

                if "dmi" in self.components:
                    self.components["dmi"].update()

                # Récupère le temps nécessaire à la mise à jour
                update_time = time.time() - update_initial_time

                # Mets à jour le tempos moyen des mises à jours ainsi que le nombre de mises à jours réussies
                self.update_average_time = (self.update_average_time * self.update_count + update_time) / (self.update_count + 1)
                self.update_count += 1

                # Dans le cas où un délai a été ajouté
                if self.DELAY != 0:
                    # Vérifie si la mise à jour a pris moins de temps que le délai souhaité
                    if self.DELAY - update_time >= 0:
                        # Si c'est le cas, attend le temps nécessaire
                        time.sleep(self.DELAY - update_time)
                    else:
                        # Sinon laisse un message de debug pour inciter à l'optimisation du code ou au changement du délai
                        log.debug("Attention mise à jour de l'application en " + "{:.2f}".format(update_time * 1000) +
                                  "ms, au lieu des " + "{:.2f}".format(self.DELAY * 1000) + "ms demandés.\n\t\t" +
                                  "Prévoir une optimisation du code ou un délai plus long si le soucis persiste.\n",
                                  prefix="simulation : update()")

        except Exception as error:
            # Dans le cas où un des modules de mise à jour à jeté une erreur, ferme l'application et rejette l'erreur
            self.app.quit()
            raise

    def stop(self):
        """Fonction de fermeture de la simulation, permet d'arrêter correctement la simulation"""
        # Indique le début de la fermeture de la simulation dans les logs
        initial_time = time.time()
        log.change_log_prefix()
        log.info("Fermeture de l'initialisation de la simulation.\n\n",
                 prefix="fermeture simulation")

        # Appelle les différentes fonctions de fermetures
        # FEATURE : ajouter les différents appels de fonctions de fermetures ici

        # Indique le temps nécessaire à la fermeture
        log.info("Simulation (" + str(len(self.components)) + " modules) initialisés en " +
                 str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n",
                 prefix="fermeture simulation")

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
                 "self.components[\"dmi\"] = DMI.DriverMachineInterface(self)")
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
