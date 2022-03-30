# Librairies par défaut
import sys
import os
import re


# Librairies graphiques
from PyQt5.QtCore import QObject


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log
import src.misc.decorators.decorators as decorators
import src.misc.translation_dictionary.translation as td


class SettingsDictionary(dict):
    """Classe permettant de convertir un fichier de paramètres en un dictionnaire fonctionnel"""

    def __setitem__(self, key, value):
        """Opérateur self["key"] = value permettant de rajouter des valeurs dans le dictionnaire de paramètres

        Parameters
        ----------
        key: `str`
            Nom du paramètre (non sensible aux minuscules et aux majuscules)
        value: `Any`
            Sa valeur
        """
        # Enlève les charactères problématiques de la clé (ici ";" et "\t")
        key = re.sub("[;\t]", "", str(key).lower())

        # Vérifie si la clé a déjà une valeur et si c'est le cas, laisse un message de debug l'indiquant
        if key in self:
            log.debug(f"La clé \"{key}\" a déjà une valeur asignée qui sera écrasée ({self[key]} -> {value}).")

        super(SettingsDictionary, self).__setitem__(key, value)

    def __getitem__(self, key):
        """Opérateur value = self["key"] permettant de lire des valeurs du dictionnaire de paramètres

        Parameters
        ----------
        key : `str`
            Nom du paramètre (non sensible aux minuscules et aux majuscules)

        Returns
        -------
        value: `Any`
            Sa valeur associée (si elle existe)

        Raises
        ------
        KeyError :
            Jetté si la clé n'a pas de valeur associée
        """
        # Retourne la valeur avec la clé envoyée et nétoyée
        return super(SettingsDictionary, self).__getitem__(re.sub("[;\t]", "", str(key).lower()))

    def get_value(self, key, default=None):
        """Méthode pour récupérer une valeur à partir de sa clé, et de mettre un message dans le registre s'il n'existe pas

        Parameters
        ----------
        key: `string`
            La clé à vérifier (la valeur associée à la clé sera retournée si elle existe
        default: `Any`
            La valeur à retourner si la clé n'a pas de valeurs associés (pour une facilité de lecture du code).

        Returns
        -------
        value: `Any`
            La valeur associée à la clé (si elle existe dans le dictionnaire) sinon la valeur par défaut
        """
        try:
            return self[key]
        except KeyError:
            log.debug(f"Aucun paramètre \"{key.lower()}\" dans le dictionnaire de paramètres ouvert.")
            return default

    @decorators.UIupdate
    @decorators.QtSignal(log_level=log.Level.WARNING, end_process=False)
    def update_ui_parameter(self, component, property_name, key, translations=None):
        """Méthode pour mettre à jour une propriété d'un composant qml à partir de son ID et de la propriété.

        Parameters
        ----------
        component: `QObject`
            Le composant à mettre à jour
        property_name: `string`
            le nom de la propriété  à mettre à jour
        key: `Any`
            la clé vers la nouvelle valeur
        translations: `td.TranslationDictionary | None`
            traductions (clés = anglais -> valeurs = langue actuelle)
            Utile pour traduire la sélection dans le cas d'un composant à choix
        """
        # Différencie les cas des composants avec un "selection_value"
        try:
            # Cas des valueinput, dont la valeur doit être changée avec la fonction change_value
            if property_name == "value":
                component.change_value(self[key])
            # Cas du changement de sélection de la combobox (obligatoirement avec la fonction change_selection)
            elif "selection" in property_name:
                # Récupère la valeur en tant qu'entier ou string selon si selection_index ou selection_
                value = int(self["key"]) if property_name == "selection_index" else str(self["key"])
                if isinstance(translations, td.TranslationDictionary):
                    # Cas où un dictionnaire de traduction a été envoyé, pour traduire la sélection
                    component.change_selection(translations[value])
                else:
                    # Cas où l'utilisateur a oublié d'envoyer un dictionaire de paramètres
                    log.debug(f"Changement de sélection avec la clé \"{key}\", sans dictionaire de paramètres.")
                    component.change_selection(value)
            # Cas général où la propriété peut être changée sans fonction
            else:
                component.setProperty(property_name, self[key])
        except KeyError:
            # Cas où la clé ne mène a aucun paramètre
            log.debug(f"Impossible de changer le paramètre : \"{property_name}\" du composant envoyé.\n\t" +
                      f"Pas de valeurs pour le paramètre : \"{key}\" dans le fichier ouvert.")
        except AttributeError:
            # Cas où le composant n'est pas valide
            log.debug(f"Le composant envoyé n'existe pas (None reçu) lors de la mise à jour du paramètre " +
                      f"\"{property_name}\" avec la clé \"{key}\".")

    def save(self, file_path, delimiter=";"):
        """Méthode permettant de sauvegarder les paramètres dans un fichier

        Parameters
        ----------
        file_path: `string`
            Chemin d'accès vers le fichier de paramètres (celui-ci sera écrasé)
        delimiter: `str`
            délimiteur séparant les différentes paramètres ";" par défaut
        """
        try:
            # Essaye de créer (ou d'écraser) le fichier avec les paramètres actuels
            with open(file_path, "w", encoding="utf-8-sig") as file:
                # Ecrit chacune des clés à l'intérieur séparé par le délimiteur
                for key, value in self.items():
                    file.write(f"{key}{delimiter}{value}\n")
        except Exception as error:
            # Cas où le fichier ouvert n'est pas accessible
            log.warning(f"Impossible d'enregistrer le fichier, l'action ne sera pas prise en compte.\n\t{file_path}",
                        exception=error, prefix="Sauvegarde des données")
        else:
            log.info(f"Enregistrement de {len(self)} données dans : {file_path}")

    def open(self, file_path, delimiter=(";", "\t")):
        """Méthode permettant d'ouvrir un fichier de paramètres et de rajouter les paramètres au dictionnaire

        Parameters
        ----------
        file_path: `string`
            chemin d'accès vers le fichier de paramètres
        delimiter: `str | tuple | list`
            potentiels délimiteurs séparant les différentes paramètres ";" ou "\t" par défaut
        """
        # Récupère la longueur actuelle
        current_length = len(self)

        try:
            # Essaye d'ouvrir le fichier avec les paramètres
            with open(file_path, "r", encoding="utf-8-sig") as file:
                # Récupère chacune des lignes du fichier
                lines = file.readlines()

                # Si plusieurs délimiteurs ont été envoyés, trouve celui utilisé pour le fichier
                if lines and isinstance(delimiter, (tuple, list)):
                    for delim in reversed(delimiter):
                        # Si ce délimiteur se trouve dans la ligne, le choisit comme nouveau délimiteur par défaut
                        if delim in lines[0]:
                            delimiter = delim

                    # Si aucun des délimiteurs ne se trouve sur la ligne, définit le premier comme celui utilisé
                    if isinstance(delimiter, (tuple, list)):
                        # Dans le cas où une liste vide de délimiteur a été envoyée utilise ";"
                        delimiter = ";" if not delimiter else delimiter[0]

                # Si le fichier est ouvert, récupère chaque lignes de celui-ci
                for line in lines:
                    # Si la ligne ne contient pas le délimiteur (ici ; ou \t) l'indique dans les logs et saute la ligne
                    if delimiter in line:
                        # Récupère les deux éléments de la ligne et les ajoutent comme clé et valeur
                        line = list(map(str.strip, line.rstrip('\n').split(delimiter, maxsplit=1)))
                        self[line[0]] = SettingsDictionary.convert_type(line[1])
                    else:
                        log.debug(f"Ligne sautée. Délimiteur \"{delimiter}\" manquant dans la ligne : {line}",
                                  prefix="Lecture des données")

        except Exception as error:
            # Cas où le fichier ouvert n'existe pas ou qu'il n'est pas accessible
            log.warning(f"Impossible d'ouvrir le fichier, action non prise en comtpe. \n\t{file_path}",
                        exception=error, prefix="Lecture des données")
        else:
            # Indique en debug le nombre d'éléments récupérés
            log.debug(f"{len(self) - current_length} nouveaux paramètres récupérés dans le fichier :\n\t{file_path}",
                      prefix="dictionaire de paramètres")

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
        converted_data : `bool | int | float | str | None`
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
        if data.lower() == "none":
            return None

        if data[0] == "(" and data[-1] == ")":
            return tuple(SettingsDictionary.convert_type(ele.strip()) for ele in data[1:-1].split(",") if ele)

        if data[0] == "[" and data[-1] == "]":
            return list(SettingsDictionary.convert_type(ele.strip()) for ele in data[1:-1].split(",") if ele)

        # Dans tous les cas (si aucun des autres cas n'a été intercepté) retourne le string
        return data
