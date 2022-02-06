import os
import sys
import traceback
import threading
import time


# Librairies pour la commande des pupitres
import serial.tools.list_ports
import pyfirmata
from pyfirmata import util


# Librairies graphiques
from PyQt5.QtWidgets import QApplication


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd
import src.train.train_database.database as tdb
import src.train.command_board.Generic.actions.actions as actions
import src.train.command_board.Generic.default_components.components as components


class Control:
    """Classe contenant la logique générale des pupitres utilisant des cartes électroniques"""
    # Delai de lecture des valeurs des boutons (volontairement différent de simulation.DELAY pour une lecture plus précise)
    DELAY = 0.015     # En secondes (Attention par palier de 0.015s)

    # Informations sur la mise à jour, utile surtout du point de vue pratique et debug
    update_count = 0
    update_average_time = 0

    # Cadenas pour éviter les settings races (Un thread qui ajoute les commandes et un autre qui les execute)
    lock = threading.Lock()

    # Liste des éléments nécessaires au fonctionnement du pupitre physique
    board = None
    board_name = ""
    reading_thread = None
    continuous_components = []     # boutons ; lever panto ; BP Urge...
    update_components = []         # manipulateur de tracion
    output_components = []         # LEDs ; acquitement ; inverseur

    # Stockage d'un lien vers la base de données train pour modifier les informations
    train_database = None

    # Elements nécessaires au fonctionnement de la partie virtuelle du pupitre
    virtual_command_board = None

    # Liste des actions à réaliser
    actions_list = []

    def __init__(self, train_database, settings, command_board_settings, app=None):
        """Initialisation  du pupitre du pupitre de commandes

        Parameters
        __________
        train_database : `tdb.TrainDatabase` TODO : trouver le vrai type de la base de données train
            lien vers la base de données train dans laquelle toutes les données seront stockées
        settings: `sd.SettingsDictionary`
            dictionnaire de paramètres simulation. Utile nottament pour les boutons virtuels
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

        # Puis initialise les boutons virtuels
        self.initialise_virtual_buttons(app, settings, command_board_settings)

        log.info(f"Chargement du module pupitre ({command_board_settings.get_value('command_board', ' ')}) en " +
                 f"{(time.perf_counter() - initial_time) * 1000:.2f} millisecondes.")

    def run(self):
        """Fonction permettant de lancer le pupitre ainsi que la boucle de lecture"""
        # Commence par lancer la partie physique et virtuelle du pupitre
        with self.lock:
            self.launch_physical_buttons()
            self.launch_virtual_buttons()

        # Lance le thread avec la fonction permettant de lire les états des boutons en boucles
        reading_loop = threading.Thread(target=self.loop, daemon=True)
        reading_loop.start()

    def loop(self):
        """Fonction appelé sur un thread permettant de lire les valeurs en boucle
        (Cette fonction gère uniquement la logique. La fonction à surcharger est self.vérify_continuous)"""
        while True:
            # Récupère le temps de début de la lecture des boutons
            update_initial_time = time.perf_counter()

            # Lecture des états des boutons et ajouts des commandes si nécessaire
            with self.lock:
                self.vérify_continuous()

            # Récupère le temps nécessaire à la lecture de toutes les états des boutons
            update_time = time.perf_counter() - update_initial_time

            # Mets à jour le tempos moyen des mises à jours ainsi que le nombre de mises à jours réussies
            self.update_average_time = (self.update_average_time * self.update_count + update_time) / (self.update_count + 1)
            self.update_count += 1

            # Dors le bon temps si nécessaire, sinon dort 1ms
            time.sleep(self.DELAY - update_time if update_time < self.DELAY else 0.001)

    def update(self):
        """Fonction qui à partir de la liste des actions execute toutes les actions associées"""
        # Bloque le thread afin d'éviter les settings races
        with self.lock:
            # Commence par ajouter les valeurs nécessaires (pour les entrées variables et les sorties
            self.prepend_update()
            self.append_outputs()

            # Pour chacune des actions dans la liste d'action à éxecuter, essaye de l'executer, sinon laise une erreur
            for action in list(self.actions_list):  # list() VITAL POUR CREER UNE COPIE ET EVITER LES ERREURS ITERATION
                try:
                    action[0](self.train_database, *action[1:])
                except Exception as error:
                    log.warning(f"Erreur lors de l'execution de la command pupitre {action[0]}",
                                exception=error)
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
                        pass

        # Si la carte électronique n'a toujours pas été chargée
        if self.board is None:
            raise PermissionError("Impossible de se connecter a une carte électronique. " +
                                  "Assurez vous qu'elle est connectée et n'est pas utilisée par un autre logiciel.")

        # Génère et démarre le thread qui lit les valeurs
        self.reading_thread = util.Iterator(self.board)
        self.reading_thread.start()

    # Fonction (surchargeable) permettant d'initialiser la liste de tous les boutons réels sur le pupitre
    def initialise_physical_buttons(self, command_board_settings):
        """Fonction permettant d'initialiser la carte éléctronique utilisée pour le pupitre

        Parameters
        ----------
        command_board_settings: `sd.SettingsDictionary`
            dictionnaire de paramètres pupitres. Permet de connecter tous les éléments à leurs fonctions
        """
        button_index = 1
        # Essaye de charger des boutons jusqu'à ce que l'index soit trop grand et qu'il n'y en ait plus
        while f"button{button_index}.type" in command_board_settings:
            # Commence par charger toutes les fonctions relié au bouton
            function_index = 1
            functions = {}      # Dictionnaire {[état pins] : fonction, ...}
            while f"button{button_index}.function{function_index}.values" in command_board_settings\
                    and f"button{button_index}.function{function_index}.function" in command_board_settings:
                try:
                    functions[command_board_settings[f"button{button_index}.function{function_index}.values"]] = \
                        actions.Actions[command_board_settings[f"button{button_index}.function{function_index}.function"][8:]]
                except Exception as error:
                    log.debug(f"Erreur lors du chargement d'une des fonctions pupitre",
                              exception=error, prefix=f"button{button_index}.function{function_index}")
                function_index += 1

            # Récupère le type et les pins du bouton et initialise le bon boutton selon le type enregistré
            button_pins = command_board_settings.get_value(f"button{button_index}.pins", 0)
            button_type = command_board_settings.get_value(f"button{button_index}.type", "")
            button_read_mode = command_board_settings.get_value(f"button{button_index}.read_mode", "").lower()

            # Dans le cas où le bouton est un PushButton
            if str(button_type).lower() == str(components.Buttons.PUSH_BUTTON).lower():
                # Récupère les actions quand pressé et non pressé
                action_released = functions[False] if False in functions else None
                action_pressed = functions[True] if True in functions else None

                # Selon s'il est indiqué en mode update ou continuous, l'ajoute dans la liste correspondante
                if button_read_mode == "update":
                    self.update_components.append(components.Buttons.PUSH_BUTTON(self.board, button_pins[0],
                                                                              action_released, action_pressed))
                else:
                    self.continuous_components.append(components.Buttons.PUSH_BUTTON(self.board, button_pins[0],
                                                                                  action_released, action_pressed))
            # Dans le cas où le bouton est un Potentiometer
            elif str(button_type).lower() == str(components.Buttons.POTENTIOMETER).lower():
                # Récupère l'action à appeler lorsque mis à jour ainsi que les différentes constantes
                action = functions[None] if None in functions else None
                precision = command_board_settings.get_value(f"button{button_index}.precision", 1024)
                limits = command_board_settings.get_value(f"button{button_index}.limits", (-1, 1))
                error = command_board_settings.get_value(f"button{button_index}.error", 0.002)

                if button_read_mode == "update":
                    self.update_components.append(components.Buttons.POTENTIOMETER(self.board, button_pins[0], action,
                                                                                precision, limits, error))
                else:
                    self.continuous_components.append(components.Buttons.POTENTIOMETER(self.board, button_pins[0], action,
                                                                                    precision, limits, error))
            # Dans le cas où le bouton est un SwitchButton
            elif str(button_type).lower() == str(components.Buttons.POTENTIOMETER).lower():
                # Pour les PushButton aucun traitement supplémentaire n'est nécessaire
                if button_read_mode == "update":
                    self.update_components.append(components.Buttons.SWITCH_BUTTON(self.board, button_pins, actions))
                else:
                    self.continuous_components.append(components.Buttons.SWITCH_BUTTON(self.board, button_pins, actions))
            # Dans le cas où le bouton est en fait... une LED
            elif str(button_type).lower() == str(components.Buttons.POTENTIOMETER).lower():
                # Récupère l'action permettant de changer l'état de la LED
                action = functions[None] if None in functions else None

                # Ajoute le composant dans la liste des sorties
                self.output_components.append(components.Buttons.LED(self.board, button_pins[0], action))

            button_index += 1

        log.info(f"{len(self.continuous_components) + len(self.update_components)} connectés au pupitre")

    # Fonction (potentiellement à surcharger) permettant d'initialiser la fenêtre avec les boutons virtuels
    def initialise_virtual_buttons(self, app, settings, command_board_settings):
        """Fonction permettant d'initialiser la fenêtre avec les boutons virtuels

        Parameters
        ----------
        app: `QApplication`
            L'application sur laquelle les modules graphiques de la simulation vont se lancer
        settings: `sd.SettingsDictionary`
            dictionnaire de paramètres simulation. Utile nottament pour les boutons virtuels
        command_board_settings: `sd.SettingsDictionary`
            dictionnaire de paramètres pupitres. Permet de connecter tous les éléments à leurs fonctions

        Raises
        ------
        KeyError
            Jeté si certains arguments vitaux (tel que le type de carte électronique) ne sont pas présents
        PermissionError
            Jeté s'il est impossible pour le pupitre de se connecter à la carte électronique de gestion de celle-ci
        """
        # Vérifie si les boutons virtuels sont activés et si l'écran pour les boutons virtuels a été paramétré
        if command_board_settings.get_value("virtual.active", False) and \
                settings.get_value("sardine simulator.virtual buttons.screen_index", 0) > 0:
            # Essaye de charger la fenêtre d'écran virtuel et récupère une potentielle erreur
            try:
                pass # TODO : rempplacer par la création d'un pupitre virtuel (Generic.controls.virtual.controls.py)
            except Exception as error:
                log.error("Erreur lors du chargement de la partie virtuel du pupitre physique.",
                          exception=error)
        else:
            log.info("fenêtre des boutons virtuels non activée")

    # Fonction (potentiellement à surcharger) permettant de lancer le pupitre
    def launch_physical_buttons(self):
        """Fonction permettant de lancer le pupitre physique"""
        # Allume toutes les LEDs
        for o_c in self.output_components:
            o_c.change_state(True)

        # Vérifie les input de tous les composants une trentaine de fois pour récupérer la valeur initiale
        for i in range(30):
            for i_c in self.update_components + self.continuous_components:
                i_c.verify_value([])

        # Attend l'équivalent d'un délai pour s'assurer que les lampes restent allumées suffisament longtemps
        time.sleep(self.DELAY)

        # éteint toutes les lampes et appelle leur fonction respectives pour rallumer les bonnes
        for o_c in self.output_components:
            o_c.change_state(False)
            o_c.add_action(self.actions_list)
        self.update(self.train_database)

    # Fonction (potentiellement à surcharger) pour rendre visible la fenêtre avec tous les boutons virtuels
    def launch_virtual_buttons(self):
        """Fonction permettant de rendre visible la fenêtre contenant tous les boutons virtuels si elle existe"""
        # Si la fenêtre virtuelle existe et a été chargée correctement, la lance
        if self.virtual_command_board is not None:
            pass        # TODO : appeler la fonction de lancement des boutons virtuels

    # Fonction (à surcharger) permettant de lire les états des différents boutons en boucles
    def vérify_continuous(self):
        """Fonction permettant de lire en boucle les états des différents éléments du pupitre"""
        for component in self.continuous_components:
            component.verify_value(self.actions_list)

    # Fonction (à surchager) permettant de lire les valeurs analogiques (position manip de traction...)
    def prepend_update(self):
        """Fonction permettant de récupérer les valeurs ne nécessitant pas une lecture en continu"""
        for component in self.update_components:
            component.add_action(self.actions_list, prepend=True)

    def append_outputs(self):
        for component in self.output_components:
            component.add_action(self.actions_list)