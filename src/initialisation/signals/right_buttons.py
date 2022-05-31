# Librairies par défaut
import sys
import os
import time


# Librairies graphiques
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.decorators as decorators
import src.misc.translation_dictionary as td
import src.initialisation.initialisation_window as ini


class RightButtons:
    """Classe s'occupant du chargement et du fonctionnement des boutons de droite de l'application d'initialisation"""

    # stocke les éléments de bases des boutons de droite
    right_buttons = None
    pages_stackview = None
    
    # Variables stockant les chemins d'accès vers le fichiers nécessaire au fonctionnement de la structure
    graphic_page_folder_path = f"{PROJECT_DIR}src\\initialisation\\graphics\\page_rb\\"
    logic_page_folder_path = f"{PROJECT_DIR}src\\initialisation\\signals\\page_rb\\"

    def __init__(self, application, translations):
        """
        Permet d'initialiser les 8 boutons permanents (rb1 -> rb8) situés à droite de la fenêtre.
        Connecte chaque bouton à sa page de paramètres associés

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        translations: `td.TranslationDictionary`
            traductions (clés = anglais -> valeurs = langue actuelle)
            Utile pour traduire les noms de dossiers et de fenêtres sauvegardés en anglais
        """
        # Récupère les boutons de droite à partir de la fenêtre
        self.right_buttons = application.win.findChild(QObject, "right_buttons")
        self.pages_stackview = application.win.findChild(QObject, "settings_pages")
        log.add_empty_lines()

        # Commence à indiquer toutes les fenêtres qui n'ont pas de fichiers graphiques associés
        not_exist = sorted({str(i + 1) for i in range(8)}.difference(f[7:-4]
                                                                     for f in os.listdir(self.graphic_page_folder_path)
                                                                     if f.startswith("page_rb") and f.endswith(".qml")))
        if not_exist:
            log.warning(f"Les pages de paramètres : {not_exist} N'ont aucun fichier graphique(.qml) associés.\n")

        # Pour toutes les pages de paramètres ayant un ficher graphique (.qml) existant
        for index in (int(f[7:-4]) for f in os.listdir(self.graphic_page_folder_path)
                      if f.startswith("page_rb") and f.endswith(".qml") and (1 <= int(f[7:-4]) <= 8)):
            # Vérifie si la partie graphique de la page existe et charge la page et le bouton associé
            engine = QQmlApplicationEngine()
            engine.load(f"{self.graphic_page_folder_path}page_rb{index}.qml")
            page_button = self.right_buttons.findChild(QObject, f"rb{index}")

            initial_time = time.perf_counter()
            log.change_log_prefix(f"Initialisation page_rb{index}")
            log.info(f"Tentative du chargement de la page_rb{index}.")

            # Essaye d'initialiser la page et si elle est correctement initialisé, tente de charger les signals
            if self.initialise_page(application, engine, index, page_button):
                if self.initialise_signals(application, engine, index, page_button, translations):
                    log.info(f"Chargement complet (graphique et fonctionnel) de la page_rb{index} en " +
                             f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.\n")
                else:
                    log.info(f"Chargement partiel (graphique uniquement) de la page_rb{index} en " +
                             f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.\n")

        log.change_log_prefix("Initialisation application d'initialisation")

    def initialise_page(self, application, engine, index, page_button):
        """Fonction permettant d'initialiser une des pages de l'application d'initialisation lié à un bouton de droite.
        Celle-ci sera initialiser si elle existe et qu'elle a un format valide

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        engine: `QQmlApplicationEngine`
            La QQmlApplicationEngine sur laquelle on a tenté de charger la page
        index: `int`
            index de la page (1 pour le bouton d'en haut -> 8 pour le bouton d'en bas
        page_button: `QObject`
            Le bouton auquel sera relié la page (généralement d'id : page_rb + index)

        Returns
        -------
        graphics_loaded: `bool`
            La partie graphique de la page a-t-elle été chargé correctement ?
        """
        # Si la page est chargée, alors elle existe et elle est ajoutée
        if engine.rootObjects():
            # Définit le bouton comme activable
            page_button.setProperty("is_activable", True)

            # Si c'est la première page existante, la charge
            if application.pages_list == [None] * 8:
                self.pages_stackview.set_active_page(engine.rootObjects()[0])
                application.active_page_index = index

            # store l'engine comme étant la page chargée
            application.pages_list[index - 1] = engine

            # Connect le bouton de droite à une fonction permettant de charger la page et d'appeler d'autres fonctions :
            # Une pour décharger la page active, et l'autre pour charger la nouvelle page
            page_button.clicked.connect(lambda new_page=engine, new_index=index:
                                           self.on_new_page_selected(application, new_page, new_index))
            return True
        else:
            # Sinon définit le bouton comme non activable et en négatif et enlève le potentiel texte
            page_button.setProperty("is_positive", False)
            page_button.setProperty("is_activable", False)
            page_button.setProperty("text", "")

            # Si le fichier n'a été chargé correctement
            log.warning(f"Le fichier graphique contient des erreurs :\n\t{self.graphic_page_folder_path}page_rb{index}.qml")
            return False

    def initialise_signals(self, application, engine, index, page_button, translations):
        """Permet lorsqu'une page de paramètres de l'application a été chargée, de charger les signals ainsi
        que des fonctions de bases (get_settings() et set_settings()) si celle-ci existe

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        engine: `QQmlApplicationEngine`
            La QQmlApplicationEngine sur laquelle on a tenté de charger la page
        index: `int`
            index de la page (1 pour le bouton d'en haut -> 8 pour le bouton d'en bas
        page_button: `QObject`
            Le bouton auquel sera relié la page (généralement d'id : page_rb + index)
        translations: `td.TranslationDictionary`
            traductions (clés = anglais -> valeurs = langue actuelle)
            Utile pour traduire les noms de dossiers et de fenêtres sauvegardés en anglais

        Returns
        -------
        logic_loaded: `bool`
            La partie fonctionnelle de la page a-t-elle été chargé correctement ?
        """
        # Vérifie si la page a des signals handlers associés (en recherchant un ficher .py associé)
        if os.path.isfile(f"{self.logic_page_folder_path}page_rb{index}.py"):
            # Si c'est le cas, initialise les signals handlers et le stock
            try:
                # Import localement le fichier de la page
                # Appelle le constructeur de la page pour affilier tous les signals aux widgets
                exec(f"from src.initialisation.signals.page_rb import page_rb{index} as rb{index}\n" +
                     f"application.pages_list[index - 1] = " +
                     f"rb{index}.PageRB{index}(application, engine, index, page_button, translations)")
            except Exception as error:
                # Permet de rattraper une erreur si le code est incorrect où qu'il ne suit pas la documentation
                log.warning(f"Erreur lors du chargement des signaux de la page_rb{index} :\n\t"
                            f"{self.logic_page_folder_path}page_rb{index}.py",
                            exception=error)
                return False
            else:
                # Vérifie (ou l'indique) si des fonctions manquent et rend le bouton relié à la page positif
                RightButtons.are_page_functions_there(application.pages_list[index - 1])
                page_button.setProperty("is_positive", True)
                return True
        else:
            # Sinon pas de signals handlers associé, le précise dans les logs
            log.warning(f"La page_rb{index} n'a pas de fichier signals. la page sera visible mais non fonctionnelle.")
            return False

    @staticmethod
    def are_page_functions_there(page):
        """Permet, à partir d'une page de paramètres correctement chargée, d'indiquer si toutes les fonctions
        potentiellement nécessaires au fonctionnement de celle-ci sont présentes.

        Parameters
        ----------
        page: `PageRBX`
            page à vérifier (celle-ci doit être de type PageRBX)
        """
        # Dans l'ordre : get_settings, set_settings, change_language, on_page_opened, on_page_closed
        for function in ["get_settings", "set_settings", "change_language", "on_page_opened", "on_page_closed"]:
            if function not in dir(page):
                log.debug(f"Aucune fonction \"{function}\" dans la page_rb{page.index}.")

    @decorators.QtSignal(log_level=log.Level.CRITICAL, end_process=True)
    def on_new_page_selected(self, application, engine, new_index):
        """Fonction permettant le changement de la page de paramètres active lorsqu'un bouton rb est cliqué
        Appelle aussi deux fonctions permettant le déchargement de la page actuelle et le chargement de la nouvelle page

        Parameters
        ----------
        application: `ini.InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        engine: `QQmlApplicationEngine`
            La QQmlApplicationEngine sur laquelle on a tenté de charger la page
        new_index: `int`
            index de la page de paramètre à charger (de 1 à 8)
        """
        # Vérifie que la page que l'on veut charger n'est pas celle qui est déjà chargée
        if new_index != application.active_page_index:
            # Si la page actuelle a une fonction de fermeture, l'appelle
            if "on_page_closed" in dir(application.pages_list[application.active_page_index - 1]):
                # Si c'est le cas, appelle la fonction de fermeture de la page
                application.pages_list[application.active_page_index - 1].on_page_closed(application)

            # Indique que l'on sort de l'ancienne page, change le préfixe et indique que l'on rentre dans la nouvelle page
            log.info(f"Fermeture de la page de paramètres page_rb{application.active_page_index}.\n")
            log.change_log_prefix(f"page_rb{new_index}")
            log.info(f"Ouverture de la page de paramètres page_rb{new_index}.")

            # Charge le graphique de la nouvelle page et indique à l'application l'index de la nouvelle page chargée
            self.pages_stackview.set_active_page(engine.rootObjects()[0])
            application.active_page_index = new_index

            # Si la nouvelle page a une fonction d'ouverture l'appelle
            if "on_page_opened" in dir(application.pages_list[application.active_page_index - 1]):
                # Si c'est le cas, appelle la fonction d'ouverture de la page
                application.pages_list[application.active_page_index - 1].on_page_opened(application)
