# Librairies par défaut
import sys
import os
import traceback


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.initialisation.initialisation_window as ini
import src.simulation as simulation


VERSION = "1.1.0"
INITIAL_LOGGING = log.Level.DEBUG


def main():

    # Lance le fichier de log en mode warning pour récupérer les warnings et erreurs critiques
    log.initialise(PROJECT_DIR + "log\\", VERSION, INITIAL_LOGGING)
    log.info("Lancement de l'application d'initialisation du simulateur\n\n\n")

    # lance le programme d'initialisation et vérifie qu'il n'y a pas d'erreurs au lancement
    parameters = None
    try:
        app = ini.InitialisationWindow()

        # Si le bouton lancer a été cliqué, récupère les informations, sinon sort
        if app.launch_simulator:
            parameters = app.get_values()
            del app
        else:
            log.change_log_prefix()
            log.info("l\'application d'initialisation a été fermée sans donner suite.\n")
            exit(0)
    # Récupère une potentielle erreur fatale et la charge
    except Exception as error:
        log.critical("Erreur fatale lors du chargement de l'application d'initialisation simulateur\n\t\t" +
                     "Erreur de type : " + str(type(error)) + "\n\t\t" +
                     "Avec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                     "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
        exit(-1)

    # Change le niveau de log à celui précisé par l'utilisateur et enlève tout préfixe
    log.change_log_prefix()
    log.info("Lancement du simulateur\n\n\n")
    try:
        log.change_log_level(parameters["Registre"])
    except KeyError:
        log.warning("Aucun paramêtre \"log_level\" récupéré du programme d'initialisation" +
                    "\n\t\tNiveau par défaut gardé à suffisant (log.WARNING)\n")

    # Lance le simulateur et en ressort que si une erreur fatale est détecté ou que le simulateur est fermé
    try:
        application = simulation.Simulation(parameters)
    except Exception as error:
        log.critical("Erreur fatale lors du fonctionnement du simulateur\n\t\t" +
                     "Erreur de type : " + str(type(error)) + "\n\t\t" +
                     "Avec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                     "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
        exit(-1)


if __name__ == "__main__":
    main()
