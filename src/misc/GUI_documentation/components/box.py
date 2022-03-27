# Librairies par défaut
from PIL import ImageFont
from .. import colors


class BoxDrawer:

    box_corners = []
    text = ""
    fill = False

    def __init__(self, x, y, w, h, draw_text="", fill=False):
        """Permet d'initialiser la boite à dessiner

        Parameters
        ----------
        x: `int`
            coordonnée x de la boite
        y: `int`
            coordonnée y de la boite
        w: `int`
            largeur de la boite
        h: `ìnt`
            hauteur de la boite
        draw_text : `string`
            texte à afficher au milieu de la boite (texte vide par défaut)
        fill : `bool`
            la boite doit-elle être remplie en bleu clair (Non par défaut)
        """
        self.box_corners = [x, y, x + w - 1, y + h - 1]
        self.text = draw_text
        self.fill = fill

    def draw(self, drawing, scale_factor=1):
        """Permet de dessiner la boite

        drawing : `ImageDrawing`
            Le dessin sur lequel il faut ajouter la forme
        scale_factor: `int`
            Savoir de combien de fois la qualité par défaut doit être augmentée (par défaut 1)
        """
        # Mets à jour les dimensions de la boite pour l'enregistrer à la bonne taille
        self.box_corners = [self.box_corners[0] * scale_factor,
                            self.box_corners[1] * scale_factor,
                            self.box_corners[2] * scale_factor + scale_factor - 1,
                            self.box_corners[3] * scale_factor + scale_factor - 1]

        # Dessine le rectangle
        drawing.rectangle(self.box_corners,
                          width=1 * scale_factor,
                          outline=colors.OUTLINE_COLOR,
                          fill=colors.BACKGROUND_LIGHT_COLOR if self.fill else colors.BACKGROUND_DARK_COLOR)

        # Dessine le texte
        w, h = drawing.textsize(self.text)
        drawing.multiline_text((self.box_corners[0] + (self.box_corners[2]-self.box_corners[0]-(w+1) * scale_factor)/2,
                                self.box_corners[1] + (self.box_corners[3]-self.box_corners[1]-(h+1) * scale_factor)/2),
                               self.text,
                               align="center",
                               font=ImageFont.truetype("arial.ttf", 12 * scale_factor),
                               fill=colors.TEXT_COLOR)
