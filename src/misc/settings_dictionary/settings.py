# Librairies par défaut
import sys
import os
import traceback


# Librairies graphiques
from PyQt5.QtCore import QObject


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


class SettingsDictionnary(dict):
    """Classe permettant de convertir un fichier de paramètres en un dictionnaire fonctionnel"""

    def __setitem__(self, key, value):
        super(SettingsDictionnary, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(SettingsDictionnary, self).__getitem__(key.lower())

    def update_parameter(self, page, widget_id, property, key):
        """Structure pour mettre à jour une propriété.

        Parameters
        ----------
        page: `QObject`
            la page contenant le composant
        widget_id: `string`
            l'id du composant qui doit être mis à jour
        property: `string`
            le nom de la propriété  à mettre à jour
        key: `Any`
            la clé vers la nouvelle valeur
        """
        try:
            page.findChild(QObject, widget_id).setProperty(property, self[key])
        except KeyError:
            log.debug("Impossible de changer le paramètre : " + property + " du composant" + widget_id + ".\n\t\t" +
                      "Pas de valeurs pour le paramètre : " + key + " dans le fichier ouvert.\n")

    def save(self, file_path):
        """Méthode permettant de sauvegarder les paramètres dans un fichier

        Parameters
        ----------
        file_path: `string`
        """
        try:
            # Essaye de créer (ou d'écraser) le fichier avec les paramètres actuels
            file = open(file_path, "w", encoding="utf-8-sig")
        except Exception as error:
            # Cas où le fichier ouvert n'est pas accessible
            log.warning("Impossible d'enregistrer le fichier :\n\t\t" + str(file_path + "\n") +
                        "\n\t\tErreur de type : " + str(type(error)) +
                        "\n\t\tAvec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                        "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                        prefix="dictionaire de données")
        else:
            for key in self.keys():
                file.write(str(key) + ";" + str(self[key]) + "\n")

            # Ferme le fichier
            file.close()

    def open(self, file_path):
        """Méthode permettant d'ouvrir un fichier de paramètres et de rajouter les paramètres au dictionnaire

        Parameters
        ----------
        file_path: `string`
            chemin d'accès vers le fichier de paramètres à ouvrir et lire
        """
        try:
            # Essaye d'ouvrir le fichier avec les paramètres
            file = open(file_path, "r", encoding="utf-8-sig")
        except Exception as error:
            # Cas où le fichier ouvert n'existe pas ou qu'il n'est pas accessible
            log.warning("Impossible d'ouvrir le fichier :\n\t\t" + str(file_path) + "\n" +
                        "\n\t\tErreur de type : " + str(type(error)) +
                        "\n\t\tAvec comme message d'erreur : " + str(error.args) + "\n\n\t\t" +
                        "".join(traceback.format_tb(error.__traceback__)).replace("\n", "\n\t\t") + "\n",
                        prefix="dictionaire de données")
            return

        # Récupère la longueur actuelle
        current_length = len(self)

        # Si le fichier est ouvert, récupère chaque lignes de celui-ci
        for line in file:
            # Si la ligne ne contient pas le délimiteur (ici ;) l'indique dans les logs et saute la ligne
            if ";" not in line:
                log.debug("Ligne sautée. Délimiteur \";\" manquant dans la ligne :\n\t\t" + line + '\n',
                          prefix="dictionaire de données")
            else:
                # Récupère les deux éléments de la ligne
                line = list(map(str.strip, line.rstrip('\n').split(";")))

                # Regarde s'il peut être convertir en bool?
                if line[1] == "True" or line[1] == "False":
                    self[line[0]] = True if line[1] == "True" else False
                    continue

                # Regarde s'il peut être convertit en int ou en float
                try:
                    line[1] = float(line[1])
                except ValueError:
                    pass
                else:
                    if line[1].is_integer():
                        self[line[0]] = int(line[1])
                    else:
                        self[line[0]] = int(line[1])
                    continue

                # Dans le cas où aucun type autre que string a été détecté
                if isinstance(line[1], type(" ")):
                    self[line[0]] = line[1]

        file.close()

        # Indique en debug le nombre d'éléments récupérés
        log.debug(str(len(self) - current_length) + " éléments récupérés dans :\n\t\t" + str(file_path) + "\n",
                  prefix="dictionaire de traduction")
