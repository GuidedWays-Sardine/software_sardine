#Librairies par défaut
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log


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

        Returns
        -------
        successful: `bool`
            Retourne si la lecture du fichier de traductions a été réussie (sinon erreur détectée)
        """
        try:
            # Parceque windows pue du cul, les fichiers Excel (csv et txt) sont sauvegardés en ANSI et non en UTF-8
            # Si le fichier n'est pas encodé en UTF-8 (et donc surement sauvegardé sous Excel), le convertit en UTF-8
            try:
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    file.readline()
            except (UnicodeDecodeError, UnicodeError):
                log.debug("Les fichiers enregistrés sous Excel ne sont pas en UTF-8 (ANSI - Windows-1252). " +
                          f"Éviter la modification et sauvegarde de fichiers paramètres sous Excel.\n\t{file_path}")

                # Ouvre le fichier avec l'encoding ANSI (utilisé par Excel)
                with open(file_path, "r", encoding="ANSI") as file:
                    contents = file.readlines()

                # L'enregistre dans le même fichier avec l'encoding utf-8-sig en décodant les lignes
                with open(file_path, "w", encoding="utf-8-sig") as file:
                    for line in contents:
                        file.write(line.replace("\t", ";").replace("\"", ""))

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
                    return False

                # Récupère la longueur actuelle
                current_length = len(self)

                # Ajoute la traduction de la langue actuelle
                self[current_language] = new_language

                # Pour chacune des lignes contenant des traductions (saute les lignes vides et avec des commentaires)
                for line in (l for l in file if l != "\n" and l[0] != "#"):
                    # récupère toutes les traductions présentes sur la ligne
                    translations = list(map(str.strip, line.rstrip('\n').split(delimiter)))

                    # Si la ligne contient le bon nombre de traduction, récupère les 2 traductions nécessaires
                    if len(translations) == len(language_list):
                        self[translations[current_index]] = translations[new_index]
                    else:
                        # S'il n'y a pas autant de traductions que de langue, cela signifie que la ligne est incomplète
                        log.debug(f"Certaines traductions manquantes ({len(translations)}/{len(language_list)}) " +
                                  f"sur la ligne : \n\t{line}")
        except Exception as error:
            # Cas où le fichier ouvert n'est pas accessible, indique la raison et retourne false
            log.warning(f"Impossible d'ouvrir le fichier de traduction : {file_path}",
                        exception=error,  prefix="dictionaire de traduction")
            return False
        else:
            # Indique le nombre d'éléments récupérées dans le registre et retourne vrai
            log.debug(f"{len(self) - current_length} nouvelles traductions récupérées dans le fichier :\n\t {file_path}",
                      prefix="dictionaire de traduction")
            return True


def get_language_list(file_path):
    """Fonction permettant de récupérer la liste des langues dans un fichier de traduction

    Parameters
    ----------
    file_path: `str`
        chemin d'accès vers le fichier de traduction

    Returns
    -------
    language_list: `tuple[str]`
    """
    try:
        # Parceque windows pue du cul, les fichiers Excel (csv et txt) sont sauvegardés en ANSI et non en UTF-8
        # Si le fichier n'est pas encodé en UTF-8 (et donc surement sauvegardé sous Excel), le convertit en UTF-8
        try:
            with open(file_path, "r", encoding="utf-8-sig") as file:
                # Pour l'optimisation (et éviter la double ouverture du fichier) esssaye de retourner la liste de suite
                return tuple(file.readline().rstrip('\n').split(";"))
        except (UnicodeDecodeError, UnicodeError):
            log.debug("Les fichiers enregistrés sous Excel ne sont pas en UTF-8 (ANSI - Windows-1252). " +
                      f"Éviter la modification et sauvegarde de fichiers paramètres sous Excel.\n\t{file_path}")

            # Ouvre le fichier avec l'encoding ANSI (utilisé par Excel)
            with open(file_path, "r", encoding="ANSI") as file:
                contents = file.readlines()

            # L'enregistre dans le même fichier avec l'encoding utf-8-sig en décodant les lignes
            with open(file_path, "w", encoding="utf-8-sig") as file:
                for line in contents:
                    file.write(line.replace("\t", ";").replace("\"", ""))

        # Ouvre le fichier de nouveau et retourne la liste des langues détectées
        with open(file_path, "r", encoding="utf-8-sig") as file:
            return tuple(file.readline().rstrip('\n').split(";"))
    # Si une erreur a été récupérée (fichier ouvert dans un autre logiciel, ...
    except Exception as error:
        # Cas où le fichier ouvert n'est pas accessible, indique la raison et retourne false
        log.warning(f"Impossible d'ouvrir le fichier de traduction : {file_path}",
                    exception=error, prefix="dictionaire de traduction")
        return ()
