import logging

from PyQt5.QtCore import QObject


class PageRB1:

    index = 1   # Attention dans les tableaux l'index comment à 0 donc index_tab = index - 1
    page = None
    current_button = None

    # Variable stockant la langue actuelle de l'application d'initialisation
    language = "Français"

    def __init__(self, application, page, index, current_button):
        self.index = index
        self.page = page.rootObjects()[0]
        self.current_button = current_button

        # Charge les langues disponibles pour le DMI
        try:
            file = open("../settings/language_settings/translation.settings", "r", encoding='utf-8-sig')
        # Récupère les exceptions dans le cas où le fichier de traduction n'existe pas ou est mal placé
        except (FileNotFoundError, OSError):
            logging.warning("Impossible d'ouvrir le fichier settings/language_settings/translation.settings\n\t\t" +
                            "Assurez vous que celui-ci existe. Le Français sera choisis par défaut\n")
        # Sinon lit la première ligne pour récupérer la liste des langues
        else:
            # Récupère la liste des langues (ligne 1 du fichier translation.settings)
            language_list = file.readline().rstrip('\n').split(";")

            # Met la liste des langues dans la combobox et connecte une fonction pour changer la langue
            language_combobox = self.page.findChild(QObject, "language_combo")
            language_combobox.setProperty("elements", language_list)
            language_combobox.selection_changed.connect(lambda: self.on_language_change(application, language_list))
            self.language = language_combobox.property("selection")

        # Définit la page comme validée (toutes les valeurs par défaut suffisent)
        application.is_completed[0] = True

    def on_language_change(self, application, language_list):
        """Fonction permettant de changer la langue de l'application d'initialisation.
        Permet aussi de choisir la langue pour le DMI du pupitre

        Parameters
        ----------
        application: `InitialisationWindow`
            L'instance source de l'application d'initialisation, pour les widgets
        language_list: `list`
            Liste des langues disponibles (doit correspondre exactement à celle de la combobox des langues"""
        translation_data = {}

        # Récupère le combobox ainsi que ses éléments et sa sélection
        current_index = language_list.index(self.language)
        new_index = language_list.index(self.page.findChild(QObject, "language_combo").property("selection"))

        # Ouvre le fichier et pour chaque ligne du fichier
        file = open("../settings/language_settings/translation.settings", "r", encoding='utf-8-sig')
        for line in file:
            # Si la ligne est vide la saute, sinon récupère les traductions des mots
            if line != "\n":
                translations = line.rstrip('\n').split(";")
                # Si la ligne est complète l'ajoute dans le dictionaire (clé = langue actuelle, valeur = traduction)
                if len(translations) == len(language_list):
                    translation_data[translations[current_index].upper()] = translations[new_index]
                # S'il n'y a pas autant de traductions que de langue, cela signifie que la ligne est incomplète
                else:
                    logging.debug("Certaines traductions manquantes sur la ligne suivante (langues attendus, mots) :" +
                                  "\n\t\t" + ";".join(language_list) + "\n\t\t" + line + "\n")
        file.close()

        # Appelle maintenant la fonction permettant
        application.change_language(translation_data)

        # Change la langue actuelle pour celle qui vient d'être changée
        self.language = language_list[new_index]
