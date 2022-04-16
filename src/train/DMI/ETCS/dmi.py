# Librairies par défaut
import os
import sys
import time


# librairies graphiques
from PyQt5.QtWidgets import QDesktopWidget, QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.simulation as sim


class DriverMachineInterface:
    """Classe contenant tous les éléments pour le DMI ETCS (ETCS et STM)"""

    # Eléments utiles à la fenêtre et les QWidgets contenus sur celle-ci
    engine = None
    dmi_window = None
    active_dmi = ""     # Par défaut le dmi ETCS sera activé. S'il doit être changé, il le sera après chargement

    pages = {}

    def __init__(self, simulation):
        """Fonction permettant d'initialiser tous les sous DMI du DMI ETCS

        Parameters
        ----------
        simulation: `sim.Simulation`
            Simulation contenant toutes les bases de données et modules de la simulation initialisée
        """
        # Indique le début du chargement de l'initialisation du dmi
        initial_time = time.perf_counter()
        log.info("Début du chargement du Driver Machine Interface.\n\n",
                 prefix="Initialisation DMI ETCS")

        # crée un engine pour le chargement de la fenêtre du DMI et essaye de charger le DMI
        self.engine = QQmlApplicationEngine()
        self.engine.load(f"{PROJECT_DIR}src\\train\\DMI\\ETCS\\dmi.qml")

        # Vérifie si le fichier qml de la fenêtre a bien été ouvert et compris, sinon jête une erreur
        if not self.engine.rootObjects() and not os.path.isfile(f"{PROJECT_DIR}src\\train\\DMI\\ETCS\\dmi.qml"):
            raise FileNotFoundError("Le fichier .qml pour la fenêtre du DMI ETCS n\'a pas été trouvé.")
        elif not self.engine.rootObjects() and os.path.isfile(f"{PROJECT_DIR}src\\train\\DMI\\ETCS\\dmi.qml"):
            raise SyntaxError("Le fichier .qml pour la fenêtre du DMI ETCS contient des erreurs.")

        # Si le fichier qml a été compris, récupère la fenêtre et la cache le temps de charger le reste du module
        self.dmi_window = self.engine.rootObjects()[0]
        self.dmi_window.hide()
        self.dmi_window.visibilityChanged.connect(lambda: QApplication.instance().quit())

        # Récupère la liste des dmis disponibles dans la norme ETCS (dossier ETCS + liste de ceux dans le dossier STM)
        dmi_list = [f"{PROJECT_DIR}src\\train\\DMI\\ETCS\\STM\\{dmi}" for dmi in os.listdir(f"{PROJECT_DIR}src\\train\\DMI\\ETCS\\STM")]
        dmi_list.insert(0, f"{PROJECT_DIR}src\\train\\DMI\\ETCS\\ETCS")
        self.active_dmi = dmi_list[0].split("DMI\\ETCS\\")[1].replace("\\", ".")

        # Pour chacun des sous-dmi à charger
        for dmi in dmi_list:
            # Ajoute un dictionnaire avec toutes les catégories vide avec comme clé le DMI (attention ETCS ou STM.X)
            dmi_key = dmi.split("DMI\\ETCS\\")[1].replace("\\", ".")
            self.pages[dmi_key] = {"A": {}, "B": {}, "C": {}, "D": {}, "E": {}, "F": {}, "G": {}}

            # Dans le cas où il existe des sections sans dossiers graphiques, les indique toutes dans le registre
            if {"A", "B", "C", "D", "E", "F", "G"}.difference(os.listdir(dmi + "\\graphics")):
                log.warning(f"Le DMI {dmi_key} n'a pas les sections : " +
                            " ; ".join(sorted({"A", "B", "C", "D", "E", "F", "G"}.difference(os.listdir(dmi + "\\graphics")))) + ".\n")

            # Pour chaque sections graphiques du DMI ayant un dossier associé (normalement A à G)
            for folder in (f for f in ["A", "B", "C", "D", "E", "F", "G"] if f in os.listdir(dmi + "\\graphics")):
                # Change le préfix des logs pour indiquer quelle section est en train d'être chargée
                log.change_log_prefix(f"Initialisation DMI ETCS ({dmi_key}) ; section {folder}")

                # Regarde pour chaque fichier graphique contenu dans le dossier de la section
                for file in (f.replace(".qml", "") for f in os.listdir(f"{PROJECT_DIR}src\\train\\DMI\\ETCS\\ETCS\\graphics\\{folder}") if f.endswith(".qml")):
                    page_initial_time = time.perf_counter()

                    # Essaye de charger la partie graphique de la page
                    if self.initialise_section(dmi_key, folder, file):
                        # Si celle-ci a correctement été chargée tente de charger la partie logique
                        self.initialise_signals(dmi_key, folder, file, page_initial_time)

                # Vérifie qu'au moins un fichier graphique a été correctement chargé, sinon l'indique
                if not self.pages[dmi_key][folder]:
                    log.warning("Aucun fichier correctement chargé dans la section. Celle-ci restera vide.\n")

        # Récupère les données reliées à la taille et la position de l'écran du DMI central
        dmi_screen_data = "SARDINE simulator.Central DMI."
        try:
            # Tente de récuper l'index et si celui-ci n'a pas été trouvé, jette une erreur et crash le programme
            screen_index = simulation.parameters[dmi_screen_data + "screen_index"]
        except KeyError:
            raise KeyError(f"Pas de valeurs : {dmi_screen_data}. L'écran DMI central n'a pas pu être chargé.\n")
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
        log.info(f"Application du DMI chargée en " +
                 f"{((time.perf_counter() - initial_time)*1000):.2f} millisecondes.\n\n")

    def initialise_section(self, dmi, section, file):
        """Fonction permettant d'initialiser un fichier graphique en fonction du dmi auquel il appartient, de la section
        où il est situé et du fichier dans lequel il se trouve

        Parameters
        ----------
        dmi: `string`
            clé permettant d'accéder aux différentes sections du dmi chargé (stocké dans self.pages[dmi])
        section: `string`
            clé et dossier permettant d'accéder aux différentes pages d'une section d'un dmi (stocké dans self.pages[dmi][section])
        file: `string`
            clé et fichier à charger l'engine généré sera stocké dans self.pages[dmi][section][file]

        Returns
        -------
        is_loaded : `bool`
            est-ce que la partie graphique de la page a été chargée ?
        """
        # Tente de charger le fichier graphique à partir du dmi, de la section et du fichier envoyé
        log.info(f"tentative de chargement du fichier : {file}.qml.\n")
        engine = QQmlApplicationEngine()
        engine.load(f"{PROJECT_DIR}src\\train\\DMI\\ETCS\\" + dmi.replace('.', '\\') + f"\\graphics\\{section}\\{file}.qml")

        # Si la page a été correctement chargée
        if engine.rootObjects():
            # Si l'élément chargé fait partie du dmi actif et que c'est le premier élément de la section chargé
            if dmi == self.active_dmi and not self.pages[dmi][section]:
                # Le rend visible sur le DMI_stackview associé à la section envoyé (attention objectName en minuscule)
                self.dmi_window.findChild(QObject, section.lower()).set_active_page(engine.rootObjects()[0])

            # Dans tous les cas, rajoute la page dans le dictionaire (pour la trouver dans le futur) et retourne vrai
            self.pages[dmi][section][file] = engine
            return True
        else:
            # Dans le cas où la page n'est pas valide laisse un warning et retourne False
            log.warning(f"Le fichier : {file}.qml contient des erreurs.\n\n")
            return False

    def initialise_signals(self, dmi, section, file, page_initial_time):
        """Fonction permettant d'initialiser un fichier logique associé à un fichier graphique correctement chargé
        en fonction du dmi auquel il appartient, de la sectionc où il est situé et du fichier dans lequel il se trouve

        Parameters
        ----------
        dmi: `string`
            clé permettant d'accéder aux différentes sections du dmi chargé (stocké dans self.pages[dmi])
        section: `string`
            clé et dossier permettant d'accéder aux différentes pages d'une section d'un dmi (stocké dans self.pages[dmi][section])
        file: `string`
            clé et fichier à charger la partie fonctionnelle généré sera stocké dans self.pages[dmi][section][file]
        page_initial_time: `float`
            temps de début de chargement de la page

        Returns
        -------
        is_fully_loaded: `bool`
            est-ce que la page a entièrement été chargée (graphique et logique)
        """
        # Vérifie si la page a des signals handlers associés (en recherchant un ficher .py associé)
        fully_loaded = False
        if os.path.isfile(f"{PROJECT_DIR}src\\train\\DMI\\ETCS\\" + dmi.replace(".", "\\") + f"\\signals\\{section}\\{file}.py"):
            # Si c'est le cas, initialise les signals handlers et le stock
            try:
                # Import localement le fichier de la page et appelle le constructeur de la page pour initialiser les signaux
                exec(f"import src.train.DMI.ETCS.{dmi}.signals.{section}.{file} as {file}\n"
                     f"self.pages[\"{dmi}\"][\"{section}\"][\"{file}\"] = {file}.{file}(self.pages[\"{dmi}\"][\"{section}\"][\"{file}\"], section, file)")
            except Exception as error:
                # Permet de rattraper une erreur si le code est incorrect
                log.warning(f"Erreur lors du chargement des signaux de la page : {file}.\n",
                            exception=error)
            else:
                # Si la page a sa partie logique de chargée, l'indique et vérifie l'existence de toutes les fonctions nécessaires
                fully_loaded = True
                self.are_page_functions_there(self.pages[dmi][section][file])
        else:
            # Sinon pas de signals handlers associé, le précise dans les logs
            log.warning(f"La page {file} n'a aucun fichier signals associé. La page sera visible mais ne sera pas fonctionnelle.\n")

        # Indique le temps de chargement partiel (graphique uniquement) ou complet (graphique et logique) de la page
        log.info(f"Page : {file} chargée partiellement (graphique " + ("et logique)" if fully_loaded else "uniquement)") +
                 f" en {((time.perf_counter() - page_initial_time) * 1000):.2f} millisecondes.\n\n")
        return fully_loaded

    def are_page_functions_there(self, page):
        """Permet, à partir d'une page de section de DMI correctement charger, d'indiquer si toutes les fonctions
        potentiellement nécessaires au fonctionnement de celle-ci sont présentes.

        Parameters
        ----------
        page: ``
            page à vérifier
        """
        # Dans l'ordre : update (ici change_language n'est pas vérifié car très peu de texte sur le DMI)
        if "update" not in dir(page):
            log.debug(f"Aucune fonction \"update\", pour la page {page.section}.{page.file}.\n",
                      prefix=f"Initialisation DMI ETCS ; section {page.section}")

    def run(self):
        """Fonction permettant de lancer le dmi, en montrant la fenêtre du dmi"""
        self.dmi_window.show()

    def update(self):   # TODO, voir si la fonction update prend le paquet de l'EVC ?
        """Fonction permettant de mettre à jour les différents éléments graphiques du DMI"""
        # TODO : Ajouter une section pour le changement du DMI si l'EVC indique que celui-ci a changé

        # Pour chacune des sections du dmi actif contenant des fichiers fichiers graphiques
        for folder in (f for f in ["A", "B", "C", "D", "E", "F", "G"] if self.pages[self.active_dmi][f]):
            log.change_log_prefix(f"Update DMI {self.active_dmi} ; section {folder}")
            # Pour chacunes des pages de chaque sections contenant une fonction update
            for file in (f for f in self.pages[self.active_dmi][folder] if "update" in dir(self.pages[self.active_dmi][folder][f])):
                # Essaye d'appeler la fonction update (et attrape les erreurs s'il y a une erreur
                try:
                    self.pages[self.active_dmi][folder][file].update()
                except Exception as error:
                    log.warning(f"Erreur lors de la mise à jour de la page {folder}.{file} du DMI.\n\t\t.\n",
                                exception=error)

def main():
    # Lance le fichier registre
    log.initialise(log_level=log.Level.DEBUG, save=True)

    # Crée une micro simulation (avec juste le DMI, les bases de données et des paramètres)
    from PyQt5.QtWidgets import QApplication
    class Simulation:
        app = QApplication(sys.argv)
        dmi = None
        parameters = {"immersion": False,
                      "SARDINE simulator.Central DMI.screen_index": 1,
                      "SARDINE simulator.Central DMI.full_screen": False,
                      "SARDINE simulator.Central DMI.x": 240,
                      "SARDINE simulator.Central DMI.y": 0,
                      "SARDINE simulator.Central DMI.w": 1440,
                      "SARDINE simulator.Central DMI.h": 1080}

    # Initialise une instance de la simulation ainsi que du dmi
    simulation = Simulation()
    simulation.dmi = DriverMachineInterface(simulation)

    # Lance le DMI
    simulation.dmi.run()
    QApplication.instance().exec()


if __name__ == "__main__":
    main()
