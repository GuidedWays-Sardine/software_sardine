# Librairies par défaut
import sys
import os


# Librairies graphiques
import time

from PyQt5.QtWidgets import QApplication


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.initialisation as ini
import src.simulation as sim


INITIAL_LOG_LEVEL = log.Level.DEBUG
SAVE = True


def main():
    # Lance le registre selon les constantes définit en amont
    application = QApplication(sys.argv)        # Une seule QApplication peut être créée durant toute la simulation
    log.initialise(log_level=INITIAL_LOG_LEVEL, save=SAVE)
    log.info(f"Lancement de l'application d'initialisation du simulateur.\n\n\n")

    # Application d'initialisation : Permet de rentrer tous les paramètres de simulation de façon simple
    settings = {}
    try:
        # Initialise et lance l'application d'initialisation.
        initialisation = ini.InitialisationWindow()

        # Si le bouton lancer a été cliqué, récupère les informations, sinon sort
        if initialisation.launch_simulator:
            settings = initialisation.get_settings()
            del initialisation
        else:
            log.add_empty_lines()
            log.info(f"l'application d'initialisation a été fermée sans donner suite.",
                     prefix="Application d'initialisation")
            exit(0)
    except Exception as error:
        # Récupère une potentielle erreur ratée, la laisse dans le registre et arrête l'application
        log.critical(f"Erreur fatale lors du chargement de l'application d'initialisation simulateur.",
                     exception=error, prefix="Application d'initialisation")
        exit(-1)

    # Change le niveau de log à celui précisé par l'utilisateur et enlève tout préfixe
    log.change_log_prefix()
    log.add_empty_lines()
    log.info(f"Lancement du simulateur.\n\n\n")
    log.change_log_level(settings.get_value("log_level", INITIAL_LOG_LEVEL))

    # Application de simulation : gère les différents modules de simulation
    try:
        # Initialise la simulation
        simulation = sim.Simulation(settings)
    except Exception as error:
        # Récupère une potentielle erreur lors de l'initialisation, la laisse dans le registre et arrête l'application
        log.critical(f"Erreur fatale lors de l'initialisation du simulateur.\n",
                     exception=error, prefix="Initialisation Simulation")
        exit(-1)
    else:
        crash = False
        try:
            # Lance la simulation (reste dans la fonction jusqu'à un crash où l'arrêt demandé de la simulation)
            simulation.run()
        except Exception as error:
            log.critical(f"Erreur fatale lors du fonctionnement du simulateur.",
                         exception=error, prefix="Simulation")
            crash = True
        finally:
            try:
                # Arrête la simulation de façon sécurisé
                simulation.stop()
            except Exception as error:
                log.critical(f"Erreur fatale lors de la fermeture du simulateur.",
                             exception=error, prefix="Fermeture simulation")
                crash = True
            exit(0 if not crash else -1)


if __name__ == "__main__":
    main()
