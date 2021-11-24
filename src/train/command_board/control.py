import os
import sys
import traceback
import threading
import time
from enum import Enum, unique


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.train.command_board.functions as func
import src.train.train_database.database as tdb


@unique
class Actions(Enum):
    """Enum contenant toutes les actions possibles par le pupitre"""
    # FEATURE : ajouter les différentes actions en suivant la structure NOM_ACTION = (func.fonction,) relié à functions.py
    LEVER_PANTHO = (func.lever_panto,)
    MANIP_DE_TRACTION = (func.manip_de_traction,)

    # Fonction permettant de facilement appeler la fonction associée à la valeur de l'Enum
    def __call__(self, *args, **kwargs):
        self.value[0](*args, **kwargs)


class Control:
    """Classe contenant la logique générale du pupitre"""
    # Delai de lecture des valeurs des boutons (volontairement différent de simulation.DELAY pour une lecture plus précise)
    DELAY = 0.02     # En secondes

    # Informations sur la mise à jour, utile surtout du point de vue pratique et debug
    update_count = 0
    update_average_time = 0

    # Cadenas pour éviter les data races (Un thread qui lit sur le pupitre et ajoute les commandes et un autre)
    lock = threading.Lock()

    # Liste des actions à réaliser
    actions_list = []

    def __init__(self, app):
        """Initialisation  du pupitre du pupitre de commandes

        Parameters
        __________
        app: `QApplication`
            L'application sur laquelle les modules graphiques de la simulation vont se lancer
        """
        # Commence par initialiser les boutons du pupitre
        self.initialise_physical_buttons()

        # Puis initialise les boutons
        self.initialise_virtual_buttons(app)

    def run(self):
        """Fonction permettant de lancer le pupitre ainsi que la boucle de lecture"""
        # Commence par lancer la partie physique et virtuelle du pupitre
        self.launch_physical_buttons()
        self.launch_virtual_buttons()

        # Lance le thread avec la fonction permettant de lire les états des boutons en boucles
        reading_loop = threading.Thread(target=self.loop, daemon=True)
        reading_loop.start()

    def loop(self):
        """Fonction appelé sur un thread permettant de lire les valeurs en boucle
        (Cette fonction gère uniquement la logique. La fonction à surcharger est self.get_buttons_state)"""
        while True:
           # Récupère le temps de début de la lecture des boutons
            update_initial_time = time.time()

            # Lecture des états des boutons et ajouts des commandes si nécessaire
            self.get_buttons_state()

            # Récupère le temps nécessaire à la lecture de toutes les états des boutons
            update_time = time.time() - update_initial_time

            # Mets à jour le tempos moyen des mises à jours ainsi que le nombre de mises à jours réussies
            self.update_average_time = (self.update_average_time * self.update_count + update_time) / (self.update_count + 1)
            self.update_count += 1

            # Dans le cas où un délai a été ajouté pour la lecture des valeurs du pupitre
            if self.DELAY != 0:
                # Vérifie si la mise à jour a pris moins de temps que le délai souhaité
                if self.DELAY - update_time >= 0:
                    # Si c'est le cas, attend le temps nécessaire
                    time.sleep(self.DELAY - update_time)
                else:
                    # Sinon laisse un message de debug pour inciter à l'optimisation du code ou au changement du délai
                    log.debug("Attention lecture des états des boutons du pupitre en " + "{:.2f}".format(update_time * 1000) +
                              "ms, au lieu des " + "{:.2f}".format(self.DELAY * 1000) + "ms demandés.\n\t\t" +
                              "Prévoir une optimisation du code ou un délai plus long si le soucis persiste.\n",
                              prefix="pupitre : loop()")

    def update(self, database):
        """Fonction qui à partir de la liste des actions execute toutes les actions associées

        Parameters
        ----------
        database:  `tdb.TrainDatabase`
            Base de données train dont il faut modifier les informations
        """
        # Bloque le thread afin d'éviter les data races
        with self.lock:
            # Commence par ajouter les valeurs nécessaires (position du manip de traction, ...) à la liste d'actions
            self.read_specific_values()

            # Pour chacune des actions dans la liste d'action à éxecuter, essaye de l'executer, sinon laise une erreur
            for action in self.actions_list:
                try:
                    exec(str(action[0]) + "(database," + str(*action[1::]) + ")")
                except Exception as error:
                    log.error("Erreur fatale lors du fonctionnement du simulateur\n\t\t" +
                              "Erreur de type : " + str(type(error)) + "\n\t\t" +
                              "Avec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                              "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                              prefix="pupitre: update()")
                finally:
                    # Dans tous les cas supprime l'action
                    del self.actions_list[0]

    def stop(self):
        """Fonction appelée lors de la fermeture du programme"""
        # Indique le nombre de lectures du pupitre et le temps moyen de lecture
        log.info("Valeurs du pupitre lu " + str(self.update_count) + " avec un temps moyen de " + str(self.update_average_time) + ".\n",
                 prefix="fermeture pupitre")

    # FEATURE : Liste de toutes les fonctions surchargeables

    # Fonction (à surcharger) permettant d'initialiser la liste de tous les boutons réels sur le pupitre
    def initialise_physical_buttons(self):
        """Fonction permettant d'initialiser tous les boutons physiques du pupitre"""
        pass

    # Fonction (potentiellement à surcharger) permettant d'initialiser la fenêtre avec les boutons virtuels
    def initialise_virtual_buttons(self, app):
        """Fonction permettant d'initialiser la fenêtre avec les boutons virtuels

        Parameters
        ----------
        app: `QApplication`
            L'application sur laquelle les modules graphiques de la simulation vont se lancer
        """
        pass

    # Fonction (potentiellement à surcharger) permettant de lancer le pupitre (Dans le cas où des vérifications
    # supplémentaires sont nécessaires
    def launch_physical_buttons(self):
        """Fonction permettant de lancer le pupitre (Cette fonction ne s'occupe pas de la lecture des valeurs)"""
        pass

    # Fonction (potentiellement à surcharger) pour rendre visible la fenêtre avec tous les boutons virtuels
    def launch_virtual_buttons(self):
        """Fonction permettant de rendre visible la fenêtre contenant tous les boutons virtuels si elle existe"""
        pass

    # Fonction (à surcharger) permettant de lire les états des différents boutons en boucles
    def get_buttons_state(self):
        """Fonction permettant de lire en boucle les états des différents éléments du pupitre"""
        pass

    # Fonction (à surchager) permettant de lire les valeurs analogiques (position manip de traction...)
    def read_specific_values(self):
        """Fonction permettant de récupérer les valeurs ne nécessitant pas une lecture en continu"""
        pass
