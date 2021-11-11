# Librairies par défaut
import os
import sys
import traceback
import time
import threading


# librairies graphiques
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QObject
from PyQt5.QtQml import QQmlApplicationEngine


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


class DriverMachineInterface:
    """Classe contenant tous les éléments pour le DMI"""

    # Eléments utiles à la fenêtre et les QWidgets contenus sur celle-ci
    engine = None
    dmi_window = None

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

        # S'occupe maintenant de l'initialisation du DMI ETCS
        # Recherche la liste des fichiers et dossiers présents dans le dossier DMI/ETCS/graphics
        folders = os.listdir(PROJECT_DIR + "src\\train\\DMI\\ETCS\\ETCS\\graphics")

        # Pour chaque sections graphiques du DMI ayant un dossier associé (A à G dans DMI/ETCS/graphics)
        for folder in ["A", "B", "C", "D", "E", "F", "G"]:
            # Initialise la liste des éléments graphiques disponibles

            self.pages[folder] = {}

            # Si le dossier existe bien, regarde chaque fichiers présents à l'intérieur de celui-ci
            if folder in folders:
                files = os.listdir(PROJECT_DIR + "src\\train\\DMI\\ETCS\\ETCS\\graphics\\" + folder)
                # Récupère tous les fichiers en .qml et enlève l'extension (rerajoutée si nécessaire)
                for file in (f.replace(".qml", "") for f in files if f.endswith(".qml")):
                    page_time = time.time()

                    # Essaye de charger la partie graphique de la page
                    if self.initialise_section(folder, file):
                        # Si celle-ci a correctement été chargée tente de charger la partie logique
                        self.initialise_signals(folder, file, initial_time)
                    #FIXME : faire l'initialisation des STM aussi, comme ça tout sera bon

                # Vérifie qu'au moins un fichier graphique a été correctement chargé
                if len(self.pages[folder]) == 0:
                    log.error("Aucun fichier graphique correctement chargé dans" + folder + ". La section restera vide.\n",
                              prefix="Initialisation DMI ETCS ; section " + folder)

            # Dans le cas où le fichier n'existe pas
            else:
                log.error("Aucun dossier graphique : " + folder + ". La section restera vide.\n",
                          prefix="Initialisation DMI ETCS ; section " + folder)

        # Récupère les données reliées à la taille et la position de l'écran du DMI central
        central_dmi_key = "SARDINE simulator.Central DMI."
        try:
            # Tente de récuper l'index et si celui-ci n'a pas été trouvé, jette une erreur et crash le programme
            screen_index = simulation.parameters[central_dmi_key + "screen_index"]
        except KeyError:
            raise KeyError("Pas de valeurs : " + central_dmi_key + "\n\t\tL'écran DMI central n'a pas pu être chargé.\n")
        else:
            # Si l'index de l'écran n'est pas bon, jette une erreur, sinon récupère ses dimensions
            if screen_index == 0 or screen_index > QDesktopWidget().screenCount():
                raise ValueError("Aucun écran sélectionné pour le DMI central, la simulation ne peut pas se lancer.\n")
            else:
                # Récupères les informations de l'écran récupéré et vérifie si l'application est en plein écran ou non
                sg = QDesktopWidget().screenGeometry(screen_index - 1).getCoords()
                if simulation.parameters[central_dmi_key + "full_screen"]:
                    # Si c'est en plein écran, récupère les valeurs de l'écran
                    self.dmi_window.setPosition(sg[0], sg[1])
                    self.dmi_window.resize(sg[2] - sg[0] + 1, sg[3] - sg[1] + 1)
                else:
                    # Si ce n'est pas en plein écran, récupère les valeurs de l'application d'initialisation
                    # Ces valeurs seront décallés selon la position
                    self.dmi_window.setPosition(sg[0] + simulation.parameters[central_dmi_key + "x"], sg[1] + simulation.parameters[central_dmi_key + "y"])
                    self.dmi_window.resize(simulation.parameters[central_dmi_key + "w"], simulation.parameters[central_dmi_key + "h"])

        # Indique le temps de chargement de l'application
        log.info("Application du DMI chargée en " +
                 str("{:.2f}".format((time.time() - initial_time)*1000)) + " millisecondes.\n\n",
                 prefix="Initialisation DMI ETCS")

    def initialise_section(self, section, file):
        log.info("tentative de chargement du fichier : " + file + ".qml.\n",
                 prefix="Initialisation DMI ETCS ; section " + section)
        engine = QQmlApplicationEngine()
        engine.load(PROJECT_DIR + "src\\train\\DMI\\ETCS\\ETCS\\graphics\\" + section + "\\" + file + ".qml")

        # Si la page a été correctement chargée
        if engine.rootObjects():
            # Si c'est le premier élément de la section correctement chargé, le rend visible
            if len(self.pages[section]) == 0:
                # Récupère le DMI_stackview (attention objectName en minuscule) et change la page active
                self.dmi_window.findChild(QObject, section.lower()).set_active_page(engine.rootObjects()[0])

            # Dans tous les cas, rajoute la page dans le dictionaire (pour la trouver dans le futur) et retourne vrai
            self.pages[section][file] = engine
            return True
        else:
            # Dans le cas où la page n'est pas valide laisse un warning et retourne False
            log.warning("Le fichier : " + file + ".qml, du dossier : " + section + ", contient des erreurs.\n\n",
                        prefix="Initialisation DMI ETCS ; section " + section)
            return False

    def initialise_signals(self, section, file, initial_time):
        # Vérifie si la page a des signals handlers associés (en recherchant un ficher .py associé)
        fully_loaded = False
        if os.path.isfile(PROJECT_DIR + "src\\train\\DMI\\ETCS\\ETCS\\signals\\" + section + "\\" + file + ".qml"):
            # Si c'est le cas, initialise les signals handlers et le stock
            try:
                # Import localement le fichier de la page et appelle le constructeur de la page pour initialiser les signaux
                exec("from src.train.DMI.ETCS.ETCS.signals." + section + " import " + file + " as " + file + "\n" +
                     "self.pages[\"" + section + "\"][\"" + file + "\"] = " +
                     file + "." + file + "(simulation, engine, folder, file)")
            except Exception as error:
                # Permet de rattraper une erreur si le code est incorrect
                log.warning("Erreur lors du chargement des signaux de la page : " + file + ".\n\t\t" +
                            "Erreur de type : " + str(type(error)) + "\n\t\t" +
                            "Avec comme message d\'erreur : " + str(error.args) +
                            "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                            prefix="Initialisation DMI ETCS ; section " + section)
            else:
                # Si la page a sa partie logique de chargée, l'indique et vérifie l'existence de toutes les fonctions nécessaires
                fully_loaded = True
                # TODO : fonction pour vérifier si la fonction update de la page existe
        else:
            # Sinon pas de signals handlers associé, le précise dans les logs
            log.warning("La page " + file + " n\'a aucun fichier signals associé." +
                        "La page sera visible mais ne sera pas fonctionnelle.\n",
                        prefix="Initialisation DMI ETCS ; section " + section)

        # Indique le temps de chargement partiel (graphique uniquement) ou complet (graphique et logique) de la page
        log.info("Page : " + file + " chargée partiellement (graphique " + "et logique)" if fully_loaded else "uniquement)" +
                 " en " + str("{:.2f}".format((time.time() - initial_time) * 1000)) + " millisecondes.\n\n",
                 prefix="Initialisation DMI ETCS ; section " + section)

    def run(self):
        # Lance la logique de mise à jour sur un nouveau thread
        logic = threading.Thread(target=self.update)
        logic.start()

        # Montre la fenêtre générale du DMI
        # Lance l'application et cherche pour le fichier QML avec tous les éléments de la fenêtre d'initialisation
        self.dmi_window.show()

    def update(self):
        # Pour chacune des sections
        for folder in ["A", "B", "C", "D", "E", "F", "G"]:
            # Pour chacunes des pages de chaque sections
            files = list(self.pages[folder].keys())
            for file in files:
                # Si la page a correctement été chargée et que la page a une fonction update
                if self.pages[folder][file] is not None and \
                        not isinstance(self.pages[folder][file], type(self.engine)) and\
                        "update" in dir(self.pages[folder][file]):
                    # Essaye d'appeler la fonction update (et attrape les erreurs s'il y a une erreur
                    try:
                        self.pages[folder][file].update()
                    except Exception as error:
                        log.warning("Erreur lors de la mise à jour de la page" + folder + "." + file + " du DMI.\n\t\t" +
                                    "Erreur de type : " + str(type(error)) + "\n\t\t" +
                                    "Avec comme message d\'erreur : " + str(error.args) +
                                    "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                                    prefix="Update DMI ETCS ; section " + folder)
                else:
                    log.debug("Aucune fonction update pour la section" + folder + "." + file + " du DMI.\n",
                              prefix="Initialisation DMI ETCS ; section " + folder)                                     #FIXME : à vérifier lors de l'initialisation pour éviter le spam


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
