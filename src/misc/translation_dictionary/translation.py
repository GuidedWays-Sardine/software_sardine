#Librairies par défaut
import sys
import os
import re
import functools


# Livbrairies graphiques
from PyQt5.QtCore import QObject


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.decorators as decorators


class TranslationDictionary(dict):
    """Classe permettant de convertir un fichier de traduction en un dictionnaire de traductions fonctionnel."""

    def __init__(self, translations=None):
        """Initialise le dictionnaire de traductions.

        Parameters
        ----------
        translations: `dict[str, str] | TranslationDictionary | None`
            traductions à insérer lors de l'initialisation du paramètres (non obligatoire).
        """
        # Initialise la base du dictionnaire de paramètres
        super().__init__()

        # Si un dictionnaire de paramètres a été envoyé ajoute chacun de ses arguments
        if isinstance(translations, dict):
            for key, value in translations.items():
                self.__setitem__(key, value)

    def __setitem__(self, key, value):
        """Opérateur self["key"] = value permettant de rajouter des valeurs dans le dictionnaire de traduction.

        Parameters
        ----------
        key: `str`
            Mot à traduire (non sensible aux minuscules et aux majuscules) ;
        value: `str`
            Sa traduction.
        """
        if isinstance(key, str) and isinstance(value, str):
            super(TranslationDictionary, self).__setitem__(key.lower(), value)
        else:
            log.debug(f"La traduction {{{key}: {value}}}, n'est pas du texte ({{{type(key)} : {type(value)}}}).")

    def __getitem__(self, key):
        """Opérateur value = self["key"] permettant de lire des valeurs du dictionnaire de traduction.

        Parameters
        ----------
        key: `str`
            Mot à traduire (non sensible aux minuscules et aux majuscules).

        Returns
        -------
        value: `str`
            Sa traduction si elle existe sinon le mot non traduit.
        """
        try:
            return super(TranslationDictionary, self).__getitem__(key.lower())
        except KeyError:
            log.debug(f"Aucune traduction correspondant à la clé : \"{key}\".")
            return key

    @decorators.UIupdate
    @decorators.QtSignal(log_level=log.Level.DEBUG, end_process=False)
    def translate_widget_property(self, widget=None, parent=None, widget_name=None, property_name="") -> None:
        """Traduit la propriété d'un composant.

        Parameters
        ----------
        widget: `QObject`
            Composant à traduire (dans le cas où le composant est directement envoyé) ;
        parent: `QObject | QWindow`
            Fenêtre/Page contenant le composant (dans le cas où le composant doit-être récupéré) ;
        widget_name: `str`
            Nom (objectName) du composant (dans le cas où le composant doit-être récupéré) ;
        property_name: `string`
            Nom de la propriété à traduire.
        """
        # Si le composant a directement été envoyé et qu'une propriété a été envoyée aussi
        if widget is not None and property_name:
            widget.setProperty(property_name, self[widget.property(property_name)])
        # Si le parent et le nom du composant ainsi qu'une propriété ont été envoyés
        elif parent is not None and widget_name and property_name:
            widget = parent.findChild(QObject, widget_name)
            widget.setProperty(property_name, self[widget.property(property_name)])
        # Si l'une des données n'a pas été correctement été envoyée
        else:
            # Si la property_name n'a pas été envoyée avec un widget, l'indique dans le registre
            if not property_name and widget is not None:
                log.debug(f"Aucun nom de propriété envoyé pour la traduction de \"{widget.property('objectName')}\".")
            # Sinon, indique le nom du composant du parent et la raison dans le registre
            elif not property_name and widget is None:
                log.debug(f"Aucun nom de propriété envoyé pour la traduction de \"{widget_name}\"" +
                          f"de la fenêtre/page : {parent.property('objectName')}." if parent is not None else ".")

            # Si aucun composant n'a été envoyé, l'indique dans le registre
            if not widget and not widget_name and not parent and not property_name:
                log.debug("Appel de la fonction de traduction de composant vide, appel inutile")
            elif not widget and not widget_name and not parent and property_name:
                log.debug(f"Tentative du changement de la propriété \"{property_name}\" d'un composant inconnu.")

    def create_translation(self, file_path, current_language, new_language, delimiter=";"):
        """Ouvre un fichier de traduction et récupèré toute les traductions.

        Parameters
        ----------
        file_path: `str`
            chemin d'accès vers le fichier de traductions à ouvrir et lire ;
        current_language: `str`
            Langue de ce qui doit être traduit ;
        new_language: `str`
            Langue des traductions ;
        delimiter: `str`
            Délimiteur séparant les différentes traductions ";" par défaut.

        Returns
        -------
        successful: `bool`
            Indique si la lecture du fichier de traductions a été réussie.
        """
        try:
            # Parceque windows pue du cul, les fichiers Excel (csv et txt) sont sauvegardés en ANSI et non en UTF-8
            # Si le fichier n'est pas encodé en UTF-8 (et donc surement sauvegardé sous Excel), le convertit en UTF-8
            try:
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    file.readline()
            except (UnicodeDecodeError, UnicodeError):
                log.debug("Les fichiers enregistrés sous Excel ne sont pas en UTF-8 (ANSI - Windows-1252). " +
                          f"Éviter la modification et sauvegarde de fichiers paramètres sous Excel.\n\t{file_path}",
                          prefix=f"Module traductions")

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
                    log.warning(f"La langue : {current_language} ou {new_language} n'existe pas : \n\t{language_list}",
                                prefix=f"Chargement traductions \"" + re.split(r"[/\\]+", file_path)[-1] + "\"")
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
                                  f"sur la ligne : \n\t{line}",
                                  prefix=f"Chargement traductions \"" + re.split(r"[/\\]+", file_path)[-1] + "\"")
        except Exception as error:
            # Cas où le fichier ouvert n'est pas accessible, indique la raison et retourne false
            log.warning(f"Impossible d'ouvrir le fichier de traductions : \n\t{file_path}", exception=error,
                        prefix=f"Chargement traductions \"" + re.split(r"[/\\]+", file_path)[-1] + "\"")
            return False
        else:
            # Indique le nombre d'éléments récupérées dans le registre et retourne vrai
            if (len(self) - current_length) == 0:
                log.debug(f"Aucune nouvelle traduction dans le fichier : \n\t{file_path}",
                          prefix=f"Chargement traductions \"" + re.split(r"[/\\]+", file_path)[-1] + "\"")
            else:
                log.debug(f"{len(self) - current_length} nouvelle{'s' if (len(self) - current_length) > 1 else ''} " +
                          f"traduction{'s' if (len(self) - current_length) > 1 else ''} dans le fichier :\n\t{file_path}",
                          prefix=f"Chargement traductions \"" + re.split(r"[/\\]+", file_path)[-1] + "\"")
            return True


