import logging
import traceback

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


class PageRB5:
    """Class de la page de settings 5"""

    index = 5   # Attention dans les tableaux l'index comment à 0 donc index_tab = index - 1
    name = "Écrans"
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
                      "Poste de Commande Centralisé (PCC)": {"Tableau de Contrôle Optique (TCO)":   [True, 640, 480]
                                                             },
                      "Visualisation des données": {"Courbes": [True, 0, 0]
                                                    }
                      }
    screen_settings = {}
    category_active = ""
    screen_list_active = 0

    def __init__(self, application, page, index, current_button):
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
            Le bouton auquel sera relié la page (généralement d'id : page_rb + index)"""
        # Stocke les informations nécessaires au fonctionnement de la page
        self.index = index
        self.page = page
        self.current_button = current_button
        self.current_button.setProperty("text", self.name)

        # Récupère le nombre d'écrans présents
        self.screen_count = QDesktopWidget().screenCount()
        self.screen_index = [None] * self.screen_count
        logging.info("[page_rb5] : " + str(self.screen_count) + " écrans détectés.\n")

        # Charge autant de fenêtres d'index d'écrans qu'il y a d'écrans
        for screen_index in range(0, self.screen_count):
            application.engine.load('initialisation/graphics/page_rb/page_rb5/screen_index.qml')
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
            window = self.screen_index[screen_index].findChild(QObject, "screen_index")
            window.setProperty("text", str(screen_index + 1))
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
                left_category_button.clicked.connect(self.on_left_category_button_clicked)
                right_category_button = self.page.findChild(QObject, "right_category_button")
                right_category_button.setProperty("is_activable", True)
                right_category_button.clicked.connect(self.on_right_category_button_clicked)
        else:
            # Dans le cas où la liste des écrans à paramétrer est nulle
            self.page.findChild(QObject, "category_title").setProperty("is_dark_grey", True)
            self.page.findChild(QObject, "category_title").setProperty("text", "Aucun écran à paramétrer")
            raise NameError("Aucun écran à paramétrer. Le dictionnaire \"screen_default\" est vide.")

        # Définit la page comme complète
        application.is_completed[4] = True

    def on_page_opened(self, application):
        """Fonction appelée lorsque la page est chargée. Permet d'afficher les fenêtre d'index
        et actualise les paramètres des écrans"""
        # Rend visible tous les écrans d'index
        for screen_index in self.screen_index:
            screen_index.show()

        # Vérifie que tous les écrans peuvent être sélectionnés
        if application.visible_pages[0] is not None \
                and not isinstance(application.visible_pages[0], type(application.engine)) \
                and "get_values" in dir(application.visible_pages[0]):
            # Récupère les données actuelles de la page de paramètres page_rb1
            page_rb1_data = application.visible_pages[0].get_values(application.read_language_file(application.language,
                                                                                                   "English"))
            try:
                category_list = list(self.screen_default.keys())
                # Met à jours les valeurs nécessaires (self.screen_default[category][screen][0]
                self.screen_default[category_list[0]][list(self.screen_default[category_list[0]].keys())[2]][0] \
                    = not page_rb1_data["Caméra"]
                self.screen_default[category_list[0]][list(self.screen_default[category_list[0]].keys())[3]][0] \
                    = page_rb1_data["Caméra"]
                self.screen_default[category_list[1]][list(self.screen_default[category_list[1]].keys())[0]][0] \
                    = page_rb1_data["PCC"]
            except Exception as error:
                logging.warning("Erreur lors de la mise à jour des paramètres par défaut des écrans.\n\t\t" +
                                "Erreur de type : " + str(type(error)) + "\n\t\t" +
                                "Avec comme message d\'erreur : " + error.args[0] + "\n\n\t\t" +
                                "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
        else:
            # Si la page_rb1 n'est pas complètement chargée, laisse un message d'erreur
            logging.warning("La page_rb1 n'a pas été chargée complètement." +
                            " L'utilisation par défaut du simulateur sera prise en compte.\n")

        # Remets à jour la page actuelle
        self.change_visible_screen_list()

    def on_page_closed(self, application):
        """Fonction appelée quand la page est fermée."""
        # Cache toutes les fenêtres d'index
        for screen_index in self.screen_index:
            screen_index.hide()

        # récupère les valeurs des écrans actuels et les sauvegarde
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

    def on_left_category_button_clicked(self):
        """signal appelé quand le bouton de changement de catégorie est appuyé. Met à jour la catégorie et ses écrans"""
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
        """signal appelé quand le bouton de changement de catégorie est appuyé. Met à jour la catégorie et ses écrans"""
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

    def change_visible_screen_list(self):
        """met à jour la liste d'écrans à rendre visible. A appeler dans le cas où la catégorie
         ou la liste d'écrans sont changés ou quand des paramètres sont mis à jour en python"""
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
                logging.warning("Les caractéristiques de " + category_screen_list[index] + " ne sont pas bonnes.\n")
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

    def on_left_screen_button_pressed(self):
        """Signal appelé lorsque le bouton permettant de changer les écrans d'une catégorie visible."""
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        # Diminue l'index de la liste d'écrans et appelle la fonction pour changer les écrans à paramétrer
        self.screen_list_active -= 1
        self.change_visible_screen_list()

    def on_right_screen_button_pressed(self):
        """Signal appelé lorsque le bouton permettant de changer les écrans d'une catégorie visible."""
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        # Augmente l'index de la liste d'écrans et appelle la fonction pour changer les écrans à paramétrer
        self.screen_list_active += 1
        self.change_visible_screen_list()

    def get_values(self, translation_data):
        """Récupère les paramètres de la page de paramètres page_rb5

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive

        Returns
        -------
        parameters : `dictionary`
            un dictionaire de paramètres de la page de paramètres page_rb5
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
                    logging.debug("Traduction de " + category_key + " manquante.\n")
                    screen_settings_key = category_key + "."
                try:
                    screen_settings_key += translation_data[screen_key] + "."
                except KeyError:
                    logging.debug("Traduction de " + screen_key + " manquante.\n")
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
        """A partir d'un dictionnaire de valeur, essaye de changer les settings des différentes pages

        Parameters
        ----------
        data: `dict`
            Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive"""
        # Change la valeur pour les écrans noirs
        try:
            self.page.findChild(QObject, "black_screens_check").setProperty("is_checked", data["EcransEteints"])
        except KeyError:
            logging.debug("Aucune données EcransEteints dans le fichier paramètres ouverts.\n")

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
                    logging.debug("Traduction de " + category_key + " manquante.\n")
                    screen_settings_key = category_key + "."
                try:
                    screen_settings_key += translation_data[screen_key] + "."
                except KeyError:
                    logging.debug("Traduction de " + screen_key + " manquante.\n")
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
                    logging.debug("L'écran : " + screen_settings_key + " n'a pas de paramètres sauvegardés.\n")

        # Met à jour la page visible de settings
        self.change_visible_screen_list()

    def change_language(self, translation_data):
        """Permet à partir d'un dictionaire de traduction, de traduire les textes de la page de paramètres

        Parameters
        ----------
        translation_data: `dict`
            dictionaire de traduction (clés = langue actuelle -> valeurs = nouvelle langue) case sensitive"""
        # Traduit le nom de la catégorie
        try:
            self.current_button.setProperty("text", translation_data[self.current_button.property("text")])
        except KeyError:
            logging.debug("Impossible de traduire le nom de la catégorie de la page_rb5.\n")

        # Change la traduction pour le texte Plein écran ? du DMI_checkbutton
        try:
            self.page.setProperty("fullscreen_text", translation_data[self.page.property("fullscreen_text")])
        except KeyError:
            logging.debug("Traduction manquante pour : " + self.page.property("fullscreen_text") + ".\n")

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
                    logging.debug("Traduction manquante pour l'écran : " + screen_index +
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
                logging.debug("Traduction manquante pour la catégorie : " + category_index + ", traduction sautée.\n")
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
            logging.debug("Traduction manquante pour : " + black_screens_check.property("text") + ", traduction sautée.\n")

        # Remets à jour la page actuelle et le titre de la catégorie
        self.page.findChild(QObject, "category_title").setProperty("text", self.category_active)
        self.change_visible_screen_list()
