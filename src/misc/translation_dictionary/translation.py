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
            log.debug(f"la clé : {key}, n'est pas de type string : {type(key)}\n")

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
            log.debug(f"Aucune traduction pour : {key}\n")
            return key

    def create_translation(self, file_path, current_language, new_language):
        """Méthode permettant d'ouvrir un fichier de traduction et de rajouter les traductions

        Parameters
        ----------
        file_path: `str`
            chemin d'accès vers le fichier de traductions à ouvrir et lire
        current_language: `str`
            la langue actuelle de ce qui doit être tradui
        new_language: `str`
            la langue dans laquelle il faut récupérer les traductions
        """
        try:
            current_index, new_index = None, None
            # essaye d'ouvrir le fichier avec les traductions
            with open(file_path, "r", encoding="utf-8-sig") as file:
                try:
                    # Récupère les index des langues (dans le cas où elles existent
                    language_list = file.readline().upper().rstrip('\n').split(";")
                    language_list = list(map(str.strip, language_list))
                    current_index = language_list.index(current_language.upper())
                    new_index = language_list.index(new_language.upper())
                except ValueError:
                    # Si l'une des langues n'existe pas (la combobox langue est générée automatiquement, donc par redondance)
                    log.warning(f"Langues : {current_language} ; " if current_index is not None else "" +
                                str(new_language) if new_index is not None else "" + "\n")
                    return

                # Récupère la longueur actuelle
                current_length = len(self)

                # Ajoute la traduction de la langue actuelle
                self[current_language] = new_language

                # our chacune des lignes contenant des traductions (saute les lignes vides et avec des commentaires)
                for line in (l for l in file if l != "\n" and l[0] != "#"):
                    # récupère toutes les traductions présentes sur la ligne
                    translations = list(map(str.strip, line.rstrip('\n').split(";")))

                    # Si la ligne contient le bon nombre de traduction, récupère les 2 traductions nécessaires et les ajoute
                    if len(translations) == len(language_list):
                        self[translations[current_index]] = translations[new_index]
                    else:
                        # S'il n'y a pas autant de traductions que de langue, cela signifie que la ligne est incomplète
                        log.debug(f"""Certaines traductions manquantes sur la ligne suivante (langues attendus, mots) :
                                  \t\t{';'.join(language_list)}\n\t\t{line}\n""",
                                  prefix="dictionaire de traduction")
        except Exception as error:
            # Cas où le fichier ouvert n'est pas accessible
            log.warning(f"Impossible d'ouvrir le fichier de traduction : {file_path}\n",
                        exception=error,  prefix="dictionaire de traduction")
        else:
            # Indique en debug le nombre d'éléments récupérées
            log.debug(f"{len(self) - current_length} éléments récupérés dans : {file_path}\n",
                      prefix="dictionaire de traduction")
