import os
import sys
import traceback
import threading
import time
from enum import Enum, unique


# Librairies pour la commande des pupitres
import serial.tools.list_ports
import pyfirmata
from pyfirmata import util


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd
import src.train.command_board.functions as func
import src.train.train_database.database as tdb
import src.train.command_board.buttons_definitions as bd


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
    DELAY = 0.015     # En secondes (Attention par palier de 0.015s)

    # Informations sur la mise à jour, utile surtout du point de vue pratique et debug
    update_count = 0
    update_average_time = 0

    # Cadenas pour éviter les data races (Un thread qui lit sur le pupitre et ajoute les commandes et un autre)
    lock = threading.Lock()

    # Liste des éléments nécessaires au fonctionnement du pupitre
    board = None
    continuous_buttons = []
    update_buttons = []

    # Liste des actions à réaliser
    actions_list = []

    def __init__(self, command_board_settings, app=None):
        """Initialisation  du pupitre du pupitre de commandes

        Parameters
        __________
        command_board_settings: `sd.SettingsDictionary`
            dictionnaire de paramètres pupitres. Permet de connecter tous les éléments à leurs fonctions
        app: `QApplication`
            L'application sur laquelle les modules graphiques de la simulation vont se lancer

        Raises
        ------
        KeyError
            Jeté si certains arguments vitaux (tel que le type de carte électronique) ne sont pas présents
        PermissionError
            Jeté s'il est impossible pour le pupitre de se connecter à la carte électronique de gestion de celle-ci
        """
        initial_time = time.perf_counter()

        # Commence par initialiser l'arduino
        self.initialise_board(command_board_settings)

        # Continue en initialisant les différents boutons physiques connecté à l'arduino
        self.initialise_physical_buttons(command_board_settings)

        # Puis initialise les boutons
        self.initialise_virtual_buttons(app)

        thread = util.Iterator(self.board)
        thread.start()

        log.info(f"Chargement du module pupitre ({command_board_settings.get_value('command_board', ' ')}) en " +
                 f"{(time.perf_counter() - initial_time) * 1000:.2f} millisecondes.")

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
                    action[0](database, *action[1:])
                    # exec(str(action[0]) + "(database," + str(*action[1::]) + ")")
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

    # Fonction (surchargeable) permettant d'initialiser la carte électronique utilisée pour le pupitre
    def initialise_board(self, command_board_settings):
        """Fonction permettant d'initialiser la carte éléctronique utilisée pour le pupitre

        Parameters
        ----------
        command_board_settings: `sd.SettingsDictionary`
            dictionnaire de paramètres pupitres. Permet de connecter tous les éléments à leurs fonctions

        Raises
        ------
        KeyError
            Jeté si certains arguments vitaux (tel que le type de carte électronique) ne sont pas présents
        PermissionError
            Jeté s'il est impossible pour le pupitre de se connecter à la carte électronique de gestion de celle-ci
        """
        # Récupère tous les ports où l'Arduino peut être connecté
        ports = serial.tools.list_ports.comports()
        if command_board_settings["board.type"] in ["Arduino", "ArduinoDue", "ArduinoMega", "ArduinoNano"]:
            # Dans le cas où c'est une carte par défaut, essaye d'initialiser jusqu'à ce qu'un des ports se connecte
            for port in ports:
                if self.board is None:
                    try:
                        # Essaye d'initialiser l'arduino
                        exec(f"self.board = pyfirmata.{command_board_settings['board']}({port.device})")
                        log.info(f"Connexion à la carte électronique : {port.name} sur le port : {port.device}.")
                        # Cas où c'est une borne déjà présent par défaut:
                    except Exception as error:
                        # Si ça rate, passe au port suivant
                        log.error("", exception=error)
                        pass
        else:
            # Dans le cas où ce n'est pas une carte par défaut, initialise une carte grâce à l'initialisation Board
            digital_pins = command_board_settings["board.digital_pins"]    # Considère digital et analog comme important
            analog_pins = command_board_settings["board.analog_pins"]
            pwm_pins = command_board_settings.get_value("board.pwm_pins", ())
            disabled_pins = command_board_settings.get_value("board.disabled_pins", ())

            # Essaye d'initialiser jusqu'à ce qu'un des ports se connecte
            for port in ports:
                if self.board is None:
                    try:
                        # Essaye d'initialiser la carte avec les arguments récupérés du fichier de paramètres
                        self.board = pyfirmata.Board(port.device, {"digital": digital_pins,
                                                                   "analog": analog_pins,
                                                                   "pwm": pwm_pins,
                                                                   "use_ports": True,
                                                                   "disabled": disabled_pins})
                        log.info(f"Connexion à la carte électronique : {port.name} sur le port : {port.device}.")
                    except Exception as error:
                        log.error("", exception=error)
                        pass

        # Si la carte électronique n'a toujours pas été chargée
        if self.board is None:
            raise PermissionError("Impossible de se connecter a une carte électronique. " +
                                  "Assurez vous qu'elle est connectée et n'est pas utilisée par un autre logiciel.")

    # Fonction (surchargeable) permettant d'initialiser la liste de tous les boutons réels sur le pupitre
    def initialise_physical_buttons(self, command_board_settings):
        """Fonction permettant d'initialiser la carte éléctronique utilisée pour le pupitre

        Parameters
        ----------
        command_board_settings: `sd.SettingsDictionary`
            dictionnaire de paramètres pupitres. Permet de connecter tous les éléments à leurs fonctions
        """
        # Essaye
        button_index = 1
        # Essaye de charger des boutons jusqu'à ce que l'index soit trop grand et qu'il n'y en ait plus
        while f"button{button_index}.type" in command_board_settings:
            try:
                # Commence par charger toutes les fonctions relié au bouton
                function_index = 1
                functions = {}      # Dictionnaire {[état pins] : fonction, ...}
                while f"button{button_index}.function{function_index}.values" in command_board_settings\
                        and f"button{button_index}.function{function_index}.function" in command_board_settings:
                    try:
                        functions[command_board_settings[f"button{button_index}.function{function_index}.values"]] = \
                            Actions[command_board_settings[f"button{button_index}.function{function_index}.function"][8:]]
                    except Exception as error:
                        log.debug(f"Erreur lors du chargement d'une des fonctions pupitre",
                                  exception=error, prefix=f"button{button_index}.function{function_index}")
                    function_index += 1

                type = command_board_settings.get_value(f"button{button_index}.type", "")
                # S'occupe maintenant de charger les informations générales sur le bouton
                if type == "PushButton":
                    # Récupère les actions quand pressé et non pressé
                    action_released = functions[False] if False in functions else None
                    action_pressed = functions[True] if True in functions else None
                    bd.PushButton(self.board, command_board_settings[f"button{button_index}.pins"][0], None,    # TODO : rajouter compatibilité avec LED
                                  action_up=action_released, action_down=action_pressed)
                elif type == "Potentiometer":
                    pass # TODO : introduire la composante
                elif type == "SwitchButton":
                    # Pour les PushButton aucun traitement n'est nécessaire
                    if command_board_settings.get_value(f"button{button_index}.read_mode", "").lower() == "update":
                        self.update_buttons.append(bd.SwitchButton(self.board, command_board_settings[f"button{button_index}.pins"], functions))
                    else:
                        self.continuous_buttons.append(bd.SwitchButton(self.board, command_board_settings[f"button{button_index}.pins"], functions))
            except Exception as error:
                log.debug(f"Erreur lors du chargement d'un des boutons du pupitre",
                          exception=error, prefix=f"button{button_index}")

            button_index += 1

        log.info(f"{len(self.continuous_buttons) + len(self.update_buttons)} connectés au pupitre")


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
        for button in self.continuous_buttons:
            button.verify_value(self.actions_list)

    # Fonction (à surchager) permettant de lire les valeurs analogiques (position manip de traction...)
    def read_specific_values(self):
        """Fonction permettant de récupérer les valeurs ne nécessitant pas une lecture en continu"""
        for button in self.update_buttons:
            button.add_action(self.actions_list)
