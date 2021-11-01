#Librairies par défaut
import sys
import os


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

    def save(self, file_path):
        """Méthode permettant de sauvegarder les paramètres dans un fichier

        Parameters
        ----------
        file_path: `string`
        """
        try:
            # Essaye de créer (ou d'écraser) le fichier avec les paramètres actuels
            file = open(file_path, "w", encoding="utf-_-sig")
        except Exception:
            # Cas où le fichier ouvert n'est pas accessible
            log.warning("Impossible d'enregistrer le fichier :\n\t\t" + str(file_path + "\n"))
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
        except Exception:
            # Cas où le fichier ouvert n'existe pas ou qu'il n'est pas accessible
            log.warning("Impossible d'ouvrir le fichier :\n\t\t" + str(file_path) + "\n")
            return

        # Récupère la longueur actuelle
        current_length = len(self)

        # Si le fichier est ouvert, récupère chaque lignes de celui-ci
        for line in file:
            # Si la ligne ne contient pas le délimiteur (ici ;) l'indique dans les logs et saute la ligne
            if ";" not in line:
                log.debug("Ligne sautée. Délimiteur \";\" manquant dans la ligne :\n\t\t" + line + '\n')
            else:
                # Récupère les deux éléments de la ligne
                line = line.rstrip('\n').split(";")

                # Regarde s'il peut être convertir en bool?
                if line[1] == "True" or line[1] == "False":
                    line[1] = True if line[1] == "True" else False
                    continue

                # regarde s'il peut être convertit en int ou en float
                try:
                    line[1] = float(line[1])
                except ValueError:
                    pass
                else:
                    if line[1].is_integer():
                        line[1] = int(line[1])

                # Ajouter la nouvelle valeur au dictionnaire
                self[line[0]] = line[1]

        file.close()

        # Indique en debug le nombre d'éléments récupérées
        log.debug(str(current_length - len(self)) + " éléments récupérés dans :\n\t\t" + str(file_path) + "\n")
