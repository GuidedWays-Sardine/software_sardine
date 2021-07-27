import logging
import log.log as log

import initialisation.initialisation_window as ini

def main():
    log.initialise('../log/', '1.0.1', logging.INFO)
    logging.info("Lancement de l'application d'initialisation du simulateur\n\n\n")

    # Lance le programme d'initialisation
    try:
        app = ini.InitialisationWindow()
    # Récupère une potentielle erreur fatale et la charge
    except Exception as error:
        logging.fatal('Erreur fatale lors du chargement de l\'application d\'initialisation simulateur\n\t\t' +
                      'Erreur de type : ' + str(type(error)) + '\n\t\t' +
                      'Avec comme message d\'erreur : ' + error.args[0] + '\n\n\t\t' +
                      ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '\n\t\t') + "\n")
        exit(-1)

if __name__ == "__main__":
    main()
