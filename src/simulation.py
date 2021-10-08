import logging
import os
import sys
import traceback
import time

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

import log.log as log


class Simulation:
    """Classe utile à l'initialisation et au lancement de la simulation"""

    # Elements utiles à toutes les GUIs (fenêtres graphiques or ligne)
    app = None
    components = []

    def __init__(self, data):

        # Indique le début de l'initialisation de la simulation
        log.change_log_prefix("[initialisation simulation]")
        initial_time = time.time()
        logging.info("Début de l'initialisation de la simulation.\n\n")

        # Initialise l'application
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)

        # A partir d'ici initialise tous les modules un par un sans les lancer
        # Ils seront tous lancés ensuite. Cela permet de tout faire apparaitre en même temps

        # Initialise le DMI
        try:
            exec("import DMI." + data["DMI"] + ".driver_machine_interface as DMI\n" +
                 "self.components.append(DMI.DriverMachineInterface(self, data))")
        except KeyError:
            # Dans le cas où aucun DMI n'a été sélectionné, essaye de charger le DMI ETCS
            logging.info("Pas de DMI récupéré. Tentative de chargement du DMI ETCS.")
            try:
                exec("import DMI.ETCS.driver_machine_interface as DMI\n" +
                     "self.components.append(DMI.DriverMachineInterface(self, data))")
            except Exception as error:
                # Si même le DMI ETCS ne peut pas se charger, ne charge aucun DMI
                log.change_log_prefix("[initialisation simulation]")
                logging.error("Impossible de charger le DMI : ETCS (mode secours). Aucun DMI ne sera chargé.\n\t\t" +
                              'Erreur de type : ' + str(type(error)) + '\n\t\t' +
                              'Avec comme message d\'erreur : ' + str(error.args) + '\n\n\t\t' +
                              ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '\n\t\t') + "\n")
        except Exception as error:
            # Si une erreur est survenur lors du chargement du DMI, ne charge pas de DMI
            log.change_log_prefix("[initialisation simulation]")
            print(data["DMI"])
            logging.error("Impossible de charger le DMI : " + data["DMI"] + ". Aucun DMI ne sera chargé.\n\t\t" +
                          'Erreur de type : ' + str(type(error)) + '\n\t\t' +
                          'Avec comme message d\'erreur : ' + str(error.args) + '\n\n\t\t' +
                          ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '\n\t\t') + "\n")

        # FEATURE : initialiser le PCC ici d'une façon similaire au DMI
        # FEATURE : initialiser les courbes d'une façon similaire mais simplifiée au DMI
        # FEATURE : lancer la partie ligne (et mettre any_launched a true si bien lancé)

        # Indique le temps de chargement de la simulation avant de lancer tous les modules
        log.change_log_prefix("[initialisation simulation]")
        logging.info("Simulation (" + str(len(self.components)) + " modules) chargée en " +
                     str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n")

        # Lance tous les modules (en appelant la fonction run) et vérifie qu'au moins un module a été chargé
        any_launched = False
        for component in self.components:
            if "run" in dir(component):
                component.run()
                any_launched = True
            else:
                logging.error("Impossible d'éxécuter le module : " + type(component) + " qui n'a pas de fonction run().\n")

        # FEATURE : lancer la boucle de dynamique du train

        # Vérifie qu'au moins un module graphique c'est lancé
        if not any_launched:
            raise ModuleNotFoundError("Aucun des modules de simulations n'a pu être chargé correctement.\n\n")

        self.app.exec()
