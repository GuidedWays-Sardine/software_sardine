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
        logging.info('right buttons')