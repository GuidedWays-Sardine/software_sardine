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
import src.misc.log as log
import src.misc.settings_dictionary as sd
import src.misc.translation_dictionary as td
import src.misc.decorators as decorators
import src.train.train_database.database as tdb
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

            # Indique les choix de matériel roulant et de positions possible
            self.win.setProperty("positions_type", [key.value for key in tdb.Position])
            self.win.setProperty("missions_type", [key.value for key in tdb.Mission])
            # Feature : rajouter le nombre maximum de portes et de niveaux pour les différents systèmes
            self.win.setProperty("max_doors_list", [0 if key == tdb.Mission.FREIGHT else
                                                    4 for key in tdb.Mission])
            self.win.setProperty("max_levels_list", [2 if key == tdb.Mission.PASSENGER else
                                                     0 if key == tdb.Mission.FREIGHT else
                                                     1 for key in tdb.Mission])

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
            self.win.setProperty("mission_list", self.train_database.systems.frame.get_mission_list())
            self.win.setProperty("position_list", self.train_database.systems.frame.get_position_list())

            # Appelle la fonction permettant de mettre à jour les différentes constantes
            self.update_constants(simple_parameters)

            # Appelle la fonction de mise à jour pour montrer la voiture avec l'index actuel
            self.win.findChild(QObject, "train_preview").setProperty("current_index", 0)
            self.update_popup(0)

    def update_constants(self, train_settings):
        """Fonction permettant de mettre à jour les différentes constantes de la popup complexe

        Parameters
        ----------
        train_settings: `sd.SettingsDictionary`
            Les paramètres du train (certains paramètres doivent être convertis du train à la voiture/au bogie
        """
        # Commence par mettre à jour les valeurs par défaut selon la moyenne des paramètres entrés
        self.win.setProperty("default_axles_count", train_settings.get_value("axles_per_bogie", 2))
        self.win.setProperty("default_axles_power", train_settings.get_value("axles_power", 750.0))
        self.win.setProperty("default_pad_brakes_count", round(train_settings.get_value("pad_brakes_count", 0) / train_settings.get_value("bogies_count", 1)))
        self.win.setProperty("default_disk_brakes_count", round(train_settings.get_value("disk_brakes_count", 0) / train_settings.get_value("bogies_count", 1)))
        self.win.setProperty("default_magnetic_brakes_count", round(train_settings.get_value("magnetic_brakes_count", 0) / train_settings.get_value("bogies_count", 1)))
        self.win.setProperty("default_foucault_brakes_count", round(train_settings.get_value("foucault_brakes_count", 0) / train_settings.get_value("bogies_count", 1)))

        # Puis met à jour les différentes limites
        # A-B-C non linéaire au nombre
        self.win.setProperty("a_max", self.parent.page.property("a_max"))
        self.win.setProperty("b_max", self.parent.page.property("b_max"))
        self.win.setProperty("c_max", self.parent.page.property("c_max"))
        self.win.setProperty("abc_decimals", self.parent.page.property("abc_decimals"))
        # Tout le reste ~linéaire au nombre de voitures, d'où la valeur divisée
        self.win.setProperty("max_railcar_weight", self.parent.page.property("max_weight") / train_settings["railcars_count"])
        self.win.setProperty("max_railcar_length", self.parent.page.property("max_length") / train_settings["railcars_count"])
        # Valeurs maximals déjà par défaut selon la voiture/le nombre de bogies
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
        -------
        train_parameters: `sd.SettingsDictionary`
            Dictionaire de paramètre avec tous les paramètres complexes du train, vide si aucun train initialisé
        """
        if self.train_database:
            return self.train_database.get_settings()
        else:
            return sd.SettingsDictionary()

    def set_complex_mode_values(self, train_parameters):
        """Fonction permettant de changer les valeurs du train

        Parameters
        ----------
        train_parameters: `sd.SettingsDictionary`
            Dictionaire contenant toutes les données complexes du train
        """
        try:
            self.train_database = tdb.TrainDatabase(train_parameters)
        except Exception as error:
            log.warning("Impossible de générer le train complexe à partir du fichier de paramètres envoyé.",
                        exception=error)
        else:
            # Récupère la liste de chacunes des positions des voitures
            self.win.setProperty("mission_list", self.train_database.systems.frame.get_mission_list())
            self.win.setProperty("position_list", self.train_database.systems.frame.get_position_list())

            # Appelle la fonction de mise à jour pour montrer la voiture avec l'index actuel
            self.update_constants(train_parameters)
            self.win.findChild(QObject, "train_preview").setProperty("current_index", 0)
            self.update_popup(0)

    def change_language(self, translations):
        """Fonction permettant de traduire la page de paramétrage train complet (appelé dans la page_rb2

        Parameters
        ----------
        translations: `td.TranslationDictionary`
            Dicionnaire de traduction contenant toutes les traductions nécessaires"""
        # Commence par traduire les différents textes visibles (fenêtre de génération)
        for widget_id in ["generate_button", "generate_l1", "generate_l2"]:
            widget = self.win.findChild(QObject, widget_id)
            widget.setProperty("text", translations[widget.property("text")])

        # Continue par traduire les textes des paramètres bogies
        for widget_id in ["front_bogie", "middle_bogie", "back_bogie"]:
            widget = self.win.findChild(QObject, widget_id)

            # Traduit chacuns des mots contenue dans le widget bogie parameters
            for parameter in ["articulated_text", "axle_text", "motor_text",
                              "pad_text", "disk_text", "magnetic_text", "foucault_text"]:
                widget.setProperty(parameter, translations[widget.property(parameter)])

    @decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
    def on_railcar_changed(self):
        """signal appelé lorsque la voiture paramétrée dans la popup complexe a changée.
        Récupère les données du popup, les changent dans la base de données et met à jour le popup et page de paramètres
        """
        # Récupère d'abord les index de la voiture à décharger et de celle à charger
        previous_railcar_index = self.win.property("previous_railcar_index")
        current_railcar_index = self.win.property("current_railcar_index")

        # Appelle d'abord la fonction pour mettre à jour la base de données avec les données visibles
        self.update_database(previous_railcar_index)

        # Appelle ensuite la fonction pour mettre à jour la popup avec les nouvelles données
        self.update_popup(current_railcar_index)

        # FEATURE : aussi mettre à jour les données simple (pour rendre le truc plus dynamique et correct)

    def update_database(self, railcar_index):
        """Fonction permettant de récupérer les valeurs de la popup et de les stoquer dans la base de données
        Attention, l'appel de cette fonction écrase les données de la voiture paramétrée

        Parameters
        ----------
        railcar_index: `int`
            index de la voiture dont les données seront récupérés (0 à Nrailcar - 1)
        """
        # TODO : mettre à jour les données de l'électrification

        # Récupère les paramètres de la voiture, les stockes et les mets à jour dans la voiture
        parameters = self.win.findChild(QObject, "general_data").get_values().toVariant()
        self.train_database.systems.frame.railcars[railcar_index].set_general_values(tdb.mission_getter[parameters[0]],
                                                                                     tdb.Position.FRONT if parameters[1] == 0 else
                                                                                     tdb.Position.BACK if parameters[1] == 2 else
                                                                                     tdb.Position.MIDDLE,
                                                                                     railcar_index, parameters[5], parameters[6],
                                                                                     parameters[2], parameters[3], parameters[4],
                                                                                     parameters[7], parameters[8],
                                                                                     parameters[9], parameters[10])

        # S'occupe du bogie avant
        # Récupère les données du bogie sur la popup complexe
        front_bogie_data = self.win.findChild(QObject, "front_bogie").get_values().toVariant()
        # Si les données sont vides ou que articulé est désactivé :
        if not front_bogie_data or not front_bogie_data[4]:
            # Essaye de diviser le bogie en deux bogies et récupère le bogie de devant
            self.train_database.systems.traction.split_bogies([railcar_index, railcar_index - 1], self.train_database)
            front_bogie = self.train_database.systems.traction.get_bogies(railcar_index, tdb.Position.FRONT)

            # Si aucun paramtètre n'a été récupéré, supprime le bogie et ses freins sinon change ses valeurs/crée le
            if not front_bogie_data and front_bogie:
                # Si aucun paramètre récupéré, supprime le bogie et tous ses systèmes de freins
                self.train_database.systems.traction.remove_bogie(front_bogie[0], self.train_database)
            elif front_bogie_data and front_bogie:
                front_modify_brakes = [b_a-b_c for b_a, b_c in zip(front_bogie_data[3][0], self.train_database.systems.braking.get_bogie_brakes_count(front_bogie[0]))]
                front_bogie[0].set_general_values(tdb.Position.FRONT, railcar_index,
                                                  front_bogie_data[0][0], front_bogie_data[1][0], front_bogie_data[2][0])
                self.train_database.systems.braking.modify_brakes_count(front_bogie[0], front_modify_brakes)
            elif front_bogie_data and not front_bogie:
                self.train_database.systems.traction.add_bogie((tdb.Position.FRONT, railcar_index,
                                                                front_bogie_data[0][0], front_bogie_data[1][0], front_bogie_data[2][0]))
                self.train_database.systems.braking.modify_brakes_count(self.train_database.systems.traction.get_bogies(railcar_index, tdb.Position.FRONT)[0],
                                                                        front_bogie_data[3][0])
        # Si les données sont les paramètres d'un bogie articulé
        else:
            # Crée un bogie articulé, le récupère et mets à jour ses données et ses systèmes de freinage
            self.train_database.systems.traction.merge_bogies([railcar_index - 1, railcar_index], self.train_database)
            front_bogie = self.train_database.systems.traction.get_bogies([railcar_index - 1, railcar_index])
            front_bogie[0].set_general_values(None, [railcar_index - 1, railcar_index],
                                              front_bogie_data[0][0], front_bogie_data[1][0], front_bogie_data[2][0])
            front_modify_brakes = [b_a - b_c for b_a, b_c in zip(front_bogie_data[3][0], self.train_database.systems.braking.get_bogie_brakes_count(front_bogie[0]))]
            self.train_database.systems.braking.modify_brakes_count(front_bogie[0], front_modify_brakes)

        # S'occupe des bogies centraux
        # Récupère d'abord les bogies centraux déjà existants pour la voiture
        middle_bogies = self.train_database.systems.traction.get_bogies(railcar_index, tdb.Position.MIDDLE)
        middle_bogies_data = self.win.findChild(QObject, "middle_bogie").get_values().toVariant()

        # Si des bogies centraux existent
        if middle_bogies_data:
            # Commence par modifier les données des bogies déjà existants
            for r_i in range(min(len(middle_bogies_data), len(middle_bogies))):
                middle_modify_brakes = [b_a - b_c for b_a, b_c in zip(middle_bogies_data[3][r_i], self.train_database.systems.braking.get_bogie_brakes_count(middle_bogies[r_i]))]
                middle_bogies[r_i].set_general_values(tdb.Position.MIDDLE, railcar_index,
                                                      middle_bogies_data[0][r_i], middle_bogies_data[1][r_i], middle_bogies_data[2][r_i])
                self.train_database.systems.braking.modify_brakes_count(middle_bogies[r_i], middle_modify_brakes)

            # Puis rajoute les bogies nécessaires (boucle sauté si aucun bogie à rajouter)
            for r_i in range(len(middle_bogies), len(middle_bogies_data[0])):
                self.train_database.systems.traction.add_bogie((tdb.Position.MIDDLE, railcar_index,
                                                                middle_bogies_data[0][r_i], middle_bogies_data[1][r_i], middle_bogies_data[2][r_i]))
                self.train_database.systems.braking.modify_brakes_count(self.train_database.systems.traction.get_bogies(railcar_index, tdb.Position.MIDDLE)[r_i], middle_bogies_data[3][r_i])

        # Si trop de bogies centraux existent, les suppriment
        for r_i in range(0 if not middle_bogies_data else len(middle_bogies_data[0]), len(middle_bogies)):
            self.train_database.systems.traction.remove_bogie(middle_bogies[r_i], self.train_database)

        # S'occupe du bogie arrière (très similairement au bogie avant)
        # Récupère les données du bogie sur la popup complexe
        back_bogie_data = self.win.findChild(QObject, "back_bogie").get_values().toVariant()
        # Si les données sont vides ou que articulé est désactivé :
        if not back_bogie_data or not back_bogie_data[4]:
            # Essaye de diviser le bogie en deux bogies et récupère le bogie de devant
            self.train_database.systems.traction.split_bogies([railcar_index, railcar_index + 1], self.train_database)
            back_bogie = self.train_database.systems.traction.get_bogies(railcar_index, tdb.Position.BACK)

            # Si aucun paramtètre n'a été récupéré, le supprime sinon change ses valeurs/en crée un nouveau
            if not back_bogie_data and back_bogie:
                self.train_database.systems.traction.remove_bogie(back_bogie[0], self.train_database)
            elif back_bogie_data and back_bogie:
                back_modify_brakes = [b_a - b_c for b_a, b_c in zip(back_bogie_data[3][0], self.train_database.systems.braking.get_bogie_brakes_count(back_bogie[0]))]
                back_bogie[0].set_general_values(tdb.Position.BACK, railcar_index,
                                                 back_bogie_data[0][0], back_bogie_data[1][0], back_bogie_data[2][0])
                self.train_database.systems.braking.modify_brakes_count(back_bogie[0], back_modify_brakes)
            elif back_bogie_data and not back_bogie:
                self.train_database.systems.traction.add_bogie((tdb.Position.BACK, railcar_index,
                                                                back_bogie_data[0][0], back_bogie_data[1][0], back_bogie_data[2][0]))
                self.train_database.systems.braking.modify_brakes_count(self.train_database.systems.traction.get_bogies(railcar_index, tdb.Position.BACK)[0],
                                                                        back_bogie_data[3][0])
        # Si les données sont les paramètres d'un bogie articulé
        else:
            # Crée un bogie articulé, le récupère et mets à jour ses données
            self.train_database.systems.traction.merge_bogies([railcar_index, railcar_index + 1], self.train_database)
            back_bogie = self.train_database.systems.traction.get_bogies([railcar_index, railcar_index + 1])
            back_bogie[0].set_general_values(None, [railcar_index, railcar_index + 1],
                                             back_bogie_data[0][0], back_bogie_data[1][0], back_bogie_data[2][0])
            back_modify_brakes = [b_a - b_c for b_a, b_c in zip(back_bogie_data[3][0], self.train_database.systems.braking.get_bogie_brakes_count(back_bogie[0]))]
            self.train_database.systems.braking.modify_brakes_count(back_bogie[0], back_modify_brakes)

    def update_popup(self, index):
        """Fonction permettant de récupérer les valeurs de la base de données et de les mettre sur la popup
        Attention, l'appel de cette fonction écrase les données visibles sur la popup de paramétrage complexe

        Parameters
        ----------
        index: `int`
            index de la voiture dont les données seront lus (0 à Nrailcar - 1)
        """
        # TODO : faire l'électrification

        # S'occupe des donnés générales
        parameters = self.train_database.systems.frame.railcars[index].get_general_values()
        self.win.findChild(QObject, "general_data").change_values(tdb.mission_getter[parameters[0]],
                                                                  parameters[1].value,
                                                                  [parameters[5], parameters[6]], parameters[7],
                                                                  parameters[3], parameters[4],
                                                                  parameters[8], parameters[9],
                                                                  parameters[10], parameters[11])

        # S'occupe maintenant du bogie avant.
        front_bogie = self.train_database.systems.traction.get_bogies(index, tdb.Position.FRONT)
        if front_bogie:
            # Récupère toutes les données du bogie avant et les envoient au bon format au bogie_parameters avant
            front_bogie_data = front_bogie[0].get_general_values()
            self.win.findChild(QObject, "front_bogie").change_values([front_bogie_data[2]],
                                                                     [[bool(axles) for axles in front_bogie_data[3]]],
                                                                     [front_bogie_data[3]],
                                                                     [self.train_database.systems.braking.get_bogie_brakes_count(front_bogie[0])],
                                                                     front_bogie[0].is_jacob_bogie())
        else:
            # Réinitialise juste les données pour le bogie avant sinon
            self.win.findChild(QObject, "front_bogie").clear()

        # S'occupe maintenant des bogies centraux
        middle_bogies = self.train_database.systems.traction.get_bogies(index, tdb.Position.MIDDLE)
        if middle_bogies:
            # Récupère les données de tous les bogies centraux
            middle_bogies_datas = [bogie.get_general_values() for bogie in middle_bogies]
            self.win.findChild(QObject, "middle_bogie").change_values([bogie[2] for bogie in middle_bogies_datas],
                                                                      [[bool(axles) for axles in bogie[3]] for bogie in middle_bogies_datas],
                                                                      [bogie[3] for bogie in middle_bogies_datas],
                                                                      [self.train_database.systems.braking.get_bogie_brakes_count(m_b) for m_b in middle_bogies],
                                                                      False)
        else:
            # Réinitialise juste les donnés pour les bogies centraux sinon
            self.win.findChild(QObject, "middle_bogie").clear()

        # S'occupe maintenant du bogie arrière
        back_bogie = self.train_database.systems.traction.get_bogies(index, tdb.Position.BACK)
        if back_bogie:
            # Récupère toutes les données du bogie avant et les envoient au bon format au bogie_parameters avant
            back_bogie_data = back_bogie[0].get_general_values()
            self.win.findChild(QObject, "back_bogie").change_values([back_bogie_data[2]],
                                                                    [[bool(axles) for axles in back_bogie_data[3]]],
                                                                    [back_bogie_data[3]],
                                                                    [self.train_database.systems.braking.get_bogie_brakes_count(back_bogie[0])],
                                                                    back_bogie[0].is_jacob_bogie())
        else:
            # Réinitialise juste les données pour le bogie avant sinon
            self.win.findChild(QObject, "back_bogie").clear()
