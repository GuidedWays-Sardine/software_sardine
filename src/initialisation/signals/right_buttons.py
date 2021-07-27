import logging
import os
import traceback

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


class RightButtons:

    #stoque les éléments de bases des boutons de droite
    right_buttons = None
    pages_stackview = None

    # Stoque si la page est chargée et si elle est complète (pour lancer le simulateur
    visible_pages = [None] * 8     # Stoque les pages que l'utilisateur peut afficher
    is_fully_loaded = [False] * 8  # Stoque directement l'instance de la classe
    is_completed = [False] * 8     # Détecte si la page est complété (égale à self.visible_pages si tout est complété)

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
            self.initialise_page(engine, index, page_path, current_button)

    def initialise_page(self, engine, index, page_path, current_button):
        """Fonction permettant d'initialiser une des pages de l'application d'initialisation lié à un bouton de droite.
        Celle-ci sera initialiser si elle existe et qu'elle a un format valide

        Parameters
        ----------
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
        page_loaded: `bool`
            La page a-t-elle été chargé correctement ?
        """
        # Si la page est chargée, alors elle existe et elle est ajoutée
        if engine.rootObjects():
            # Définit le bouton comme activable
            current_button.setProperty("isActivable", True)

            # Si c'est la première page existante, la charge
            if self.visible_pages == [None] * 8:
                self.pages_stackview.set_active_page(engine.rootObjects()[0])

            # store l'engine comme étant la page chargée
            self.visible_pages[index - 1] = engine

            # Connecte le bouton de droite correspondant pour charger la page
            current_button.clicked.connect(lambda new_page=engine:
                                           self.pages_stackview.set_active_page(new_page.rootObjects()[0]))
        else:
            # Sinon définit le bouton comme non activable et enlève le potentiel texte
            current_button.setProperty("isActivable", False)
            current_button.setProperty("text", "")

            # Si le fichier existe mais n'a pas été ouvert, cela veut dire qu'il y a une erreur dans le fichier
            if os.path.isfile(page_path):
                logging.warning("le chargement de la page " + str(index)
                                + " relié au bouton rb" + str(index) + " est impossible"
                                + "\n\t\tLe fichier " + page_path + " existe mais ne se charge pas correctement"
                                + "\n\t\tAssurez-vous que celui-ci ne contient pas d'erreurs\n")
            # Sinon c'est qu'il n'existe pas où qu'il est mal placé
            else:
                logging.warning("le chargement de la page " + str(index)
                                + " relié au bouton rb" + str(index) + " est impossible"
                                + "\n\t\tLe fichier " + page_path + " n'existe pas"
                                + "\n\t\tAssurez-vous que le fichier source est au bon endroit ou créez le\n")
