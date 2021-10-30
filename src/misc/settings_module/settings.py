


class SettingsDictionnary(dict):
    """Classe permettant de convertir un fichier de paramètres en un dictionnaire fonctionnel"""

    def __setitem__(self, key, value):
        super(SettingsDictionnary, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(SettingsDictionnary, self).__getitem__(key.lower())
