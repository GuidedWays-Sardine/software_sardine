import logging
import traceback

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog


class BottomButtons:

    def __init__(self, application):
        """Permet d'initialiser les boutons permanents (quitter, ouvrir, sauvegarder, lancer) en bas de la fenêtre.
        Connecte chaque bouton à sa fonctionalité (nécessaires au bon fonctionnement de l'application d'initialisation)

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        # Boutons quitter/lancer (obligatoires pour le lancement de l'application)
        application.win.findChild(QObject, "quitter").clicked.connect(lambda: self.on_quit_clicked(application))
        application.win.findChild(QObject, "lancer").clicked.connect(lambda: self.on_launch_clicked(application))

        # Boutons sauvegarder/ouvrir (non obligatoire pour le lancement de l'application)
        try:
            application.win.findChild(QObject, "sauvegarder").clicked.connect(lambda: self.on_save_clicked(application))
        except AttributeError as error:
            logging.warning('Problème lors du chargement du signal handler du bouton sauvegarder ou ouvrir\n\t' +
                            'Erreur de type : ' + str(type(error)) + '\n\t' +
                            'Avec comme message d\'erreur : ' + error.args[0] + '\n\n\t' +
                            ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '\n\t'))

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

    def on_save_clicked(self, application):
        """Fonction appelée lorsque le bouton sauvegarder est cliqué.
        Permet la sauvegarde d'un fichier avec les settings.

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets"""
        # Ouvre la fenêtre de sauvegarde et enregegistre le fichier si un nom a été donné
        file_name = QFileDialog.getSaveFileName(caption="Sauvegarder un fichier de configuration",
                                                directory="../settings/",
                                                filter="Fichiers de configuration Sardine (*.csv)")
        if file_name[0] != '':
            application.save_configuration_file(file_name)
