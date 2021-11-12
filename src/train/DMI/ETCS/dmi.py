# Librairies par défaut
import os
import sys
import traceback
import time


# librairies graphiques
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.simulation as sim


class DriverMachineInterface:
    """Classe contenant tous les éléments pour le DMI"""

    # Eléments utiles à la fenêtre et les QWidgets contenus sur celle-ci
    engine = None
    dmi_window = None
    active_dmi = ""     # Par défaut le dmi ETCS sera activé. S'il doit être changé, il le sera après chargement

    pages = {}

    def __init__(self, simulation):
        initial_time = time.time()
        log.info("Début du chargement du Driver Machine Interface.\n\n",
                 prefix="Initialisation DMI ETCS")

        # crée un self.engine pour le chargement de la fenêtre du DMI et essaye de charger le DMI
        self.engine = QQmlApplicationEngine()
        self.engine.load(PROJECT_DIR + "src\\train\\DMI\\ETCS\\dmi.qml")

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile(PROJECT_DIR + "src\\train\\DMI\\ETCS\\dmi.qml"):
            raise FileNotFoundError("Le fichier .qml pour la fenêtre du DMI ETCS n\'a pas été trouvé.")
        elif not self.engine.rootObjects() and os.path.isfile(PROJECT_DIR + "src\\train\\DMI\\ETCS\\dmi.qml"):
            raise SyntaxError("Le fichier .qml pour la fenêtre du DMI ETCS contient des erreurs.")

        # Si le fichier qml a été compris, récupère la fenêtre et la cache le temps que tous les modules finissent de charger
        self.dmi_window = self.engine.rootObjects()[0]
        self.dmi_window.hide()
        self.dmi_window.visibilityChanged.connect(lambda: simulation.app.quit())

        # Récupère la liste des dmis disponibles dans la norme ETCS
        dmi_list = [(PROJECT_DIR + "src\\train\\DMI\\ETCS\\STM\\" + dmi) for dmi in os.listdir(PROJECT_DIR + "src\\train\\DMI\\ETCS\\STM")]
        dmi_list.insert(0, PROJECT_DIR + "src\\train\\DMI\\ETCS\\ETCS")
        self.active_dmi = dmi_list[0].split("DMI\\ETCS\\")[1].replace("\\", ".")

        # Pour chacun des sous-dmi à charger
        for dmi in dmi_list:
            # Ajoute un dictionnaire vide pour le dmi
            dmi_key = dmi.split("DMI\\ETCS\\")[1].replace("\\", ".")
            self.pages[dmi_key] = {"A": {}, "B": {}, "C": {}, "D": {}, "E": {}, "F": {}, "G": {}}

            # Commence par indiquer toutes les sections qui n'ont pas de dossiers graphiques
            log.warning("Le DMI " + dmi_key + " n'a pas les sections : " +
                        " ; ".join(sorted(list({"A", "B", "C", "D", "E", "F", "G"}.difference(os.listdir(dmi + "\\graphics"))))) + ".\n")

        # Pour chaque sections graphiques du DMI ayant un dossier associé (A à G dans DMI/ETCS/graphics)
            for folder in (f for f in ["A", "B", "C", "D", "E", "F", "G"] if f in os.listdir(dmi + "\\graphics")):
                # Change le préfix des logs pour indiquer où la simulation en est
                log.change_log_prefix("Initialisation DMI ETCS (" + dmi_key + ") ; section " + folder)

                # Regarde tous les fichiers graphiques contenus dans ce fichier graphique
                for file in (f.replace(".qml", "") for f in os.listdir(PROJECT_DIR + "src\\train\\DMI\\ETCS\\ETCS\\graphics\\" + folder) if f.endswith(".qml")):
                    page_time = time.time()

                    # Essaye de charger la partie graphique de la page
                    if self.initialise_section(dmi_key, folder, file):
                        # Si celle-ci a correctement été chargée tente de charger la partie logique
                        self.initialise_signals(simulation, dmi_key, folder, file, page_time)

                # Vérifie qu'au moins un fichier graphique a été correctement chargé
                if not self.pages[dmi_key][folder]:
                    log.warning("Aucun fichier correctement chargé dans la section. Celle-ci restera vide.\n")

        # Récupère les données reliées à la taille et la position de l'écran du DMI central
        dmi_screen_data = "SARDINE simulator.Central DMI."
        try:
            # Tente de récuper l'index et si celui-ci n'a pas été trouvé, jette une erreur et crash le programme
            screen_index = simulation.parameters[dmi_screen_data + "screen_index"]
        except KeyError:
            raise KeyError("Pas de valeurs : " + dmi_screen_data + "\n\t\tL'écran DMI central n'a pas pu être chargé.\n")
        else:
            # Si l'index de l'écran n'est pas bon, jette une erreur, sinon récupère ses dimensions
            if screen_index == 0 or screen_index > QDesktopWidget().screenCount():
                raise ValueError("Aucun écran sélectionné pour le DMI central, la simulation ne peut pas se lancer.\n")
            else:
                # Récupères les informations de l'écran récupéré et vérifie si l'application est en plein écran ou non
                sg = QDesktopWidget().screenGeometry(screen_index - 1).getCoords()
                if simulation.parameters[dmi_screen_data + "full_screen"]:
                    # Si c'est en plein écran, récupère les valeurs de l'écran
                    self.dmi_window.setPosition(sg[0], sg[1])
                    self.dmi_window.resize(sg[2] - sg[0] + 1, sg[3] - sg[1] + 1)
                else:
                    # Si ce n'est pas en plein écran, récupère les valeurs de l'application d'initialisation
                    # Ces valeurs seront décallés selon la position
                    self.dmi_window.setPosition(sg[0] + simulation.parameters[dmi_screen_data + "x"], sg[1] + simulation.parameters[dmi_screen_data + "y"])
                    self.dmi_window.resize(simulation.parameters[dmi_screen_data + "w"], simulation.parameters[dmi_screen_data + "h"])

        # Indique le temps de chargement de l'application
        log.change_log_prefix("Initialisation DMI ETCS")
        log.info("Application du DMI chargée en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n")

    def initialise_section(self, dmi, section, file):
        log.info("tentative de chargement du fichier : " + file + ".qml.\n")
        engine = QQmlApplicationEngine()
        engine.load(PROJECT_DIR + "src\\train\\DMI\\ETCS\\" + dmi.replace(".", "\\") + "\\graphics\\" + section + "\\" + file + ".qml")

        # Si la page a été correctement chargée
        if engine.rootObjects():
            # Si c'est le premier élément de la section correctement chargé, le rend visible
            if not self.pages[dmi][section]:
                # Récupère le DMI_stackview (attention objectName en minuscule) et change la page active
                self.dmi_window.findChild(QObject, section.lower()).set_active_page(engine.rootObjects()[0])

            # Dans tous les cas, rajoute la page dans le dictionaire (pour la trouver dans le futur) et retourne vrai
            self.pages[dmi][section][file] = engine
            return True
        else:
            # Dans le cas où la page n'est pas valide laisse un warning et retourne False
            log.warning("Le fichier : " + file + ".qml contient des erreurs.\n\n")
            return False

    def initialise_signals(self, simulation, dmi, section, file, initial_time):
        # Vérifie si la page a des signals handlers associés (en recherchant un ficher .py associé)
        fully_loaded = False
        if os.path.isfile(PROJECT_DIR + "src\\train\\DMI\\ETCS\\" + dmi.replace(".", "\\") + "\\signals\\" + section + "\\" + file + ".py"):
            # Si c'est le cas, initialise les signals handlers et le stock
            try:
                # Import localement le fichier de la page et appelle le constructeur de la page pour initialiser les signaux
                exec("import src.train.DMI.ETCS." + dmi + ".signals." + section + "." + file + " as " + file + "\n" +
                     "self.pages[\"" + dmi + "\"][\"" + section + "\"][\"" + file + "\"] = " +
                     file + "." + file + "(simulation, self.pages[\"" + dmi + "\"][\"" + section + "\"][\"" + file + "\"], section, file)")
            except Exception as error:
                # Permet de rattraper une erreur si le code est incorrect
                log.warning("Erreur lors du chargement des signaux de la page : " + file + ".\n\t\t" +
                            "Erreur de type : " + str(type(error)) + "\n\t\t" +
                            "Avec comme message d\'erreur : " + str(error.args) +
                            "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")
            else:
                # Si la page a sa partie logique de chargée, l'indique et vérifie l'existence de toutes les fonctions nécessaires
                fully_loaded = True
                self.are_page_functions_there(self.pages[dmi][section][file])
        else:
            # Sinon pas de signals handlers associé, le précise dans les logs
            log.warning("La page " + file + " n\'a aucun fichier signals associé." +
                        "La page sera visible mais ne sera pas fonctionnelle.\n")

        # Indique le temps de chargement partiel (graphique uniquement) ou complet (graphique et logique) de la page
        log.info("Page : " + file + " chargée partiellement (graphique " + ("et logique)" if fully_loaded else "uniquement)") +
                 " en " + str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n")

    def are_page_functions_there(self, page):
        """Permet, à partir d'une page de section de DMI correctement charger, d'indiquer si toutes les fonctions
        potentiellement nécessaires au fonctionnement de celle-ci sont présentes.

        Parameters
        ----------
        page: ``
            page à vérifier
        """
        # Dans l'ordre : update
        if "update" not in dir(page):
            log.debug("Aucune fonction \"update\", pour la page " + page.section + "." + page.file + ".\n",
                      prefix="Initialisation DMI ETCS ; section " + page.section)

    def run(self):
        # Montre la fenêtre générale du DMI
        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.dmi_window.show()

    def update(self):   # TODO, voir si la fonction update prend le paquet de l'EVC ?
        # TODO : Ajouter une section pour le changement du DMI si l'EVC indique que celui-ci a changé
        # Pour chacune des sections contenant des fichiers
        for folder in (f for f in ["A", "B", "C", "D", "E", "F", "G"] if self.pages[self.active_dmi][f]):
            log.change_log_prefix("Update DMI " + self.active_dmi + " ; section " + folder)
            # Pour chacunes des pages de chaque sections
            for file in self.pages[self.active_dmi][folder]:
                # Si la page a correctement été chargée et que la page a une fonction update
                if "update" in dir(self.pages[self.active_dmi][folder][file]):
                    # Essaye d'appeler la fonction update (et attrape les erreurs s'il y a une erreur
                    try:
                        self.pages[self.active_dmi][folder][file].update()
                    except Exception as error:
                        log.warning("Erreur lors de la mise à jour de la page" + folder + "." + file + " du DMI.\n\t\t" +
                                    "Erreur de type : " + str(type(error)) + "\n\t\t" +
                                    "Avec comme message d\'erreur : " + str(error.args) +
                                    "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n")

def main():
    log.initialise("../../../../log/", "1.1.0", log.Level.DEBUG)

    # Crée une micro simulation (avec juste le DMI)
    from PyQt5.QtWidgets import QApplication

    class A:
        app = None
        dmi = None
        parameters = None

    simulation = A()
    simulation.app = QApplication(sys.argv)
    simulation.app.setQuitOnLastWindowClosed(True)

    simulation.parameters = {"immersion": False,
                             "SARDINE simulator.Central DMI.screen_index": 1,
                             "SARDINE simulator.Central DMI.full_screen": False,
                             "SARDINE simulator.Central DMI.x": 240,
                             "SARDINE simulator.Central DMI.y": 0,
                             "SARDINE simulator.Central DMI.w": 1440,
                             "SARDINE simulator.Central DMI.h": 1080}

    # Initialise, lance et montre le dmi
    simulation.dmi = DriverMachineInterface(simulation)
    simulation.dmi.run()
    simulation.app.exec()


if __name__ == "__main__":
    main()
