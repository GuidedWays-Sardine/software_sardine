import logging
import traceback

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


class PageRB5:
    """Class de la page de settings 5"""

    index = 5   # Attention dans les tableaux l'index comment à 0 donc index_tab = index - 1
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
    screen_list_index_active = 0
    visible_screen_names = []
    visible_screen_activable = []
    visible_screen_minimum_wh = []
    visible_screen_default_settings = []

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
        self.current_button.setProperty("text", "Écrans")

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
        self.page.setProperty("screenList", screen_list)
        self.page.setProperty("screenSize", screen_dimensions)

        # Définit le fonctionnement de base des boutons supérieurs et inférieurs
        # Aucun des boutons ne sera fonctionnel et aucune page ne sera chargée
        if len(self.screen_default.keys()) != 0:
            # Rend le texte supérieur en gris claire
            self.page.findChild(QObject, "category_title").setProperty("isDarkGrey", False)

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
            self.change_visible_screens()

            # S'il y a plus d'une catégorie d'écrans, rend les boutons supérieurs de catégories fonctionnels
            if len(self.screen_default.keys()) > 1:
                left_category_button = self.page.findChild(QObject, "left_category_button")
                left_category_button.clicked.connect(self.on_left_category_button_clicked)
                right_category_button = self.page.findChild(QObject, "right_category_button")
                right_category_button.setProperty("isActivable", True)
                right_category_button.clicked.connect(self.on_right_category_button_clicked)
        else:
            # Dans le cas où la liste des écrans à paramétrer est nulle
            self.page.findChild(QObject, "category_title").setProperty("isDarkGrey", True)
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
                # Met à jours les valeurs nécessaires
                self.screen_default["Simulateur SARDINE"]["Ligne virtuelle"][0] = page_rb1_data["Caméra"] == "False"
                self.screen_default["Simulateur SARDINE"]["Train caméra"][0] = page_rb1_data["Caméra"] == "True"
                self.screen_default["Poste de Commande Centralisé (PCC)"]["TCO"][0] = page_rb1_data["PCC"] == "True"
            except Exception as error:
                logging.warning("Erreur lors de la mise à jour des paramètres par défaut des écrans.\n\t\t" +
                                "Erreur de type : " + str(type(error)) + "\n\t\t" +
                                "Avec comme message d\'erreur : " + error.args[0] + "\n\n\t\t" +
                                "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
            else:
                # Remets à jour la page actuelle
                print("e") #TODO : appeller la fonction pour mettre à jour la page
                # FIXME : vérifier si rendre la apge inactive évite la page d'avoir des coordonnées
        else:
            # Si la page_rb1 n'est pas complètement chargée, laisse un message d'erreur
            logging.warning("La page_rb1 n'a pas été chargée complètement." +
                            " L'utilisation par défaut du simulateur sera prise en compte.\n")



        #TODO changer les différents écrans activables ou non

    def on_page_closed(self, application):
        for screen_index in self.screen_index:
            screen_index.hide()

    def on_left_category_button_clicked(self):
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        left_category_button = self.page.findChild(QObject, "left_category_button")
        category_title = self.page.findChild(QObject, "category_title")
        try:
            # Récupère l'index et le nom du nouvel élément
            new_index = list(self.screen_default.keys()).index(category_title.property("text")) - 1
            self.category_active = list(self.screen_default.keys())[new_index]
        except (IndexError, KeyError):
            # Si le nouvel élément n'a pas été trouvé, désactive le bouton et laisse un message d'erreur
            logging.debug("La catégorie d'écran n'a pas été trouvée.\n")
            left_category_button.setProperty("isActivable: false")
        else:
            # Si nouvel élément trouvé, change le titre de la catégorie.
            category_title.setProperty("text", self.category_active)

            # Appelle la fonction pour changer les écrans visibles
            self.change_visible_screens()

            # Rend le bouton de droite actif, et si première catégorie rend celui de gauche inactif
            self.page.findChild(QObject, "right_category_button").setProperty("isActivable", True)
            if new_index == 0:
                left_category_button.setProperty("isActivable", False)

    def on_right_category_button_clicked(self):
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        right_category_button = self.page.findChild(QObject, "right_category_button")
        category_title = self.page.findChild(QObject, "category_title")
        try:
            # Récupère l'index et le nom du nouvel élément
            new_index = list(self.screen_default.keys()).index(self.category_active) + 1
            self.category_active = list(self.screen_default.keys())[new_index]
        except (IndexError, KeyError):
            # Si le nouvel élément n'a pas été trouvé, désactive le bouton et laisse un message d'erreur
            logging.debug("La catégorie d'écran n'a pas été trouvée.\n")
            right_category_button.setProperty("isActivable: false")
        else:
            # Si nouvel élément trouvé, change le titre de la catégorie.
            category_title.setProperty("text", self.category_active)

            # Appelle la fonction pour changer les écrans visibles
            self.change_visible_screens()

            # Rend le bouton de gauche actif, et si dernière catégorie rend celui de droite inactif
            self.page.findChild(QObject, "left_category_button").setProperty("isActivable", True)
            if new_index == len(self.screen_default.keys()) - 1:
                right_category_button.setProperty("isActivable", False)

    def change_visible_screens(self):
        # Essaye de récupérer le dictionnaire des écrans de la catégorie sélectionnée
        try:
            category_screen_dict = self.screen_default[self.category_active]
            default_settings_dict = self.screen_settings[self.category_active]
        except KeyError:
            logging.error("Aucune catégorie d'écrans au nom de : " + self.category_active + ".\n")
        else:
            # Récupère les clés (nom des écrans) du dictionnaire récupéré (pour optimisation)
            category_screen_list = list(category_screen_dict.keys())

            # Vide les liste qui seront envoyés à la partie graphique
            self.visible_screen_names = []
            self.visible_screen_activable = []          # OPTIMIZE : pas nécessaire de les stocker comme objets de la classe
            self.visible_screen_minimum_wh = []
            self.visible_screen_default_settings = []

            # S'il y a plus de 4 écrans dans la catégorie, montre les 4 premiers sinon les montre tous
            for index in range(0, len(category_screen_list) if len(category_screen_list) <= 4 else 4):
                screen_data = category_screen_dict[category_screen_list[index]]
                self.visible_screen_default_settings.append(default_settings_dict[category_screen_list[index]])
                self.visible_screen_names.append(category_screen_list[index])
                # Vérifie si l'écran a bien les 3 éléments nécessaires
                if(len(screen_data)) >= 3:
                    # Si les 3 éléments sont présents, récupère leurs valeurs et les rajoutes
                    self.visible_screen_activable.append(not not screen_data[0])
                    self.visible_screen_minimum_wh.append([int(screen_data[1]), int(screen_data[2])])
                else:
                    # Si les valeurs ne sont pas présentes, laisse un message d'erreur et rajoute des valeurs par défaut
                    logging.warning("Les caractéristiques de " + category_screen_list[index] + " ne sont pas bonnes.\n")
                    self.visible_screen_activable.append(False)
                    self.visible_screen_minimum_wh.append([0, 0])

            # Maintenant que toutes les valeurs ont été récupérés, les ajoutent à la partie graphique
            self.page.setProperty("screenNames", self.visible_screen_names)
            self.page.setProperty("screenActivable", self.visible_screen_activable)
            self.page.setProperty("minimumWH", self.visible_screen_minimum_wh)
            self.page.setProperty("initialSettings", self.visible_screen_default_settings)

            # Remet l'index de la page d'écrans actif à 0
            self.screen_list_index_active = 0

            # Rend visible et fonctionnel les boutons du bas pour changer de page d'écrans dans le cas
            if len(category_screen_list) > 4:
                left_button = self.page.findChild(QObject, "left_screen_button")
                left_button.setProperty("isVisible", True)
                left_button.setProperty("isActivable", False)
                right_button = self.page.findChild(QObject, "right_screen_button")
                right_button.setProperty("isVisible", True)
                right_button.setProperty("isActivable", True)
            else:
                self.page.findChild(QObject, "left_screen_button").setProperty("isVisible", False)
                self.page.findChild(QObject, "right_screen_button").setProperty("isVisible", False)

    def on_left_screen_button_pressed(self):
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        # Diminue l'index et rend le bouton de droite actif
        self.screen_list_index_active -= 1
        self.page.findChild(QObject, "right_screen_button").setProperty("isActivable", True)

        # Vide les liste qui seront envoyés à la partie graphique
        self.visible_screen_names = []
        self.visible_screen_activable = []
        self.visible_screen_minimum_wh = []
        self.visible_screen_default_settings = []

        # Récupère le dictionaire relié à la catégorie visible et récupère les écrans (clés) de cette catégorie
        category_screen_dict = self.screen_default[self.category_active]
        default_settings_dict = self.screen_settings[self.category_active]
        category_screen_list = list(category_screen_dict.keys())
        for index in range(self.screen_list_index_active * 4,
                           len(category_screen_list) if len(category_screen_list) <= (self.screen_list_index_active + 1) * 4
                           else 4 * (self.screen_list_index_active + 1)):
            screen_data = category_screen_dict[category_screen_list[index]]
            self.visible_screen_default_settings.append(default_settings_dict[category_screen_list[index]])
            self.visible_screen_names.append(category_screen_list[index])
            # Vérifie si l'écran a bien les 3 éléments nécessaires
            if (len(screen_data)) >= 3:
                # Si les 3 éléments sont présents, récupère leurs valeurs et les rajoutes
                self.visible_screen_activable.append(not not screen_data[0])
                self.visible_screen_minimum_wh.append([int(screen_data[1]), int(screen_data[2])])
            else:
                # Si les valeurs ne sont pas présentes, laisse un message d'erreur et rajoute des valeurs par défaut
                logging.warning("Les caractéristiques de " + category_screen_list[index] + " ne sont pas bonnes.\n")
                self.visible_screen_activable.append(False)
                self.visible_screen_minimum_wh.append([0, 0])

        # Maintenant que toutes les valeurs ont été récupérés, les ajoutent à la partie graphique
        self.page.setProperty("screenNames", self.visible_screen_names)
        self.page.setProperty("screenActivable", self.visible_screen_activable)
        self.page.setProperty("minimumWH", self.visible_screen_minimum_wh)
        self.page.setProperty("initialSettings", self.visible_screen_default_settings)

        # Vérifie maintenant s'il y a encore des écrans sur la page d'après, sinon désactive le bouton
        if self.screen_list_index_active == 0:
            self.page.findChild(QObject, "left_screen_button").setProperty("isActivable", False)

    def on_right_screen_button_pressed(self):
        # Récupère les valeurs actuellement sur l'écran
        old_screens_values = self.page.get_values().toVariant()
        for index in range(0, len(old_screens_values)):
            self.screen_settings[self.category_active][old_screens_values[index][0]] = old_screens_values[index][1]

        # Augmente l'index de la page de 1 (pour suivre les écrans à montrer), et active le bouton de gauche
        self.screen_list_index_active += 1
        self.page.findChild(QObject, "left_screen_button").setProperty("isActivable", True)

        # Vide les liste qui seront envoyés à la partie graphique
        self.visible_screen_names = []
        self.visible_screen_activable = []
        self.visible_screen_minimum_wh = []
        self.visible_screen_default_settings = []

        # Récupère le dictionaire relié à la catégorie visible et récupère les écrans (clés) de cette catégorie
        category_screen_dict = self.screen_default[self.category_active]
        default_settings_dict = self.screen_settings[self.category_active]
        category_screen_list = list(category_screen_dict.keys())
        for index in range(self.screen_list_index_active * 4,
                           len(category_screen_list) if len(category_screen_list) <= (self.screen_list_index_active + 1) * 4
                           else 4 * (self.screen_list_index_active + 1)):
            screen_data = category_screen_dict[category_screen_list[index]]
            self.visible_screen_default_settings.append(default_settings_dict[category_screen_list[index]])
            self.visible_screen_names.append(category_screen_list[index])
            # Vérifie si l'écran a bien les 3 éléments nécessaires
            if (len(screen_data)) >= 3:
                # Si les 3 éléments sont présents, récupère leurs valeurs et les rajoutes
                self.visible_screen_activable.append(not not screen_data[0])
                self.visible_screen_minimum_wh.append([int(screen_data[1]), int(screen_data[2])])
            else:
                # Si les valeurs ne sont pas présentes, laisse un message d'erreur et rajoute des valeurs par défaut
                logging.warning("Les caractéristiques de " + category_screen_list[index] + " ne sont pas bonnes.\n")
                self.visible_screen_activable.append(False)
                self.visible_screen_minimum_wh.append([0, 0])

        # Maintenant que toutes les valeurs ont été récupérés, les ajoutent à la partie graphique
        self.page.setProperty("screenNames", self.visible_screen_names)
        self.page.setProperty("screenActivable", self.visible_screen_activable)
        self.page.setProperty("minimumWH", self.visible_screen_minimum_wh)
        self.page.setProperty("initialSettings", self.visible_screen_default_settings)

        # Vérifie maintenant s'il y a encore des écrans sur la page d'après, sinon désactive le bouton
        if len(category_screen_list) <= (self.screen_list_index_active + 1) * 4:
            self.page.findChild(QObject, "right_screen_button").setProperty("isActivable", False)


#TODO faire les fonctions pour récupérer les valeurs de la partie graphique
#TODO faire le get_values
#TODO faire le set_values
#TODO faire le change_language
