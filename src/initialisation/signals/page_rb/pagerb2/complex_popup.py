# Librairies par défaut
import os
import sys
import time


# Librairies graphiques
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


#Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.train.train_database.database as tdb
import src.misc.settings_dictionary.settings as sd
import src.misc.translation_dictionary.translation as td
import src.misc.decorators.decorators as decorators
import src.misc.log.log as log
import src.initialisation.signals.page_rb.page_rb2 as prb2


class ComplexPopup:
    """classe contenant toutes les fonctions pour la page de paramètre train en mode complexe"""

    # Eléments nécessaires au fonctionnement de la popup
    loaded = False
    app = None
    engine = None
    win = None

    # Base de données train utile au paramétrage
    train_database = None

    # Stocke la page parent
    parent = None

    # Constantes sur les emplacements des différents fichiers et dossiers nécessaires au fonctionement de la popup
    graphic_file_path = f"{PROJECT_DIR}src\\initialisation\\graphics\\page_rb\\page_rb2\\complex_popup.qml"

    def __init__(self, page_rb):
        """Fonction d'initialisation de la popup de paramétrage complexe train (reliée à la page_rb2)

        Parameters
        ----------
        page_rb: `prb2.PageRB2`
            La page de paramètres train (permettant d'accéder aux widgets du mode simple)

        Raises
        ------
        FileNotFoundError
            Soulevé quand le fichier .qml de la fenêtre d'initialisation n'est pas trouvé
        SyntaxError
            Soulevé quand le fichier .qml de la fenêtre d'initialisation a une erreur de syntaxe et n'est pas lisible
        """
        log.change_log_prefix("Initialisation popup train")

        # Initialise la popup de paramétrage complexe
        self.engine = QQmlApplicationEngine()
        self.engine.load(self.graphic_file_path)

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon laisse un message d'erreur
        if self.engine.rootObjects():
            self.win = self.engine.rootObjects()[0]
            self.win.hide()

            # Récupère le bouton des modes, le rend activable et le connecte à sa fonction
            self.win.closed.connect(lambda: self.win.hide())

            # Connecte tous les boutons nécessaires au fonctionnement de la popup de paramétrage complex
            self.parent = page_rb
            self.win.findChild(QObject, "generate_button").clicked.connect(self.on_complex_generate_clicked)
            self.win.railcar_changed.connect(self.on_railcar_changed)
            self.win.update.connect(self.update_popup)

            # Indique que la fenêtre est complètement
            self.loaded = True
            log.info("Chargement de la popup de paramétrage complexe réussi avec succès.")
            log.change_log_prefix("Initialisation")
        else:
            # Sinon laisse un message de warning selon si le fichier est introuvable ou contient des erreurs
            if os.path.isfile(self.graphic_file_path):
                raise SyntaxError(f"le fichier graphique de la popup complexe contient des erreurs.\n\t{self.graphic_file_path}")
            else:  # Cas où le fichier n'existe pas
                raise FileNotFoundError(f"Le fichier graphique de la popup complexe n'a pas été trouvé.\n\t{self.graphic_file_path}")

    @decorators.QtSignal(log_level=log.Level.ERROR, end_process=False)
    def on_complex_generate_clicked(self):
        """Fonction activée lorsque le bouton généré est cliqué"""
        try:
            # Génère le train à partir des données simples
            simple_parameters = self.parent.get_simple_mode_values()
            self.train_database = tdb.TrainDatabase(simple_parameters)
        except Exception as error:
            # S'il y a une erreur, laisse un message d'erreur et désactive le mode complexe
            log.error("Impossible de correctement générer le train, mode complexe désactivé.\n",
                      exception=error, prefix="Génération train complexe")
            self.win.hide()
            self.win.setProperty("generated", False)
            self.parent.page.setProperty("generated", False)
            mode_switchbutton = self.parent.page.findChild(QObject, "mode_switchbutton")
            mode_switchbutton.change_selection(0)
            mode_switchbutton.setProperty("is_activable", False)
            mode_switchbutton.setProperty("is_positive", False)
            self.loaded = False
        else:
            # Sinon indique aux différentes pages que le mode complexe de paramétrage a été activé
            self.parent.current_mode = self.parent.Mode.COMPLEX
            self.win.setProperty("generated", True)
            self.parent.page.setProperty("generated", True)

            # Récupère la liste de chacunes des positions des voitures
            self.win.setProperty("mission_list", self.train_database.systems.get_mission_list())
            self.win.setProperty("position_list", self.train_database.systems.get_position_list())

            # Appelle la fonction permettant de mettre à jour les différentes constantes
            self.update_constants(simple_parameters)

            # Appelle la fonction de mise à jour pour montrer la voiture avec l'index actuel
            self.win.findChild(QObject, "train_preview").setProperty("current_index", 0)
            self.update_popup(0)

    def update_constants(self, train_data):
        """Fonction permettant de mettre à jour les différentes constantes de la popup complexe

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Les paramètres du train (certains paramètres doivent être convertis du train à la voiture/au bogie
        """
        # Commence par mettre à jour les valeurs par défaut selon la moyenne des paramètres entrés
        self.win.setProperty("default_axles_count", train_data.get_value("axles_per_bogie", 2))
        self.win.setProperty("default_axles_power", train_data.get_value("axles_power", 750.0))
        self.win.setProperty("default_pad_brakes_count", round(train_data.get_value("pad_brakes_count", 0) / train_data.get_value("bogies_count", 1)))
        self.win.setProperty("default_disk_brakes_count", round(train_data.get_value("disk_brakes_count", 0) / train_data.get_value("bogies_count", 1)))
        self.win.setProperty("default_magnetic_brakes_count", round(train_data.get_value("magnetic_brakes_count", 0) / train_data.get_value("bogies_count", 1)))
        self.win.setProperty("default_foucault_brakes_count", round(train_data.get_value("foucault_brakes_count", 0) / train_data.get_value("bogies_count", 1)))

        # Puis met à jour les différentes limites
        self.win.setProperty("max_bogies_per_railcar", max(self.parent.page.property("max_bogies_per_railcar"), 2))
        self.win.setProperty("max_axles_per_bogies", self.parent.page.property("max_axles_per_bogie"))
        self.win.setProperty("max_axles_power", self.parent.page.property("max_axles_power"))
        self.win.setProperty("max_pad_brakes_per_axle", self.parent.page.property("max_pad_brakes_per_axle"))
        self.win.setProperty("max_disk_brakes_per_axle", self.parent.page.property("max_disk_brakes_per_axle"))
        self.win.setProperty("max_magnetic_brakes_per_axle", self.parent.page.property("max_magnetic_brakes_per_axle"))

    def reset(self):
        """Fonction permettant de réinitialiser le mode complexe (supression des données)"""
        # Passe la base de données train à None (elle devra être recréée après)
        self.train_database = None

    def get_complex_mode_values(self):
        """Fonction permettant de récupérer toutes les informations de la configuration simple

        Returns
        ----------
        train_parameters: `sd.SettingsDictionary`
            Dictionaire de paramètre avec tous les paramètres complexes du train
        """
        parameters = sd.SettingsDictionary()

        # TODO : sauvegarder les données

        return parameters

    def set_complex_mode_values(self, train_data):
        """"""

    def change_language(self, translation_data):
        """Fonction permettant de traduire la page de paramétrage train complet (appelé dans la page_rb2

        Parameters
        ----------
        translation_data: `td.TranslationData`
            Dicionnaire de traduction contenant toutes les traductions nécessaires"""
        # Commence par traduire les différents textes visibles (fenêtre de génération)
        for widget_id in ["generate_button", "generate_l1", "generate_l2"]:
            widget = self.win.findChild(QObject, widget_id)
            widget.setProperty("text", translation_data[widget.property("text")])

        # Continue par traduire les textes des paramètres bogies
        for widget_id in ["front_bogie", "middle_bogie", "back_bogie"]:
            widget = self.win.findChild(QObject, widget_id)

            # Traduit chacuns des mots contenue dans le widget bogie parameters
            for parameter in ["articulated_text", "axle_text", "motor_text",
                              "pad_text", "disk_text", "magnetic_text", "foucault_text"]:
                widget.setProperty(parameter, translation_data[widget.property(parameter)])

    @decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
    def on_railcar_changed(self):
        """signal appelé lorsque la voiture paramétrée dans la popup complexe a changée"""
        # Récupère d'abord les index de la voiture à décharger et de celle à charger
        previous_railcar_index = self.win.property("previous_railcar_index")
        current_railcar_index = self.win.property("current_railcar_index")

        # Appelle d'abord la fonction pour mettre à jour la base de données avec les données visibles
        self.update_database(previous_railcar_index)

        # Appelle ensuite la fonction pour mettre à jour la popup avec les nouvelles données
        self.update_popup(current_railcar_index)



    def split_bogies(self, linked_coaches):
        """Fonction permettant de diviser un bogie jacobien en deux bogies.

        Parameters
        ----------
        linked_coaches: `list`
            Index des deux voitures dont le bogie articulé doit être séparé.
            elle doit contenir deux voitures consécutives. Si aucun bogie articulé n'est trouvé, rien ne se passera.
        """
        # Vérifie que la liste d'index est bien composé de deux index consécutif
        if isinstance(linked_coaches, list) and len(linked_coaches) == 2 and int(min(linked_coaches)) == int(max(linked_coaches) - 1):
            # Récupère le bogie articulé à diviser et le divise s'il existe (sinon fait rien)
            jacob_bogie = self.train_database.systems.get_bogies(linked_coaches)
            if jacob_bogie:
                # Récupère les données du bogie
                bogie_data = jacob_bogie[0].get_general_values()

                # met à jour les données du bogie récupérer pour le mettre à l'arrière de la voiture avant
                jacob_bogie[0].set_general_values(tdb.Position.BACK,
                                                  -1,
                                                  int(min(linked_coaches)),
                                                  bogie_data[3],
                                                  None,
                                                  bogie_data[4])

                # Rajoute un nouveau bogie à l'avant de la voiture arrière avec les mêmes données
                self.train_database.systems.traction.append(tdb.systems.traction.Bogie(tdb.Position.FRONT,
                                                                                       -1,
                                                                                       int(max(linked_coaches)),
                                                                                       bogie_data[3],
                                                                                       None,
                                                                                       bogie_data[4]))

            # TODO : dupliquer les systèmes de freinages
        else:
            log.debug(f"Impossible de séparer les deus bogies. Liste de voitures invalide ({linked_coaches}).")


    def merge_bogies(self, linked_coaches):
        """Fonction permettant de fusioner deux bogies pour en faire un bogie articulé.
        Si aucun bogie existe sur les deus voitures, un bogie articulé sera créé

        Parameters
        ----------
        linked_coaches: `list`
            Index des deux voitures dont les bogies doivent être fusionés.
            elle doit contenir deux voitures consécutives. Si l'une des voitures sont suspendus, créera un nouveau bogie
        """
        # Vérifie que la liste d'index est bien composé de deux index consécutif
        if isinstance(linked_coaches, list) and len(linked_coaches) == 2 and int(min(linked_coaches)) == int(max(linked_coaches) - 1):
            # Vérifie qu'il n'y a pas déjà un bogie articulé entre ces deux voitures, sinon retourne
            if self.train_database.systems.get_bogies([int(linked_coaches[0]), int(linked_coaches[1])]):
                return

            # Récupère les deux bogies à fusioner
            back_bogie = self.train_database.systems.get_bogies(int(min(linked_coaches)), tdb.Position.BACK)
            front_bogie = self.train_database.systems.get_bogies((int(max(linked_coaches))), tdb.Position.FRONT)

            # Si au moins l'un des bogies non articulé existe
            if front_bogie or back_bogie:
                # Commence par supprimer le bogie arrière si les deux bogies non articulés existe (évite le duplicata)
                if front_bogie and back_bogie:
                    self.train_database.systems.traction.remove(back_bogie[0])

                # Utilise ce bogie comme base pour créer le bogie articulé
                bogie_data = front_bogie[0].get_general_values() if front_bogie else back_bogie[0].get_general_values()

                # met à jour les données du bogie récupérer pour le mettre à l'arrière de la voiture avant
                front_bogie[0].set_general_values(None,
                                                  -1,
                                                  [int(linked_coaches[0]), int(linked_coaches[1])],
                                                  bogie_data[3],
                                                  None,
                                                  bogie_data[4])
            # Si les deux bogies n'existent pas (les deux voitures suspendus)
            else:
                # Génère un essieu porteur
                self.train_database.systems.traction.append(tdb.systems.traction.Bogie(None,
                                                                                       -1,
                                                                                       [int(linked_coaches[0], int(linked_coaches[1]))],
                                                                                       self.win.property("default_axles_count"),
                                                                                       0,
                                                                                       0.0))

        # TODO : dupliquer les systèmes de freinages
        else:
            log.debug(f"Impossible de fusionner deux voitures. Liste de voitures invalide ({linked_coaches}).")