@functools.lru_cache(maxsize=len(os.listdir(f"{PROJECT_DIR}/settings/language_settings/")))
def get_language_list(file_path):
    """Récupère la liste des langues dans un fichier de traduction.

    Parameters
    ----------
    file_path: `str`
        Chemin d'accès vers le fichier de traduction.

    Returns
    -------
    language_list: `tuple[str]`
        Liste des langues détectées dans le fichier de traduction.
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
                      f"Éviter la modification et sauvegarde de fichiers paramètres sous Excel.\n\t{file_path}",
                      prefix="Module traductions")

            # Ouvre le fichier avec l'encoding ANSI (utilisé par Excel)
            with open(file_path, "r", encoding="ANSI") as file:
                contents = file.readlines()

            # L'enregistre dans le même fichier avec l'encoding utf-8-sig en décodant les lignes
            with open(file_path, "w", encoding="utf-8-sig") as file:
                for line in contents:
                    file.write(line.replace("\t", ";").replace("\"", ""))

        # Ouvre le fichier de nouveau et retourne la liste des langues détectées
        with open(file_path, "r", encoding="utf-8-sig") as file:
            languages = tuple(file.readline().rstrip('\n').split(";"))
            if not languages:
                log.warning(f"Aucune langue détectée dans le fichier : \n\t{file_path}", prefix="Module traductions")
            else:
                log.info(f"{len(languages)} langue{'s' if len(languages) > 1 else ''} dans le fichier : \n\t{file_path}",
                         prefix="Module traductions")
            return languages
    # Si une erreur a été récupérée (fichier ouvert dans un autre logiciel, ...
    except Exception as error:
        # Cas où le fichier ouvert n'est pas accessible, indique la raison et retourne false
        log.warning(f"Impossible d'ouvrir le fichier de traduction : {file_path}",
                    exception=error, prefix="Module de traductions")
        return ()
