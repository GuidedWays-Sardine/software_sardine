import logging


def read_data_file(file_path, delimiter = ';'):
    """Ouvre un fichier au format csv récupère les donés et les retournes dans un dictionnaire

    Parameters
    ----------
    file_path: `str`
        chemin vers le fichier à ouvrir
    delimiter: `str`
        charactère délimitant le nom de lma variable et sa valeur : ";" par défaut

    Raises
    ------
    FileNotFoundError
        Si le fichier ouvert n'existe pas ou que le chemin fournis n'est pas correct

    Return
    ------
    data: `dict`
        Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        (Attention: Toutes les valeurs sont retournés en format texte)
    """
    data = {}

    # Essaye d'ouvrir le fichier envoyer, et jette une erreur si le fichier n'exsite pas
    file = open(file_path, "r")

    # Lit chaque ligne du fichier
    for line in file:
        # Si la ligne ne contient pas le délimiteur (et donc que le fichier
        if not delimiter in line:
            logging.warning("Aucun délimiteur : \"" + delimiter + "\" dans la ligne : " + line +
                            + "\n\t\t La ligne n\'est pas prise en compte")
        else:
            line = line.split(delimiter)
            data[line[0]] = line[1]

    # Ferme le fichier et retourne le dictionnaire avec les valeurs récupérées
    file.close()
    return data


def write_data_file(file_path, data, delimiter=';'):
    """Ouvre ou crée un fichier au format csv récupère les donés et les retournes dans un dictionnaire

    Parameters
    ----------
    file_path: `str`
        chemin vers le fichier à ouvrir
    delimiter: `str`
        charactère délimitant le nom de lma variable et sa valeur : ";" par défaut
    data: `dict`
        Un dictionnaire contenant toutes les valeurs relevés dans le fichier.
        (Attention: à envoyer des donnés compatible avec la fonction str())
    """
    # Essaye d'ouvrir le fichier envoyer, et jette une erreur si le fichier n'exsite pas
    file = open(file_path, "w")

    # Récupère chaque clé/valeur du dictionnaire
    for key in data.keys():
        # Ecrit une ligne contenant la clé et la valeur séparé par le délimiteur
        file.write(str(key) + delimiter + str(data[key]))

    # Ferme le fichier
    file.close()
