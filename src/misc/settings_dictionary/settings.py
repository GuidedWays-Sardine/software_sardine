# Librairies par défaut
import sys
import os
from typing import Union


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
            log.debug(f"""Impossible de changer le paramètre : {property} du composant {widget_id}
                      \t\tPas de valeurs pour le paramètre : {key} dans le fichier ouvert.\n""")

    def save(self, file_path):
        """Méthode permettant de sauvegarder les paramètres dans un fichier

        Parameters
        ----------
        file_path: `string`
        """
        try:
            # Essaye de créer (ou d'écraser) le fichier avec les paramètres actuels
            with open(file_path, "w", encoding="utf-8-sig") as file:
                # Ecrit chacune des clés à l'intérieur séparé par le délimiteur
                for key in self.keys():
                    file.write(f"{key};{self[key]}\n")
        except Exception as error:
            # Cas où le fichier ouvert n'est pas accessible
            log.warning(f"Impossible d'enregistrer le fichier : {file_path}.\n",
                        exception=error, prefix="dictionaire de données")

    def open(self, file_path):
        """Méthode permettant d'ouvrir un fichier de paramètres et de rajouter les paramètres au dictionnaire

        Parameters
        ----------
        file_path: `string`
            chemin d'accès vers le fichier de paramètres à ouvrir et lire
        """
        # Récupère la longueur actuelle
        current_length = len(self)

        try:
            # Essaye d'ouvrir le fichier avec les paramètres
            with open(file_path, "r", encoding="utf-8-sig") as file:
                # Si le fichier est ouvert, récupère chaque lignes de celui-ci
                for line in file:
                    # Si la ligne ne contient pas le délimiteur (ici ;) l'indique dans les logs et saute la ligne
                    if ";" not in line:
                        log.debug("Ligne sautée. Délimiteur \";\" manquant dans la ligne : {line} \n",
                                  prefix="dictionaire de données")
                    else:
                        # Récupère les deux éléments de la ligne et les ajoutent comme clé et valeur
                        line = list(map(str.strip, line.rstrip('\n').split(";")))
                        line[0] = SettingsDictionnary.convert_type(line[1])

        except Exception as error:
            # Cas où le fichier ouvert n'existe pas ou qu'il n'est pas accessible
            log.warning(f"Impossible d'ouvrir le fichier : {file_path}.\n",
                        exception=error, prefix="dictionaire de données")
        else:
            # Indique en debug le nombre d'éléments récupérés
            log.debug(f"{len(self) - current_length} éléments récupérés dans : {file_path}\n",
                      prefix="dictionaire de traduction")

    @staticmethod
    def convert_type(data):
        """Fonction permettant de convertir un string de la data en son type correct.
        Fonctionne pour tous les types immutables par défaut

        Parameters
        ----------
        data: `string`
            donnée à convertir

        Returns
        -------
        converted_data : `Union[bool, int, float, None, str]`
            donnée convertie (string si aucun moyen de le convertir)
        """
        # Regarde s'il peut être convertir en bool?
        if data.lower() == "true" or data.lower() == "false":
            return data.lower() == "true"

        # Regarde s'il peut être convertit en int
        if data.isnumeric():
            return int(data)

        # Regarde s'il peut être convertit en float
        if data.replace(".", "", 1).isnumeric():
            return float(data)

        # Regarde s'il peut être convertit en NoneType
        if data.lower == "none":
            return None

        # Dans tous les cas (si aucun des autres cas n'a été intercepté) retourne le string
        return data
