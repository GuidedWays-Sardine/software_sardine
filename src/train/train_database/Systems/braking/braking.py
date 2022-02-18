# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary.settings as sd


class Braking:
    # Informations sur certains types de freinages
    regenerative_activated = False
    dynamic_activated = False

    # Informations sur les systèmes de freinages
    pad_brakes = None
    disk_brakes = None
    magnetic_brakes = None
    foucault_brakes = None

    def __init__(self, train_data):
        """Fonction permettant d'initialiser les systèmes de freinages

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Dictionaire de paramètres train
        """
        # Récupère les valeurs pour le freinage rhéostatique et par régénération
        self.regenerative_activated = train_data.get_value("regenerative", False)
        self.dynamic_activated = train_data.get_value("dynamic", False)

        # Initialise des listes vides pour chacuns des systèmes de freinage
        self.pad_brakes = []
        self.disk_brakes = []
        self.magnetic_brakes = []
        self.foucault_brakes = []

    def generate(self, train_data):
        pass

    def read_train(self, train_data):
        pass
