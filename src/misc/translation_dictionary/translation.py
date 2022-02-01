#Librairies par défaut
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


class TranslationDictionary(dict):
    """Classe permettant de convertir un fichier de paramètres en un dictionnaire fonctionnel"""

    def __setitem__(self, key, value):
        """Opérateur self["key"] = value permettant de rajouter des valeurs dans le dictionnaire de traduction

        Parameters
        ----------
        key: `str`
            Mot à traduire (non sensible aux minuscules et aux majuscules)
        value: `str`
            Sa traduction
        """
        if isinstance(key, str):
            super(TranslationDictionary, self).__setitem__(key.lower(), value)
        else:
            log.debug(f"la clé : {key}, n'est pas de type string : {type(key)}")

    def __getitem__(self, key):
        """Opérateur value = self["key"] permettant de lire des valeurs du dictionnaire de traduction

        Parameters
        ----------
        key : `str`
            Mot à traduire (non sensible aux minuscules et aux majuscules)

        Returns
        -------
        value: `str`
            Sa traduction si elle existe sinon le mot non traduit
        """
        try:
            return super(TranslationDictionary, self).__getitem__(key.lower())
        except KeyError:
            log.debug(f"Aucune traduction pour : \"{key}\".")
            return key

    def create_translation(self, file_path, current_language, new_language, delimiter=";"):
        """Méthode permettant d'ouvrir un fichier de traduction et de rajouter les traductions

        Parameters
        ----------
        file_path: `str`
            chemin d'accès vers le fichier de traductions à ouvrir et lire
        current_language: `str`
            la langue actuelle de ce qui doit être tradui
        new_language: `str`
            la langue dans laquelle il faut récupérer les traductions
        delimiter: `str`
            délimteur séparant les différentes traductions ";" par défaut
        """
        try:
            # essaye d'ouvrir le fichier avec les traductions
            with open(file_path, "r", encoding="utf-8-sig") as file:
                try:
                    # Récupère les index des langues (dans le cas où elles existent
                    language_list = file.readline().lower().rstrip('\n').split(delimiter)
                    language_list = list(map(str.strip, language_list))
                    current_index = language_list.index(current_language.lower())
                    new_index = language_list.index(new_language.lower())
                except ValueError:
                    # Si l'une des langues n'existe envoyée n'existe pas
                    log.warning(f"La langue : {current_language} ou {new_language} n'existe pas : \n\t{language_list}")
                    return

                # Récupère la longueur actuelle
                current_length = len(self)

                # Ajoute la traduction de la langue actuelle
                self[current_language] = new_language

                # Pour chacune des lignes contenant des traductions (saute les lignes vides et avec des commentaires)
                for line in (l for l in file if l != "\n" and l[0] != "#"):
                    # récupère toutes les traductions présentes sur la ligne
                    translations = list(map(str.strip, line.rstrip('\n').split(delimiter)))

                    # Si la ligne contient le bon nombre de traduction, récupère les 2 traductions nécessaires et les ajoute
                    if len(translations) == len(language_list):
                        self[translations[current_index]] = translations[new_index]
                    else:
                        # S'il n'y a pas autant de traductions que de langue, cela signifie que la ligne est incomplète
                        log.debug(f"Certaines traductions manquantes ({len(translations)}/{len(language_list)}) " +
                                  f"sur la ligne : \n\t{line}")
        except Exception as error:
            # Cas où le fichier ouvert n'est pas accessible
            log.warning(f"Impossible d'ouvrir le fichier de traduction : {file_path}",
                        exception=error,  prefix="dictionaire de traduction")
        else:
            # Indique en debug le nombre d'éléments récupérées
            log.debug(f"{len(self) - current_length} éléments récupérés dans : {file_path}",
                      prefix="dictionaire de traduction")
