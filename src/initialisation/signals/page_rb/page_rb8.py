# Librairies par défaut
import os
import sys


# Librairies graphiques
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary.settings as sd
import src.misc.translation_dictionary.translation as td
import src.misc.log.log as log


class PageRB8:
    """classe pour la page de paramètres 8"""

    # variables nécessaire au bon fonctionnement de la page
    index = 8   # Attention dans les tableaux l'index commence à 0
    name = "Écrans"
    engine = None
    page = None
    current_button = None
    screen_count = 0
    screen_index = []

    # Informations par défauts des écrans {"nom écran": [sera utilisé ?, longuer minimum, hauteur minimum]}
    screen_default = {}
    screen_settings = {}
    category_active = ""
    screen_list_active = 0

    def __init__(self, application, engine, index, current_button):
        """Fonction d'initialisation de la page de paramtètres 1 (page paramètres général)

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        page: `QQmlApplicationEngine`
            La QQmlApplicationEngine de la page à charger
        index: `int`
            index de la page (1 pour le bouton d'en haut -> 8 pour le bouton d'en bas
        current_button: `QObject`
            Le bouton auquel sera relié la page (généralement d'id : page_rb + index)
        """
        # Stocke les informations nécessaires au fonctionnement de la page
        self.index = index
        self.engine = engine
        self.page = engine.rootObjects()[0]
        self.current_button = current_button
        self.current_button.setProperty("text", self.name)

        # Récupère le nombre d'écrans présents
        self.screen_count = QDesktopWidget().screenCount()
        self.screen_index = [None] * self.screen_count
        log.info(str(self.screen_count) + " écrans détectés.\n")

        # Charge autant de fenêtres d'index d'écrans qu'il y a d'écrans
        for screen_index in range(0, self.screen_count):
            application.engine.load(PROJECT_DIR + "src\\initialisation\\graphics\\page_rb\\page_rb8\\screen_index.qml")
            self.screen_index[screen_index] = application.engine.rootObjects()[len(application.engine.rootObjects()) - 1]
            self.screen_index[screen_index].hide()

        # Puis récupère les tailles des écrans et places les différentes fenêtres d'index en haut à gauche des écrans
        # Et dans le même temps initialise la liste de choix des écrans
        screen_list = ["Aucun"]
        screen_dimensions = []
        for screen_index in range(0, self.screen_count):
            sg = QDesktopWidget().screenGeometry(screen_index).getCoords()
            self.screen_index[screen_index].setPosition(sg[0], sg[1])
            screen_dimensions.append([sg[2] - sg[0] + 1, sg[3] - sg[1] + 1])
            self.screen_index[screen_index].findChild(QObject, "screen_index").setProperty("text", str(screen_index + 1))
            screen_list.append(str(screen_index + 1))

        # Envoie liste des fenètre et de leurs dimensions à la graphique de la page*
        self.page.setProperty("screen_list", screen_list)
        self.page.setProperty("screen_size", screen_dimensions)

        # Charge la traduction pour le nom des fichiers et des catégories (Anglais -> langue actuelle)
        translation_data = td.TranslationDictionnary()
        translation_data.create_translation(PROJECT_DIR + "settings\\language_settings\\initialisation.lang",
                                            "English", application.language)

        # Pour chacun des fichiers dans le répertoire de paramètres d'écrans
        for file_path in (f for f in os.listdir(PROJECT_DIR + "settings\\screen_settings") if f.endswith(".screens")):
            # Ouvre le fichier, et crée un dictionaire vide pour les écrans dans le fichier
            file = open(PROJECT_DIR + "settings\\screen_settings\\" + file_path, "r", encoding="utf-8-sig")
            screens_default = {}
            screens_settings = {}

            # Pour chacune des lignes contenant des informations
            for line in (l for l in file.readlines() if l != "\n" and l[0] != "#"):
                # Rajoute les paramètres par défaut et crée une ligne de paramètres (incomplet par défaut)
                info = list(map(str.strip, line.rstrip("\n").split(";")))
                screens_default[translation_data[info[0]]] = [True,
                                                              int(info[1]) if len(info) >= 2 else 0,
                                                              int(info[2]) if len(info) >= 3 else 0,
                                                              True if len(info) >= 4 and info[3].lower() == "true" else False]

                screens_settings[translation_data[info[0]]] = [0, False, [0, 0], [0, 0]]

            # Rajouter cette série d'écran à la catégorie
            self.screen_default[translation_data[file_path.replace("_", " ")[3:-8]]] = screens_default
            self.screen_settings[translation_data[file_path.replace("_", " ")[3:-8]]] = screens_settings

        # Définit le fonctionnement de base des boutons supérieurs et inférieurs
        if self.screen_default:
            # Rend le texte supérieur en gris claire
            self.page.findChild(QObject, "category_title").setProperty("is_dark_grey", False)

            # Change le nom de la catégorie pour la première catégorie d'écrans (pour initialiser une page)
            self.category_active = list(self.screen_default.keys())[0]
            self.page.findChild(QObject, "category_title").setProperty("text", self.category_active)

            # Rend fonctionnel les boutons inférieurs (visibles et activable que quand nécessaire)
            self.page.findChild(QObject, "left_screen_button").clicked.connect(self.on_left_screen_button_pressed)
            self.page.findChild(QObject, "right_screen_button").clicked.connect(self.on_right_screen_button_pressed)

            # S'il y a plus d'une catégorie d'écrans, rend les boutons supérieurs de catégories fonctionnels
            if len(self.screen_default.keys()) > 1:
                left_category_button = self.page.findChild(QObject, "left_category_button")
                left_category_button.setProperty("is_activable", False)
                left_category_button.clicked.connect(self.on_left_category_button_clicked)
                right_category_button = self.page.findChild(QObject, "right_category_button")
                right_category_button.setProperty("is_activable", True)
                right_category_button.clicked.connect(self.on_right_category_button_clicked)
        else:
            # Dans le cas où la liste des écrans à paramétrer est nulle
            self.page.findChild(QObject, "category_title").setProperty("is_dark_grey", True)
            self.page.findChild(QObject, "category_title").setProperty("text", "Aucun écran à paramétrer")
            raise NameError("Aucun écran à paramétrer. Le dictionnaire \"screen_default\" est vide.")

        # connecte les différents boutons des autres pages à la paramétrabilité de certaines fenêtres
        # FEATURE : Ajouter les conditions dans des fonctions annexes comme ci-dessous pour les autres pages
        self.connect_page_rb1(application)

        # Définit la page comme validée (toutes les valeurs par défaut suffisent)
        application.is_completed_by_default[self.index - 1] = "is_page_valid" not in dir(self)

    def connect_page_rb1(self, application):
        if application.visible_pages[0] is not None and not isinstance(application.visible_pages[0], type(self.engine)):
            # camera_check pour ligne virtuelle ou train caméra
            application.visible_pages[0].page.findChild(QObject, "camera_check").value_changed.connect(
                lambda: self.on_camera_train_checked(application))
            self.on_camera_train_checked(application)

            # pcc_check pour TCO et toute autre fenêtre nécessaire au fonctionnement du PCC
            application.visible_pages[0].page.findChild(QObject, "pcc_check").value_changed.connect(
                lambda: self.on_pcc_checked(application))
            self.on_pcc_checked(application)

            # data_check pour l'affichage des données en direct
            application.visible_pages[0].page.findChild(QObject, "data_check").value_changed.connect(
                lambda: self.on_data_checked(application))
            application.visible_pages[0].page.findChild(QObject, "dashboard_check").value_changed.connect(
                lambda: self.on_data_checked(application))
            self.on_data_checked(application)
        else:
            log.warning("Certains paramétrages d'écrans dépendent du bon fonctionnement de la page_rb1." +
                        "Ceux-ci ne peuvent pas se charger correctement.\n")

            # Désactive l'écran train caméra
            category = list(self.screen_default.keys())[0]
            screen_camera_train = list(self.screen_default[category].keys())[3]
            self.screen_default[category][screen_camera_train][0] = False

            # Désactive les graphs en mode fenêtré
            category = list(self.screen_default.keys())[2]
            screen_dashboard = list(self.screen_default[category].keys())[0]
            for screen_graph in list(self.screen_default[category].keys()):
                if screen_graph == screen_dashboard:
                    self.screen_default[category][screen_graph][0] = True
                else:
                    self.screen_default[category][screen_graph][0] = False

    def is_page_valid(self):
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        # Pour toutes les catégories de paramètrages d'écrans
        for category_key in list(self.screen_default.keys()):
            # Pour tous les écrans de cette catégorie
            for screen_key in list(self.screen_default[category_key].keys()):
                # Vérifier pour chaque page si la page doit et peut être complétée mais ne l'est pas
                if self.screen_default[category_key][screen_key][0] and \
                        self.screen_default[category_key][screen_key][3] \
                        and self.screen_settings[category_key][screen_key][0] == 0:
                    print(self.screen_default[category_key][screen_key][0],
                          self.screen_default[category_key][screen_key][3],
                          self.screen_settings[category_key][screen_key][0])
                    return False

        # Si aucune des pages n'a pas encore été complétée, retourne que la page est complète
        return True

    def on_camera_train_checked(self, application):
        """Signal appelé lorsque le checkbutton camera_check est coché ou décoché.
        Permet de mettre à jour la paramétrabilité des fenêtres Train caméra et ligne virtuelle

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Récupère si le checkbutton est activé, le nom de la catégorie et des écrans à modifier
        is_checked = application.visible_pages[0].page.findChild(QObject, "camera_check").property("is_checked")
        category = list(self.screen_default.keys())[0]
        screen_virtual_line = list(self.screen_default[category].keys())[2]
        screen_camera_train = list(self.screen_default[category].keys())[3]

        # Change la paramétrabilité des écrans souhaités
        self.screen_default[category][screen_virtual_line][0] = not is_checked
        self.screen_default[category][screen_camera_train][0] = is_checked

        # Réinitialise les paramètres de ces écrans s'ils ne sont plus paramétrables
        if not self.screen_default[category][screen_virtual_line][0]:
            self.screen_settings[category][screen_virtual_line] = [0, False, [0, 0], [0, 0]]
        else:
            self.screen_settings[category][screen_camera_train] = [0, False, [0, 0], [0, 0]]

    def on_pcc_checked(self, application):
        """Signal appelé lorsque le checkbutton camera_check est coché ou décoché.
        Permet de mettre à jour la paramétrabilité des fenêtres TCO du PCC

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Récupère si le checkbutton est activé, le nom de la catégorie et des écrans à modifier
        is_checked = application.visible_pages[0].page.findChild(QObject, "pcc_check").property("is_checked")
        category = list(self.screen_default.keys())[1]
        screen_tco = list(self.screen_default[category].keys())[0]

        # Change la paramétrabilité des écrans souhaités
        self.screen_default[category][screen_tco][0] = is_checked

        # Réinitialise les paramètres de ces écrans s'ils ne sont plus paramétrables
        if not self.screen_default[category][screen_tco][0]:
            self.screen_settings[category][screen_tco] = [0, False, [0, 0], [0, 0]]

    def on_data_checked(self, application):
        """Signal appelé lorsque le checkbutton camera_check est coché ou décoché.
        Permet de mettre à jour la paramétrabilité des fenêtres des courbes de paramètres en direct

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Récupère si les données sont activées et si elles sont activées en mode dashboard
        is_data_checked = application.visible_pages[0].page.findChild(QObject, "data_check").property("is_checked")
        dashboard = application.visible_pages[0].page.findChild(QObject, "dashboard_check")
        dashboard.setProperty("is_activable", is_data_checked)
        category = list(self.screen_default.keys())[2]
        screen_graphs = list(self.screen_default[category].keys())
        screen_dashboard = screen_graphs[0]

        # Mets à jour la paramétrabilité des écrans
        for screen_graph in screen_graphs:
            if is_data_checked and (dashboard.property("is_checked") == (screen_graph == screen_dashboard)):
                self.screen_default[category][screen_graph][0] = True
            else:
                self.screen_default[category][screen_graph][0] = False
                self.screen_settings[category][screen_graph] = [0, False, [0, 0], [0, 0]]

    def get_values(self, translation_data):
        """Récupère les paramètres de la page de paramètres page_rb8

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) 

        Returns
        -------
        parameters : `dictionary`
            un dictionaire de paramètres de la page de paramètres page_rb8
        """
        # Initialise les paramètres récupérés et récupère le paramètre sur si les écrans sont éteins
        page_parameters = sd.SettingsDictionnary()
        page_parameters["immersion"] = self.page.findChild(QObject, "black_screens_check").property("is_checked")

        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        # Pour chaque catégorie d'écrans
        for category_key in list(self.screen_settings.keys()):
            # Pour chaque écrans de cette catégorie
            for screen_key in list(self.screen_settings[category_key].keys()):
                # Récupère les paramètres de l'écran et les sauvegardes (dépend de si l'écran est sélectionable ou non
                screen_settings_key = translation_data[category_key] + "." + translation_data[screen_key] + "."
                is_activable = self.screen_default[category_key][screen_key][0]
                screen_settings_values = self.screen_settings[category_key][screen_key]
                page_parameters[screen_settings_key + "screen_index"] = screen_settings_values[0] if is_activable else 0
                page_parameters[screen_settings_key + "full_screen"] = screen_settings_values[1] if is_activable else False
                page_parameters[screen_settings_key + "x"] = screen_settings_values[2][0] if is_activable else 0
                page_parameters[screen_settings_key + "y"] = screen_settings_values[2][1] if is_activable else 0
                page_parameters[screen_settings_key + "w"] = screen_settings_values[3][0] if is_activable else 0
                page_parameters[screen_settings_key + "h"] = screen_settings_values[3][1] if is_activable else 0

        return page_parameters

    def set_values(self, data, translation_data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings de la page de paramètres 8

        Parameters
        ----------
        data: `dict`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) 
        """
        # Change la valeur pour les écrans noirs
        data.update_parameter(self.page, "black_screens_check", "is_checked", "immersion")

        # Inverse les données de traduction pour avoir un dictionnaire langue actuelle -> Français
        invert_translation = td.TranslationDictionnary()
        invert_translation.create_translation(PROJECT_DIR + "settings\\language_settings\\initialisation.lang",
                                              translation_data["English"], "English")

        # Pour chaque catégorie d'écrans
        for category_key in list(self.screen_settings.keys()):
            # Pour chaque écrans de cette catégorie
            for screen_key in list(self.screen_settings[category_key].keys()):
                # Crée pour chaque écran la clé avec laquelle l'information serait sauvegardée
                screen_settings_key = invert_translation[category_key] + "." + invert_translation[screen_key] + "."

                # Essaye de récupérer les donnés reliées à l'écran
                try:
                    if int(data[screen_settings_key + "screen_index"]) <= self.screen_count:
                        self.screen_settings[category_key][screen_key][0] = data[screen_settings_key + "screen_index"]
                        self.screen_settings[category_key][screen_key][1] = data[screen_settings_key + "full_screen"]
                        self.screen_settings[category_key][screen_key][2][0] = data[screen_settings_key + "x"]
                        self.screen_settings[category_key][screen_key][2][1] = data[screen_settings_key + "y"]
                        self.screen_settings[category_key][screen_key][3][0] = data[screen_settings_key + "w"]
                        self.screen_settings[category_key][screen_key][3][1] = data[screen_settings_key + "h"]
                except KeyError:
                    log.debug("L'écran : " + screen_settings_key + " n'a pas de paramètres sauvegardés.\n")

        # Met à jour la page visible de settings
        self.change_visible_screen_list()

    def change_language(self, translation_data):    # TODO : améliorer avec le dictionnaire de traduction
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de la page de paramètres

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) 
        """
        # Traduit le nom de la catégorie
        self.current_button.setProperty("text", translation_data[self.current_button.property("text")])

        # Change la traduction pour le texte Plein écran ? du DMI_checkbutton
        self.page.setProperty("fullscreen_text", translation_data[self.page.property("fullscreen_text")])

        # Pour chaque catégories
        for category_key in list(self.screen_default.keys()):
            # Pour chaque écrans de chaques catégories
            for screen_key in list(self.screen_default[category_key].keys()):
                # Traduit la clé d'écran pour le dictionaire de paramètres choisis et de paramètres par défaut
                self.screen_default[category_key][translation_data[screen_key]] = self.screen_default[category_key][screen_key]
                self.screen_settings[category_key][translation_data[screen_key]] = self.screen_settings[category_key][screen_key]

                # Si la clé d'écran a été traduite avec succès, enlève la version non traduite
                if screen_key != translation_data[screen_key]:
                    self.screen_default[category_key].pop(screen_key)
                    self.screen_settings[category_key].pop(screen_key)

            # Traduit la clé de catégorie pour le dictionaire de paramètres choisis et de paramètres par défaut
            self.screen_default[translation_data[category_key]] = self.screen_default[category_key]
            self.screen_settings[translation_data[category_key]] = self.screen_settings[category_key]

            # Si la clé de la catégorie a été traduite avec succès, enlève la version non traduite
            if category_key != translation_data[category_key]:
                self.screen_default.pop(category_key)
                self.screen_settings.pop(category_key)

            # Si la catégorie est la catégorie active, traduit la catégorie active
            if self.category_active == category_key:
                self.category_active = translation_data[self.category_active]

        # Traduit le texte devant le DMI_checkbutton pour savoir
        black_screens_check = self.page.findChild(QObject, "black_screens_check")
        black_screens_check.setProperty("text", translation_data[black_screens_check.property("text")])

        # Remets à jour la page actuelle et le titre de la catégorie
        self.page.findChild(QObject, "category_title").setProperty("text", self.category_active)
        self.change_visible_screen_list()

    def on_page_opened(self, application):
        """Fonction appelée lorsque la page de paramètres 8 est chargée.
        Permet d'afficher les fenêtre d'index et actualise les paramètres des écrans visibles

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Rend visible tous les écrans d'index
        for screen_index in self.screen_index:
            screen_index.show()

        # Remets à jour la page actuelle
        self.change_visible_screen_list()

    def on_page_closed(self, application):
        """Fonction appelée quand la page de paramètres 8 est fermée.
        Permet de cacher les différentes fenêtres d'index

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Cache toutes les fenêtres d'index
        for screen_index in self.screen_index:
            screen_index.hide()

        # récupère les valeurs des écrans actuels et les sauvegarde
        screens_values = self.page.get_values().toVariant()
        for index in range(0, len(screens_values)):
            self.screen_settings[self.category_active][screens_values[index][0]] = screens_values[index][1]

    def on_left_category_button_clicked(self):
        """Signal appelé quand le bouton pour passer à la catégorie de paramétraghes d'écran de gauche est cliqué.
        Attention ce signal doit être appelé uniquement si la page de gauche existe, sous risque de crash.
        """
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        left_category_button = self.page.findChild(QObject, "left_category_button")
        category_title = self.page.findChild(QObject, "category_title")

        # Récupère l'index et le nom du nouvel élément
        new_index = list(self.screen_default.keys()).index(category_title.property("text")) - 1
        self.category_active = list(self.screen_default.keys())[new_index]

        # Si nouvel élément trouvé, change le titre de la catégorie.
        category_title.setProperty("text", self.category_active)

        # Remet l'index de la liste d'écrans visible à 0 et appelle la fonction pour changer les écrans visibles
        self.screen_list_active = 0
        self.change_visible_screen_list()

        # Rend le bouton de droite actif, et si première catégorie rend celui de gauche inactif
        self.page.findChild(QObject, "right_category_button").setProperty("is_activable", True)
        if new_index == 0:
            left_category_button.setProperty("is_activable", False)

    def on_right_category_button_clicked(self):
        """Signal appelé quand le bouton pour passer à la catégorie de paramétraghes d'écran de droite est cliqué.
        Attention ce signal doit être appelé uniquement si la page de droite existe, sous risque de crash.
        """
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        right_category_button = self.page.findChild(QObject, "right_category_button")
        category_title = self.page.findChild(QObject, "category_title")

        # Récupère l'index et le nom du nouvel élément
        new_index = list(self.screen_default.keys()).index(self.category_active) + 1
        self.category_active = list(self.screen_default.keys())[new_index]

        # Change le nom de la catégorie active
        category_title.setProperty("text", self.category_active)

        # Remet l'index de la liste d'écrans visible à 0 et appelle la fonction pour changer les écrans visibles
        self.screen_list_active = 0
        self.change_visible_screen_list()

        # Rend le bouton de gauche actif, et si dernière catégorie rend celui de droite inactif
        self.page.findChild(QObject, "left_category_button").setProperty("is_activable", True)
        if new_index == len(self.screen_default.keys()) - 1:
            right_category_button.setProperty("is_activable", False)

    def on_left_screen_button_pressed(self):
        """Signal appelé quand le bouton pour passer à la série de paramétraghes d'écran de gauche d'une catégorie est cliqué.
        Attention ce signal doit être appelé uniquement si la série d'écrans de gauche existe, sous risque de crash.
        """
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        # Diminue l'index de la liste d'écrans et appelle la fonction pour changer les écrans à paramétrer
        self.screen_list_active -= 1
        self.change_visible_screen_list()

    def on_right_screen_button_pressed(self):
        """Signal appelé quand le bouton pour passer à la série de paramétraghes d'écran de droite d'une catégorie est cliqué.
        Attention ce signal doit être appelé uniquement si la série d'écrans de droite existe, sous risque de crash.
        """
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        # Augmente l'index de la liste d'écrans et appelle la fonction pour changer les écrans à paramétrer
        self.screen_list_active += 1
        self.change_visible_screen_list()

    def change_visible_screen_list(self):
        """Met à jour la liste de paramétrages éccrans visible par l"utilisateur.
        A appeler dans le cas où la catégorie ou la série d'écran a été changé ou que les paramètres défauts de l'écrans ont été changés.
        """
        # Essaye de récupérer le dictionnaire des écrans de la catégorie sélectionnée et récupère leurs clés
        category_screen_dict = self.screen_default[self.category_active]
        default_settings_dict = self.screen_settings[self.category_active]
        category_screen_list = list(category_screen_dict.keys())

        # Vide les liste qui seront envoyés à la partie graphique
        visible_screen_names = []
        visible_screen_activable = []
        visible_screen_minimum_wh = []
        visible_screen_default_settings = []

        # S'il y a plus de 4 écrans dans la catégorie, montre les 4 premiers sinon les montre tous
        for index in range(self.screen_list_active * 4,
                           len(category_screen_list) if len(category_screen_list) <= (self.screen_list_active + 1) * 4
                           else 4 * (self.screen_list_active + 1)):
            screen_data = category_screen_dict[category_screen_list[index]]
            visible_screen_default_settings.append(default_settings_dict[category_screen_list[index]])
            visible_screen_names.append(category_screen_list[index])
            # Vérifie si l'écran a bien les 3 éléments nécessaires
            if (len(screen_data)) >= 3:
                # Si les 3 éléments sont présents, récupère leurs valeurs et les rajoutes
                visible_screen_activable.append(not not screen_data[0])
                visible_screen_minimum_wh.append([int(screen_data[1]), int(screen_data[2])])
            else:
                # Si les valeurs ne sont pas présentes, laisse un message d'erreur et rajoute des valeurs par défaut
                log.warning("Les caractéristiques de " + category_screen_list[index] + " ne sont pas bonnes.\n")
                visible_screen_activable.append(False)
                visible_screen_minimum_wh.append([0, 0])

        # Maintenant que toutes les valeurs ont été récupérés, les ajoutent à la partie graphique
        self.page.setProperty("screen_names", visible_screen_names)
        self.page.setProperty("screen_activable", visible_screen_activable)
        self.page.setProperty("minimum_wh", visible_screen_minimum_wh)
        self.page.setProperty("initial_settings", visible_screen_default_settings)

        # Rend visible et fonctionnel les boutons du bas pour changer de page d'écrans dans le cas
        if len(category_screen_list) > 4:
            left_button = self.page.findChild(QObject, "left_screen_button")
            left_button.setProperty("is_visible", True)
            left_button.setProperty("is_activable", self.screen_list_active > 0)
            right_button = self.page.findChild(QObject, "right_screen_button")
            right_button.setProperty("is_visible", True)
            right_button.setProperty("is_activable", (self.screen_list_active + 1) * 4 < len(category_screen_list))
        else:
            self.page.findChild(QObject, "left_screen_button").setProperty("is_visible", False)
            self.page.findChild(QObject, "right_screen_button").setProperty("is_visible", False)
