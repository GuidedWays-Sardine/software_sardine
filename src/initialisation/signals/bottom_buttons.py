import logging
import traceback

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog


class BottomButtons:

    def __init__(self, application):
        """Permet d'initialiser les boutons permanents (quitter, ouvrir, sauvegarder, lancer) situés en bas de la fenêtre.
        Connecte chaque bouton à sa fonctionalité (nécessaires au bon fonctionnement de l'application d'initialisation)

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Boutons quitter/lancer (obligatoires pour le lancement de l'application)
        application.win.findChild(QObject, "quitter").clicked.connect(lambda: self.on_quit_clicked(application))
        application.win.findChild(QObject, "lancer").clicked.connect(lambda: self.on_launch_clicked(application))


    def on_quit_clicked(self, application):
        """Ferme la fenêtre d'initialisation

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        """
        application.app.quit()

    def on_launch_clicked(self, application):
        """Ferme la fenêtre d'initialisation et indique au programme de récupérer les données entrées

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets"""
        # Indique que le simulateur va être lancée et ferme l'application
        application.launch_simulator = True
        application.app.quit()
