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
    screen_default = {"Simulateur SARDINE": {"DMI central":     [True, 640, 480],
                                             "DMI gauche":      [True, 640, 480],
                                             "Ligne virtuelle": [True, 1080, 720],
                                             "Train caméra":    [False, 640, 480]
                                             },
                      "Poste de Commande Centralisé (PCC)": {"Tableau de Contrôle Optique (TCO)":   [False, 640, 480]
                                                             },
                      "Visualisation des données": {"Courbes": [False, 0, 0]
                                                    }
                      }
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

        # Définit le fonctionnement de base des boutons supérieurs et inférieurs
        # Aucun des boutons ne sera fonctionnel et aucune page ne sera chargée
        if len(self.screen_default.keys()) != 0:
            # Rend le texte supérieur en gris claire
            self.page.findChild(QObject, "category_title").setProperty("is_dark_grey", False)

            # Change le nom de la catégorie pour la première catégorie d'écrans (pour initialiser une page)
            self.category_active = list(self.screen_default.keys())[0]
            self.page.findChild(QObject, "category_title").setProperty("text", self.category_active)

            # Rend fonctionnel les boutons inférieurs (visibles et activable que quand nécessaire)
            self.page.findChild(QObject, "left_screen_button").clicked.connect(self.on_left_screen_button_pressed)
            self.page.findChild(QObject, "right_screen_button").clicked.connect(self.on_right_screen_button_pressed)

            # Initialise les résultats (mets tout à blanc)
            for category_key in list(self.screen_default.keys()):
                temp_category = {}
                for screen_key in list(self.screen_default[category_key].keys()):
                    temp_category[screen_key] = [0, False, [0, 0], [0, 0]]
                self.screen_settings[category_key] = temp_category
            self.change_visible_screen_list()

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

        # Commence par les éléments de la page 1
        if application.visible_pages[0] is not None and not isinstance(application.visible_pages[0], type(self.engine)):
            # camera_check pour ligne virtuelle ou train caméra
            application.visible_pages[0].page.findChild(QObject, "camera_check").value_changed.connect(lambda: self.on_camera_train_checked(application))
            self.on_camera_train_checked(application)

            # pcc_check pour TCO et toute autre fenêtre nécessaire au fonctionnement du PCC
            application.visible_pages[0].page.findChild(QObject, "pcc_check").value_changed.connect(lambda: self.on_pcc_checked(application))
            self.on_pcc_checked(application)

            # data_check pour l'affichage des données en direct
            application.visible_pages[0].page.findChild(QObject, "data_check").value_changed.connect(lambda: self.on_data_checked(application))
            self.on_data_checked(application)
        else:
            log.warning("Certains paramétrages d'écrans dépendent du bon fonctionnement de la page_rb1." +
                        "Ceux-ci ne peucent pas se charger correctement.\n")

        # Définit la page comme validée (toutes les valeurs par défaut suffisent)
        application.is_completed_by_default[self.index - 1] = "is_page_valid" not in dir(self)

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
        # Récupère si le checkbutton est activé, le nom de la catégorie et des écrans à modifier
        is_checked = application.visible_pages[0].page.findChild(QObject, "data_check").property("is_checked")
        category = list(self.screen_default.keys())[2]
        screen_data = list(self.screen_default[category].keys())[0]

        # Change la paramétrabilité des écrans souhaités
        self.screen_default[category][screen_data][0] = is_checked

        # Réinitialise les paramètres de ces écrans s'ils ne sont plus paramétrables
        if not self.screen_default[category][screen_data][0]:
            self.screen_settings[category][screen_data] = [0, False, [0, 0], [0, 0]]

    def get_values(self, translation_data): # TODO : à optimiser avec les différents dictionnaires personalisés
        """Récupère les paramètres de la page de paramètres page_rb8

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive

        Returns
        -------
        parameters : `dictionary`
            un dictionaire de paramètres de la page de paramètres page_rb8
        """
        # Initialise les paramètres récupérés et récupère le paramètre sur si les écrans sont éteins
        page_parameters = {"EcransEteints": self.page.findChild(QObject, "black_screens_check").property("is_checked")}

        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        # Pour chaque catégorie d'écrans
        for category_key in list(self.screen_settings.keys()):
            # Pour chaque écrans de cette catégorie
            for screen_key in list(self.screen_settings[category_key].keys()):
                # Sauvegarde chaque donné au format : category.screen.data = value
                try:
                    screen_settings_key = translation_data[category_key] + "."
                except KeyError:
                    log.debug("Traduction de " + category_key + " manquante.\n")
                    screen_settings_key = category_key + "."
                try:
                    screen_settings_key += translation_data[screen_key] + "."
                except KeyError:
                    log.debug("Traduction de " + screen_key + " manquante.\n")
                    screen_settings_key += screen_key + "."

                # Récupère les paramètres de l'écran et les sauvegardes (dépend de si l'écran est sélectionable ou non
                is_activable = self.screen_default[category_key][screen_key][0]
                screen_settings_values = self.screen_settings[category_key][screen_key]
                page_parameters[screen_settings_key + "IndexEcran"] = screen_settings_values[0] if is_activable else 0
                page_parameters[screen_settings_key + "PleinEcran"] = screen_settings_values[1] if is_activable else False
                page_parameters[screen_settings_key + "positionX"] = screen_settings_values[2][0] if is_activable else 0
                page_parameters[screen_settings_key + "positionY"] = screen_settings_values[2][1] if is_activable else 0
                page_parameters[screen_settings_key + "tailleX"] = screen_settings_values[3][0] if is_activable else 0
                page_parameters[screen_settings_key + "tailleY"] = screen_settings_values[3][1] if is_activable else 0

        return page_parameters

    def set_values(self, data, translation_data):
        """A partir d'un dictionnaire de valeur, essaye de changer les settings de la page de paramètres 8

        Parameters
        ----------
        data: `dict`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive
        """
        # Change la valeur pour les écrans noirs
        try:
            self.page.findChild(QObject, "black_screens_check").setProperty("is_checked", data["EcransEteints"])
        except KeyError:
            log.debug("Aucune données EcransEteints dans le fichier paramètres ouverts.\n")

        # Inverse les données de traduction pour avoir un dictionnaire langue actuelle -> Français
        translation_data = dict([reversed(i) for i in translation_data.items()])

        # Pour chaque catégorie d'écrans
        for category_key in list(self.screen_settings.keys()):
            # Pour chaque écrans de cette catégorie
            for screen_key in list(self.screen_settings[category_key].keys()):
                # Sauvegarde chaque donné au format : category.screen.data = value
                try:
                    screen_settings_key = translation_data[category_key] + "."
                except KeyError:
                    log.debug("Traduction de " + category_key + " manquante.\n")
                    screen_settings_key = category_key + "."
                try:
                    screen_settings_key += translation_data[screen_key] + "."
                except KeyError:
                    log.debug("Traduction de " + screen_key + " manquante.\n")
                    screen_settings_key += screen_key + "."

                # Essaye de récupérer les donnés reliés à l'écran
                try:
                    if int(data[screen_settings_key + "IndexEcran"]) <= self.screen_count:
                        self.screen_settings[category_key][screen_key][0] = int(data[screen_settings_key + "IndexEcran"])
                        self.screen_settings[category_key][screen_key][1] = data[screen_settings_key + "PleinEcran"] == "True"
                        self.screen_settings[category_key][screen_key][2][0] = int(data[screen_settings_key + "positionX"])
                        self.screen_settings[category_key][screen_key][2][1] = int(data[screen_settings_key + "positionY"])
                        self.screen_settings[category_key][screen_key][3][0] = int(data[screen_settings_key + "tailleX"])
                        self.screen_settings[category_key][screen_key][3][1] = int(data[screen_settings_key + "tailleY"])
                except KeyError:
                    log.debug("L'écran : " + screen_settings_key + " n'a pas de paramètres sauvegardés.\n")

        # Met à jour la page visible de settings
        self.change_visible_screen_list()

    def change_language(self, translation_data):    # TODO : améliorer avec le dictionnaire de traduction
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de la page de paramètres

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive
        """
        # Traduit le nom de la catégorie
        try:
            self.current_button.setProperty("text", translation_data[self.current_button.property("text")])
        except KeyError:
            log.debug("Impossible de traduire le nom de la catégorie de la page_rb8.\n")

        # Change la traduction pour le texte Plein écran ? du DMI_checkbutton
        try:
            self.page.setProperty("fullscreen_text", translation_data[self.page.property("fullscreen_text")])
        except KeyError:
            log.debug("Traduction manquante pour : " + self.page.property("fullscreen_text") + ".\n")

        # Pour chaque catégories
        for category_index in list(self.screen_default.keys()):
            # Pour chaque écrans de chaques catégories
            for screen_index in list(self.screen_default[category_index].keys()):
                try:
                    # Essaye de rajouter la version avec la clé traduite de l'écran
                    self.screen_default[category_index][translation_data[screen_index]] = self.screen_default[category_index][screen_index]
                    self.screen_settings[category_index][translation_data[screen_index]] = self.screen_settings[category_index][screen_index]
                except KeyError:
                    # Récupère dans l'éventualité d'une traduction manquante
                    log.debug("Traduction manquante pour l'écran : " + screen_index +
                                  " de la catégorie : " + category_index + ", traduction sautée.\n")
                else:
                    # Si les écrans traduites ont été rajoutés avec succès enlève les versions non traduites
                    self.screen_default[category_index].pop(screen_index)
                    self.screen_settings[category_index].pop(screen_index)

            try:
                # Essaye de traduire le nom de la catégorie
                self.screen_default[translation_data[category_index]] = self.screen_default[category_index]
                self.screen_settings[translation_data[category_index]] = self.screen_settings[category_index]
            except KeyError:
                # Récupère dans l'éventualité d'une traduction manquante
                log.debug("Traduction manquante pour la catégorie : " + category_index + ", traduction sautée.\n")
            else:
                # Si les catégories traduites ont été rajoutés avec succès enlève les versions non traduites
                self.screen_default.pop(category_index)
                self.screen_settings.pop(category_index)

                # Si la catégorie est la catégorie active, traduit la catégorie active
                if self.category_active == category_index:
                    self.category_active = translation_data[self.category_active]

        # Traduit le texte devant le DMI_checkbutton pour savoir
        try:
            black_screens_check = self.page.findChild(QObject, "black_screens_check")
            black_screens_check.setProperty("text", translation_data[black_screens_check.property("text")])
        except KeyError:
            log.debug("Traduction manquante pour : " + black_screens_check.property("text") + ", traduction sautée.\n")

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
