# Librairies par défaut
import sys
import os
import traceback


# Librairies graphiques
from PyQt5.QtWidgets import QApplication


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.initialisation.initialisation_window as ini
import src.simulation as sim


VERSION = "1.1.0"
INITIAL_LOGGING = log.Level.DEBUG


def main():
    # Lance le fichier de log en mode warning pour récupérer les warnings et erreurs critiques
    log.initialise(log_level=log.Level.DEBUG, save=True)
    log.info(f"Lancement de l'application d'initialisation du simulateur.\n\n\n")
    application = QApplication(sys.argv)

    parameters = None
    try:
        # lance le programme d'initialisation et vérifie qu'il n'y a pas d'erreurs au lancement
        initialisation = ini.InitialisationWindow(application)

        # Si le bouton lancer a été cliqué, récupère les informations, sinon sort
        if initialisation.launch_simulator:
            parameters = initialisation.get_values()
            del initialisation
        else:
            log.change_log_prefix()
            log.info(f"l'application d'initialisation a été fermée sans donner suite.\n")
            exit(0)
    except Exception as error:
        # Récupère une potentielle erreur fatale et la charge
        log.critical(f"""Erreur fatale lors du chargement de l'application d'initialisation simulateur
                     \t\tErreur de type : {type(error)}
                     \t\tAvec comme message d'erreur : {error.args}\n\n\t\t""" +
                     "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                     prefix="")
        exit(-1)

    # Change le niveau de log à celui précisé par l'utilisateur et enlève tout préfixe
    log.change_log_prefix()
    log.info(f"Lancement du simulateur.\n\n\n")
    try:
        log.change_log_level(parameters["log_level"])
    except KeyError:
        log.warning(f"""Aucun paramêtre \"log_level\" récupéré du programme d'initialisation
                    \t\tNiveau par défaut gardé ({INITIAL_LOGGING})\n""")

    # Lance le simulateur et en ressort que si une erreur fatale est détecté ou que le simulateur est fermé
    try:
        # Initialise la simulation
        simulation = sim.Simulation(application, parameters)
    except Exception as error:
        # Récupère une potentielle erreur lors de l'initialisation de la simulation
        log.critical(f"""Erreur fatale lors de l'initialisation du simulateur
                     \t\tErreur de type : {type(error)}
                     \t\tAvec comme message d'erreur : {error.args}\n\n\t\t""" +
                     "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                     prefix="")
        exit(-1)
    else:
        crash = False
        try:
            # Lance la simulation
            simulation.run()
        except Exception as error:
            log.critical(f"""Erreur fatale lors du fonctionnement du simulateur
                         \t\tErreur de type : {type(error)}
                         \t\tAvec comme message d'erreur : {error.args}\n\n\t\t""" +
                         "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                         prefix="")
            crash = True
        finally:
            simulation.stop()
            exit(0 if not crash else -1)


if __name__ == "__main__":
    main()
