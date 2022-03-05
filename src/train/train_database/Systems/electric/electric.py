# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))


class Electric:
    """Classe contenant tous les éléments du système électrique"""
    # TODO : ajouter les différents éléments nécessaires

    def __init__(self):
        """Fonction permettant d'initialiser les listes des sous-systèmes électriques vide"""
        pass  # TODO : ajouter l'initialisation et les autres fonctions nécessaires aux systèmes électriques
