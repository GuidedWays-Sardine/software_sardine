# Librairies pour créer les images
from PIL import Image, ImageFont, ImageDraw


# Librairies SARDINE
from . import box


class Button(box.BoxDrawer):
    """Classe pour dessier un composant INI_button"""
    pass


class Text(box.BoxDrawer):
    """Classe pour dessiner un composant INI_text"""
    def __init__(self, position, text, text_size=12, draw_text="", fill=False):
        """Permet d'initialiser la boite à dessiner

        Parameters
        ----------
        position: `tuple | list`
            position du texte
        text: `str`
            texte affiché sur l'application
        text_size: `int`
            taille du texte
        draw_text : `string`
            texte à afficher au milieu de la boite (texte vide par défaut)
        fill : `bool`
            la boite doit-elle être remplie en bleu clair (Non par défaut)
        """
        # Récupère en fonction du texte et de sa taille, la taille du texte
        drawing = ImageDraw.Draw(Image.new("RGB", (640, 480), (0, 0, 0)))
        text_w = drawing.textsize(text, font=ImageFont.truetype("arial.ttf", text_size))[0] if text else 0

        # Appelle le constructeur de la classe mêre poure dessiner la boite
        super(Text, self).__init__((position[0], position[1] - 2), (text_w, text_size + 4), draw_text, fill)

    def draw(self, drawing, scale_factor=1):
        """Permet de dessiner la boite

        drawing : `ImageDrawing`
            Le dessin sur lequel il faut ajouter la forme
        scale_factor: `int`
            Savoir de combien de fois la qualité par défaut doit être augmentée (par défaut 1)
        """
        # S'assure que la boite contient bien du texte, si c'est le cas dessine la boite
        if self.box_corners[0] < self.box_corners[2]:
            super().draw(drawing, scale_factor)


class Checkbutton:
    """Classe pour dessiner un composant INI_checkbutton"""

    box_box = None
    title_box = None

    def __init__(self, position, box_length, title="", text_size=12, draw_text="", fill=False):
        """Permet d'initialiser les boites nécessaires pour dessiner le composant

        Parameters
        ----------
        position: `tuple | list`
            position du combobox
        box_length: `int`
            largeur et hauteur de la boite du combobox
        title: `str`
            titre du composant (texte affiché en haut à gauche)
        text_size: `int`
            taille du titre du composant
        draw_text : `string`
            texte à afficher au milieu de la boite (texte vide par défaut)
        fill : `bool`
            la boite doit-elle être remplie en bleu clair (Non par défaut)
        """
        # Initialise chacun des sous-boites du composant
        self.box_box = box.BoxDrawer(position, (box_length, box_length), "", fill)
        self.title_box = Text((position[0] + box_length + text_size, int(position[1] + (box_length - text_size)/2)),
                              title, text_size, draw_text, fill)

    def draw(self, drawing, scale_factor=1):
        """Permet de dessiner la boite

        drawing : `ImageDrawing`
            Le dessin sur lequel il faut ajouter la forme
        scale_factor: `int`
            Savoir de combien de fois la qualité par défaut doit être augmentée (par défaut 1)
        """
        self.title_box.draw(drawing, scale_factor)
        self.box_box.draw(drawing, scale_factor)


class IntegerInput:
    """Classe pour dessiner un composant INI_integerinput"""

    box_box = None
    title_box = None
    unit_box = None

    def __init__(self, position, size, title="", unit="", text_size=12, draw_text="", fill=False):
        """Permet d'initialiser les boites nécessaires pour dessiner le composant

        Parameters
        ----------
        position: `tuple | list`
            position du composant
        size: `tuple | list`
            dimensions du composant
        title: `str`
            titre du composant (texte affiché en haut à gauche)
        unit: `str`
            unités du composant (texte affiché en bas à droite)
        text_size: `int`
            taille du titre du composant
        draw_text : `string`
            texte à afficher au milieu de la boite (texte vide par défaut)
        fill : `bool`
            la boite doit-elle être remplie en bleu clair (Non par défaut)
        """
        # Initialise les différentes boites nécessaires pour dessiner le composant
        self.box_box = box.BoxDrawer(position, size, draw_text, fill)
        self.title_box = Text((position[0], position[1] - text_size - 1), title, text_size, "", fill)
        self.unit_box = Text((position[0] + size[0] - 1, position[1] + size[1] - int(text_size/3) - 2),
                             unit, int(text_size/3), "", fill)

    def draw(self, drawing, scale_factor=1):
        """Permet de dessiner la boite

        drawing : `ImageDrawing`
            Le dessin sur lequel il faut ajouter la forme
        scale_factor: `int`
            Savoir de combien de fois la qualité par défaut doit être augmentée (par défaut 1)
        """
        self.box_box.draw(drawing, scale_factor)
        self.title_box.draw(drawing, scale_factor)
        self.unit_box.draw(drawing, scale_factor)


class Floatinput(IntegerInput):
    """Classe pour dessiner un composant INI_floatinput"""
    pass


class Stringinput(IntegerInput):
    """Classe pour dessiner un composant INI_stringinput"""
    def __init__(self, position, size, title, text_size, draw_text, fill=False):
        """Permet d'initialiser les boites nécessaires pour dessiner le composant

        Parameters
        ----------
        position: `tuple | list`
            position du composant
        size: `tuple | list`
            dimensions du composant
        title: `str`
            titre du composant (texte affiché en haut à gauche)
        text_size: `int`
            taille du titre du composant
        draw_text : `string`
            texte à afficher au milieu de la boite (texte vide par défaut)
        fill : `bool`
            la boite doit-elle être remplie en bleu clair (Non par défaut)
        """
        # Appelle l'initialisation en envoyant une unité vide
        super(Stringinput, self).__init__(position, size, title, "", text_size, draw_text, fill)


class Combobox(Stringinput):
    """Classe permettant de dessiner un composant INI_combobox"""
    pass


class Switchbutton(Stringinput):
    """Classe permettant de dessiner un composant INI_combobox"""
    pass


class TrainPreview(box.BoxDrawer):
    """Classe permettant de dessiner un INI_trainpreview"""
    pass
