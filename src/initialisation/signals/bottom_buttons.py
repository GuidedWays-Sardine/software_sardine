import logging
import traceback

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog

from file_io import data_file_interaction as dfi


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
            application.win.findChild(QObject, "ouvrir").clicked.connect(lambda: self.on_open_clicked(application))
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
        # Vérifie que toutes les pages accessibles sont complètes
        if application.is_fully_loaded == application.is_completed:
            # Indique que le simulateur va être lancée et ferme l'application
            application.launch_simulator = True
            application.app.quit()

    def on_open_clicked(self, application):
        """Fonction appelée lorsque le bouton ouvrir est cliqué.
        Permet l'ouverture d'un fichier texte et la récupération de ses paramètres.

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets"""
        # Ouvre la fenêtre d'ouverture de fichier
        file_path = QFileDialog.getOpenFileName(caption="Ouvrir un fichier de configuration",
                                                directory="../settings/general_settings",
                                                filter="Fichiers de configuration Sardine (*.settings)")
        if file_path[0] != '':
            # Récupère les donnés du fichier text et mets à jour les différentes pages de paramètres
            try:
                data = dfi.read_data_file(file_path[0])
            except FileNotFoundError:
                logging.error("Le fichier ouvert n'existe plus. Aucun paramètre ne sera modifié\n")
            except OSError:
                logging.error("Le fichier n\'a pas pu être ouvert. Assurez vous qu'il ne soit pas déjà ouvert.\n")
            else:
                application.set_values(data)

    def on_save_clicked(self, application):
        """Fonction appelée lorsque le bouton sauvegarder est cliqué.
        Permet la sauvegarde d'un fichier avec les settings.

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets"""
        # Ouvre la fenêtre de sauvegarde et enregegistre le fichier si un nom a été donné
        file_path = QFileDialog.getSaveFileName(caption="Sauvegarder un fichier de configuration",
                                                directory="../settings/general_settings",
                                                filter="Fichiers de configuration Sardine (*.settings)")
        if file_path[0] != '':
            # Récupère les donnés des différentes pages de paramètres et les écrits dans le fichier
            try :
                dfi.write_data_file(file_path, application.get_values())
            except OSError:
                logging.error("Vous n'avez pas les droit d'enregistrer un fichier dans cet emplacement")
