import logging
import os
import traceback

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


class RightButtons:

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