# Librairies par défaut
import sys
import os
import threading
import time


# Librairies graphiques
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow
from PyQt5.QtCore import Qt


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary as sd
import src.misc.log as log
import src.misc.immersion as immersion


class Simulation:
    """Classe utile à l'initialisation et au lancement de la simulation"""

    # Constante permettant de gérer le temps alloué à chaque tick (temps entre chaque mise à jour de tous les modules)
    DELAY = 0.250   # en s

    # Elements utiles à toutes les GUIs (fenêtres graphiques hors ligne)
    components = {}
    parameters = {}
    running = True

    # Informations sur la mise à jour, utile surtout du point de vue pratique et debug
    update_count = 0
    update_average_time = 0     # s

    #Différentes bases de données utiles au fonctionnement du simulateur
    train_database = None
    line_database = None

    # Elément stockant la liste des fenêtre permettant d'éteindre les écrans en mode immersion
    black_screens = []

    def __init__(self, data):
        """Fonction de gestion de la simulation. S'occupe de l'initialisation, du lancemenet et de la mise à jour des
        différents modules de simulation.

        Parameters
        ----------
        data: `sd.SettingsDictionary`

        Raises
        ------
        ModuleNotFoundError
            Soulevée lorsque l'un des modules obligatoire n'a pas été correctement chargé ou lancé.
        Exception
            Soulevée lorsqu'une des fonctions d'initialisation, de lancement ou de mise à jour contient une erreur
        """
        # Indique le début de l'initialisation de la simulation
        initial_time = time.perf_counter()
        log.change_log_prefix("initialisation simulation")
        log.info("Début de l'initialisation de la simulation.\n\n")
        self.parameters = data

        # Change le mode d'immersion en mode chargement s'il est activé, sinon le désactive
        if "immersion" in self.parameters and self.parameters["immersion"]:
            # Récupère la liste des catégories/écrans de tous les écrans utilisant un logiciel externe
            # information stocké dans "category.window.extern"
            keys = (key.rsplit(".", 1)[-1] for key in list(self.parameters)
                    if key.endswith(".extern") and self.parameters[key])
            # récupère l'index de l'écran utilisé pour chacun des écrans externe si celui-ci est utilisé
            skip_list = (self.parameters[f"{key}.screen_index"] - 1 for key in keys
                         if f"{key}.screen_index" in self.parameters and self.parameters[f"{key}.screen_index"] != 0)

            # Change la skip_list et se met en mode loading
            immersion.change_skip_list(skip_list=tuple(skip_list),
                                       new_mode=immersion.Mode.LOADING)
        else:
            immersion.change_mode(immersion.Mode.DEACTIVATED)

        # Génère et stocke les différents BDD nécessaire à la simulation
        # FEATURE : initialiser la base de données train ici
        # FEATURE : initialiser la base de données ligne ici (à partir de l'identifiant ligne)

        # A partir d'ici initialise tous les modules un par un (ils seront lancées dans la fonction run())
        # FEATURE : appeler les différentes fonctions d'initialisation de modules
        self.initialise_dmi()  # Initialisation du DMI

        # Si aucun module de simulation n'a été lancé
        if not self.components:
            raise ModuleNotFoundError("Aucun des modules n'a correctement été initialisé. Impossible de lancer la simulation.")

        # Indique le temps de chargement de la simulation avant de lancer tous les modules
        log.change_log_prefix("initialisation simulation")
        log.info(f"Simulation ({len(self.components)} modules) initialisés en " +
                 f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.\n\n")

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
        initial_time = time.perf_counter()
        log.change_log_prefix("lancement simulation")
        log.info("Début du lancement de la simulation.\n\n")

        # Lance tous les modules en appelant la fonction run()
        # Chaque module doit avoir une fonction run() sinon la simulation ne se lance pas
        for module in self.components:
            self.components[module].run()

        # Si le mode immersion est activé, le change en mode STILL
        if "immersion" in self.parameters and self.parameters["immersion"]:
            immersion.change_mode(immersion.Mode.STILL)

        # Indique le temps de lancement de l'application (celui-ci doit être le plus court possible)
        log.info(f"Lancements des modules de simulation en " +
                 f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.\n")

        # Lance le thread pour mettre à jour constament la simulation et lance la partié graphique
        update = threading.Thread(target=self.update)
        update.start()
        QApplication.instance().exec()

        # Dans le cas où une fenêtre graphique est fermée par l'utilisateur, arrête la mise à jour de la simulation
        # et attend que celle-ci finisse de se réaliser, avant de sortir de la fonction run().
        self.running = False
        update.join()

    def update(self):
        # Tant que la simulation est lancée
        try:
            while self.running:
                # Récupère le temps du début de la mise à jour (à pure titre de debug)
                update_initial_time = time.perf_counter()

                # Mets à jour tous les modules dans un ordre logique
                # FEATURE appeler toutes les fonctions update des modules dans un ordre logique
                if "dmi" in self.components:
                    self.components["dmi"].update()

                # Récupère le temps nécessaire à la mise à jour
                update_time = time.perf_counter() - update_initial_time

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
                        log.debug(f"Attention mise à jour de l'application en {(update_time * 1000):.2f} millisecondes" +
                                  f"ms, au lieu des {(self.DELAY * 1000):.2f} millisecondes demandées.\n" +
                                  "\t\tPrévoir une optimisation du code ou un délai plus long si le soucis persiste.\n",
                                  prefix="simulation : update()")

        except Exception as error:
            # Dans le cas où un des modules de mise à jour a jeté une erreur, ferme l'application et rejette l'erreur
            QApplication.instance().quit()
            raise

    def stop(self):
        """Fonction de fermeture de la simulation, permet d'arrêter correctement la simulation"""
        # Indique le début de la fermeture de la simulation dans les logs
        initial_time = time.perf_counter()
        log.change_log_prefix("fermeture simulation")
        log.info("Fermeture de l'initialisation de la simulation.\n\n")

        # Change le mode immersion en mode fermeture si le mode immersion est activé
        if "immersion" in self.parameters and self.parameters["immersion"]:
            immersion.change_mode(immersion.Mode.UNLOADING)

        # Indique le nombre de mises à jours réussies et le temps moyen de mise à jour
        log.info(f"Simulation mises à jour {self.update_count} fois avec un temps moyen de {(self.update_average_time * 1000):.2f} millisecondes.\n")

        # Appelle les différentes fonctions de fermetures
        # FEATURE : ajouter les différents appels de fonctions de fermetures ici

        # Indique le temps nécessaire à la fermeture
        log.info(f"Simulation fermée correctement en : " +
                 f"{((time.perf_counter() - initial_time) * 1000):.2f} millisecondes.\n\n")

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
            exec(f"import src.train.DMI.{self.parameters['dmi']}.dmi as DMI\n" +
                 f"self.components[\"dmi\"] = DMI.DriverMachineInterface(self)")
        except KeyError:
            # Dans le cas où le DMI n'a pas été trouvé, crash si le dmi est obligatoire, laisse un message d'erreur sinon
            if self.parameters["sardine simulator.central dmi.mandatory"]:
                raise ModuleNotFoundError("Le paramètre \"dmi\" n'existe pas alors qu'il est obligatoire.\n")
            else:
                log.error("Impossible de charger le DMI, la paramètre \"dmi\" est introuvable. Aucun DMI ne sera chargé.\n")
        except Exception as error:
            # Dans le cas où l'initialisation contient une erreur, crash si le dmi est obligatoire sinon laisse un message d'erreur
            if self.parameters["sardine simulator.central dmi.mandatory"]:
                raise
            else:
                log.error(f"Impossible de charger le DMI : {self.parameters['dmi']}. Aucun DMI ne sera chargé.\n",
                          exception=error, prefix="initialisation simulation")
