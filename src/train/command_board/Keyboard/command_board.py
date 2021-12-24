# Librairies par défaut
import sys
import os


# Librairie de commande pupitre
# https://www.youtube.com/watch?v=823ProFM4us


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


# TODO : classe et code permettant de recevoir les informations du pupitre. Cett classe doit contenir 3 fonctions
# Une fonction initialise qui va chercher le port de l'arduino et va s'y connecter
# Une fonction run qui va lancer sur un nouveau thread la fonction update()
# une fonction update contenant une boucle qui tournera jusqu'à ce que la simulation s'arrête


def main():
    # Lance un fichier de registre
    log.initialise(log_level=log.Level.DEBUG, save=True)
    log.info("Lancement des essais du pupitre léger")

    # TODO : initialiser une instance de la base de donnée train et appeler son constructeur afin de tester le pupitre avec différents matériels roulants

    # TODO : appeler la fonction d'initialisation du pupitre

    # TODO : lancer le pupitre

