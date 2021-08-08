import logging
import os
import traceback
import time

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


class RightButtons:

    # stocke les éléments de bases des boutons de droite
    right_buttons = None
    pages_stackview = None

    def __init__(self, application):
        """
        Permet d'initialiser les 8 boutons permanents (rb1 -> rb8) situés à droite de la fenêtre.
        Connecte chaque bouton à sa page de paramètres associés

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Récupère les boutons de droite à partir de la fenêtre
        self.right_buttons = application.win.findChild(QObject, "right_buttons")
        self.pages_stackview = application.win.findChild(QObject, "settings_pages")

        # Pour les 8 boutons de droite
        for index in range(1, 9):
            # Vérifie si la partie graphique de la page existe et charge la page et le bouton associé
            engine = QQmlApplicationEngine()
            page_path = "initialisation/graphics/page_rb/page_rb" + str(index) + ".qml"  # Par rapport au main.py
            engine.load(page_path)
            current_button = self.right_buttons.findChild(QObject, "rb" + str(index))

            # Essaye d'initialiser la page et si elle est correctement initialisé, tente de charger les signals
            initial_time = time.time()
            if self.initialise_page(application, engine, index, page_path, current_button):
                if self.initialise_signals(application, engine, index, page_path, current_button):
                    logging.info("Chargement complet (graphique et fonctionelle) de la  page " + str(index) +
                                 " en " + str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n")
                else:
                    logging.info("Chargement partiel (graphique uniquement) de la page " + str(index) +
                                 " en " + str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n")

        # Vérifie si au moins une page est chargée, sinon l'indique et cache les boutons ouvrir et sauvegarder
        if not any(application.is_fully_loaded):
            logging.error("Aucune des pages n'a été correctement chargée. Les valeurs par défaut seront utilisés.\n\t\t"
                          + "Seuls les boutons quitter et lancer sont fonctionnels.\n\t\t"
                          + "Veuillez lire les warnings ci-dessus pour comprendre la cause du problème et le régler.\n")
            save_button = application.win.findChild(QObject, "sauvegarder")
            if save_button is not None:
                save_button.setProperty("isVisible", False)
            open_button = application.win.findChild(QObject, "ouvrir")
            if open_button is not None:
                open_button.setProperty("isVisible", False)

    def initialise_page(self, application, engine, index, page_path, current_button):
        """Fonction permettant d'initialiser une des pages de l'application d'initialisation lié à un bouton de droite.
        Celle-ci sera initialiser si elle existe et qu'elle a un format valide

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        engine: `QQmlApplicationEngine`
            La QQmlApplicationEngine sur laquelle on a tenté de charger la page
        index: `int`
            index de la page (1 pour le bouton d'en haut -> 8 pour le bouton d'en bas
        page_path: `string`
            Chemin vers la page de widgets stocké(.qml) à charger (par rapport au main.py)
        current_button: `QObject`
            Le bouton auquel sera relié la page (généralement d'id : page_rb + index)

        Returns
        -------
        graphics_loaded: `bool`
            La partie graphique de la page a-t-elle été chargé correctement ?
        """
        # Si la page est chargée, alors elle existe et elle est ajoutée
        if engine.rootObjects():
            # Définit le bouton comme activable
            current_button.setProperty("isActivable", True)

            # Si c'est la première page existante, la charge
            if application.visible_pages == [None] * 8:
                self.pages_stackview.set_active_page(engine.rootObjects()[0])
                application.active_settings_page = index

            # store l'engine comme étant la page chargée
            application.visible_pages[index - 1] = engine

            # Connect le bouton de droite à une fonction permettant de charger la page et d'appeler d'autres fonctions :
            # Une pour décharger la page active, et l'autre pour charger la nouvelle page
            current_button.clicked.connect(lambda new_page=engine, new_index=index:
                                           self.on_new_page_selected(application, new_page, new_index))
            return True
        else:
            # Sinon définit le bouton comme non activable et en négatif et enlève le potentiel texte
            current_button.setProperty("isPositive", False)
            current_button.setProperty("isActivable", False)
            current_button.setProperty("text", "")

            # Si le fichier existe mais n'a pas été ouvert, cela veut dire qu'il y a une erreur dans le fichier
            if os.path.isfile(page_path):
                logging.warning("le chargement de la page " + str(index) +
                                " relié au bouton rb" + str(index) + " est impossible.\n\t\t" +
                                "Le fichier " + page_path + " existe mais ne se charge pas correctement.\n\t\t" +
                                "Assurez-vous que celui-ci ne contient pas d'erreurs.\n")
            # Sinon c'est qu'il n'existe pas où qu'il est mal placé
            else:
                logging.warning("le chargement de la page " + str(index) +
                                " relié au bouton rb" + str(index) + " est impossible.\n\t\t" +
                                "Le fichier " + page_path + " n'existe pas.\n\t\t" +
                                "Assurez-vous que le fichier source est au bon endroit ou créez le\n")
            return False

    def on_new_page_selected(self, application, engine, new_index):
        """Fonction permettant le changement de la page de paramètres active lorsqu'un bouton rb est cliqué
        Appelle aussi deux fonctions permettant le déchargement de la page actuelle et le chargement de la nouvelle page

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        engine: `QQmlApplicationEngine`
            La QQmlApplicationEngine sur laquelle on a tenté de charger la page
        new_index: `int`
            index de la page de paramètre à charger (de 1 à 8)
        """
        # Vérifie que la page que l'on veut charger n'est pas celle qui est déjà chargée
        if new_index != application.active_settings_page:
            if application.is_fully_loaded[application.active_settings_page - 1]:
                # Vérifie si la page que l'on va décharger a un protocole de déchargement spécifique
                if "on_page_closed" in dir(application.visible_pages[application.active_settings_page - 1]):
                    try:
                        application.visible_pages[application.active_settings_page - 1].on_page_closed(application)
                    except Exception as error:
                        logging.error("La fonction on_page_closed de la page " + str(application.active_settings_page)
                                      + " contient une erreur\n\t\t" +
                                      "Erreur de type : " + str(type(error)) + "\n\t\t" +
                                      "Avec comme message d\'erreur : " + error.args[0] + "\n\n\t\t" +
                                      "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
                else:
                    logging.debug("Aucune fonction on_page_closed page " + str(application.active_settings_page) + "\n")

            # Charge le graphique de la nouvelle page et indique à l'application l'index de la nouvelle page chargée
            self.pages_stackview.set_active_page(engine.rootObjects()[0])
            application.active_settings_page = new_index

            if application.is_fully_loaded[application.active_settings_page - 1]:
                # Vérifie si la page que l'on charge  a un protocole de chargement particulier
                if "on_page_opened" in dir(application.visible_pages[application.active_settings_page - 1]):
                    try:
                        application.visible_pages[application.active_settings_page - 1].on_page_opened(application)
                    except Exception as error:
                        logging.error("La fonction on_page_opened de la page " + str(application.active_settings_page) +
                                      " contient une erreur.\n\t\t" +
                                      "Erreur de type : " + str(type(error)) + "\n\t\t" +
                                      "Avec comme message d\'erreur : " + error.args[0] + "\n\n\t\t" +
                                      "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
                else:
                    logging.debug("Aucune fonction on_page_opened page " + str(application.active_settings_page) + "\n")

    def initialise_signals(self, application, engine, index, page_path, current_button):
        """Permet lorsqu'une page de paramètres de l'application a été chargée, de charger les signals ainsi
        que des fonctions de bases (get_values() et set_values()) si celle-ci existe

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        engine: `QQmlApplicationEngine`
            La QQmlApplicationEngine sur laquelle on a tenté de charger la page
        index: `int`
            index de la page (1 pour le bouton d'en haut -> 8 pour le bouton d'en bas
        page_path: `string`
            Chemin vers la page de widgets (.qml) à charger (par rapport au main.py)
        current_button: `QObject`
            Le bouton auquel sera relié la page (généralement d'id : page_rb + index)

        Returns
        -------
        logic_loaded: `bool`
            La partie fonctionnelle de la page a-t-elle été chargé correctement ?
        """
        # Vérifie si la page a des signals handlers associés (en recherchant un ficher .py associé)
        if os.path.isfile("initialisation/signals/page_rb/page_rb" + str(index) + ".py"):
            # Si c'est le cas, initialise les signals handlers et le stock
            try:
                # Import localement le fichier de la page
                # Appelle le constructeur de la page pour affilier tous les signals aux widgets
                exec("from initialisation.signals.page_rb import page_rb" + str(index) + " as rb" + str(index) + "\n" +
                     "application.visible_pages[index - 1] = " +
                     "(rb" + str(index) + ".PageRB" + str(index) + "(application, engine, index, current_button))")

                # Indique que la page a entièrement été chargée (partie visuelle et signals)
                application.is_fully_loaded[index - 1] = True
                current_button.setProperty("isPositive", True)
                return True
            except Exception as error:
                # Permet de rattraper une erreur si le code est incorrect où qu'il ne suit pas la documentation
                logging.warning("Erreur lors du chargement des signaux de la page : " + page_path + ".\n\t\t" +
                                "Erreur de type : " + str(type(error)) + "\n\t\t" +
                                "Avec comme message d\'erreur : " + error.args[0] +
                                ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '\n\t\t') + "\n")
                current_button.setProperty("isPositive", False)
                return False
        else:
            # Sinon pas de signals handlers associé, le précise dans les logs
            logging.warning("La page " + str(index) + " n\'a aucun fichier signals associé.\n\t\t" +
                            "La page sera visible mais ne sera pas fonctionnelle.\n")
            current_button.setProperty("isPositive", False)
            return False
