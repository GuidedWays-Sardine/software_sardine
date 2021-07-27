import logging
import log.log as log

import initialisation.initialisation_window as ini

def main():
    log.initialise('../log/', '1.0.1', logging.INFO)
    logging.info("Lancement de l'application d'initialisation du simulateur\n\n\n")

    # Lance le programme d'initialisation
    app = ini.InitialisationWindow()


if __name__ == "__main__":
    main()
