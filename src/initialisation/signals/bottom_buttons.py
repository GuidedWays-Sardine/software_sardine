import logging
import traceback
import time

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog


class BottomButtons:
    """Classe s'occupant du chargement et du fonctionnement des boutons inférieurs de l'application d'initialisation"""

    def __init__(self, application):
        """Permet d'initialiser les boutons permanents (quitter, ouvrir, sauvegarder, lancer) en bas de la fenêtre.
        Connecte chaque bouton à sa fonctionalité (nécessaires au bon fonctionnement de l'application d'initialisation)

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, (pour intérargir avec l'application)
        """
        initial_time = time.time()
        logging.info("Tentative de chargement des boutons inférieurs.\n")

        # Boutons quitter/lancer (obligatoires pour le lancement de l'application)
        application.win.findChild(QObject, "quit").clicked.connect(lambda: self.on_quit_clicked(application))
        application.win.findChild(QObject, "launch").clicked.connect(lambda: self.on_launch_clicked(application))

        # Boutons sauvegarder/ouvrir (non obligatoire pour le lancement de l'application)
        try:
            application.win.findChild(QObject, "open").clicked.connect(lambda: self.on_open_clicked(application))
            application.win.findChild(QObject, "save").clicked.connect(lambda: self.on_save_clicked(application))
        except Exception as error:
            logging.warning('Problème lors du chargement du signal du bouton sauvegarder ou ouvrir.\n\t' +
                            'Erreur de type : ' + str(type(error)) + '\n\t\t' +
                            'Avec comme message d\'erreur : ' + error.args[0] + '\n\n\t\t' +
                            ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '\n\t\t') + '\n')

        logging.info("Boutons inférieurs chargés en " +
                     str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

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
                data = {}

                # Essaye d'ouvrir le fichier envoyer, et jette une erreur si le fichier n'exsite pas
                file = open(file_path[0], "r", encoding='utf-8-sig')

                # Lit chaque ligne du fichier
                for line in file:
                    # Si la ligne ne contient pas le délimiteur (ici ;) l'indique dans les logs
                    if ";" not in line:
                        logging.debug("Ligne sautée. Délimiteur : \";\" manquant dans la ligne : " + line + '\n')
                    else:
                        line = line.rstrip('\n').split(";")
                        data[line[0]] = line[1]

                # Ferme le fichier et retourne le dictionnaire avec les valeurs récupérées
                file.close()
            except FileNotFoundError:
                logging.error("Le fichier ouvert n'existe plus. Aucun paramètre ne sera modifié.\n")
            except OSError:
                logging.error("Le fichier n\'a pas pu être ouvert. Assurez vous qu'il ne soit pas déjà ouvert.\n")
            else:
                # Si le dictionnaire de donnés n'a aucune valeur, un message d'erreur est levé sur le fichier
                if len(data) != 0:
                    application.set_values(data)
                else:
                    logging.warning(file_path[0] + " n'a aucune donné ou n'est pas dans un format compatible.\n")

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
            # Récupère les donnés des différentes pages de paramètres et les écrit dans le fichier
            data = application.get_values()
            try:
                # Essaye d'ouvrir le fichier envoyer, et jette une erreur si le fichier n'exsite pas
                file = open(file_path[0], "w", encoding='utf-8-sig')

                # Récupère chaque clé/valeur du dictionnaire
                for key in data.keys():
                    # Ecrit une ligne contenant la clé et la valeur séparé par le délimiteur (ici ;)
                    file.write(str(key) + ";" + str(data[key]) + "\n")

                # Ferme le fichier
                file.close()

            # Exception soulevée dans le cas où le fichier ne peut pas être créé ou modifié
            except OSError:
                logging.error("Vous n'avez pas les droit d'enregistrer un fichier dans cet emplacement.\n")
            else:
                # Dans le cas où aucune donnée n'a été récupérée, le signale dans les logs
                if len(data) == 0:
                    logging.warning("Aucune valeur récupérée, le fichier créé sera vide.\n")

    def change_language(self, application, translation_data):
        """Permet à partir d'un dictionnaire de traduction de traduire le textes des 4 boutons inférieurs.

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        translation_data: `dict`
            dictionaire contenant en clé les mots de la langue actuelle et en valeurs, leurs traductions
        """
        # Liste les id de chaque boutons pour simplifier la structure
        buttons_id = ["quit", "launch", "open", "save"]

        # Pour chaque boutons : récupère le texte, prend sa traduction dans translation_data et change son texte
        for id in buttons_id:
            # Récupère le bouton et vérifie s'il a bien été récupéré
            widget = application.win.findChild(QObject, id)
            if widget is not None:

                # S'il existe, essaye de traduire le texte sur le bouton
                try:
                    widget.setProperty("text", translation_data[widget.property("text").upper()])
                # Si la clé n'existe pas c'est que le mot n'existe pas dans le dictionnaire ou qu'il est mal traduit.
                except KeyError:
                    logging.debug("aucune traduction de : " + widget.property("text") + " n'existe pas.\n")
            else:
                logging.debug("Bouton d'objectName : " + id + " dans Bottom_Buttons introuvable.\n")
