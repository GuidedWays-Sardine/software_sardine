# Librairies par défaut
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
from src.misc.GUI_documentation.components.box import BoxDrawer
from src.misc.GUI_documentation.components.image import ImageDrawer
import src.misc.GUI_documentation.components.INI as INI


# Layouts généraux de l'application d'initialisation
def general_layout():
    general_layout_image = ImageDrawer("initialisation/general_layout.png", scale_factor=4)
    general_layout_image.draw([BoxDrawer((0, 0), (640, 480), ""),                       # contour de l'application
                               BoxDrawer((0, 0), (640, 15), "(640x15)"),                # bande vide supérieure
                               BoxDrawer((0, 465), (640, 15), "(640x15)"),              # bande vide inférieure
                               BoxDrawer((0, 415), (640, 50), "bb\n(640x50)"),          # zone bb
                               BoxDrawer((580, 15), (60, 400), "rb\n(60x400)"),         # zone rb
                               BoxDrawer((0, 15), (580, 400), "page_rb\n(580x400)")])   # zone page_rb
    general_layout_image.save()


def page_rb_focus_layout():
    general_layout_image = ImageDrawer("initialisation/page_rb_focus_layout.png", scale_factor=4)
    general_layout_image.draw([BoxDrawer((0, 0), (640, 480), ""),                       # contour de l'application
                               BoxDrawer((0, 0), (640, 15), "(640x15)", True),          # bande vide supérieure
                               BoxDrawer((0, 465), (640, 15), "(640x15)", True),        # bande vide inférieure
                               BoxDrawer((0, 415), (640, 50), "bb\n(640x50)", True),    # zone bb
                               BoxDrawer((580, 15), (60, 400), "rb\n(60x400)", True),   # zone rb
                               BoxDrawer((0, 15), (580, 400), "page_rb\n(580x400)")])   # zone page_rb
    general_layout_image.save()


def detailed_layout():
    detailed_layout_image = ImageDrawer("initialisation/detailed_layout.png", scale_factor=4)
    detailed_layout_image.draw([BoxDrawer((0, 0), (640, 480), ""),                      # contour de l'application
                                BoxDrawer((0, 0), (640, 15), "(640x15)"),               # bande vide supérieure
                                BoxDrawer((0, 465), (640, 15), "(640x15)"),             # bande vide inférieure
                                BoxDrawer((0, 415), (640, 50), "")] +                   # zone bb
                                [BoxDrawer((120 * i + (160 if i > 0 else 0), 415), (120, 50), f"bb{i}\n(120x50)") for i in range(4)] +                               # boutons zone bb
                                [BoxDrawer((580, 15), (60, 400), "")] +                 # zone rb
                                [BoxDrawer((580, 15+50*(i-1)), (60, 50), f"rb{i}\n(60x50)") for i in range(1, 9)] +
                                [BoxDrawer((0, 15), (580, 400), "page_rb\n(580x400)")]) # zone page_rb
    detailed_layout_image.save()


def page_rb_initialise(file_name):
    layout_image = ImageDrawer(f"initialisation/{file_name}", scale_factor=4)
    layout_image.draw([BoxDrawer((0, 0), (640, 480), ""),                      # contour de l'application
                       BoxDrawer((0, 0), (640, 15), "(640x15)", True),         # bande vide supérieure
                       BoxDrawer((0, 465), (640, 15), "(640x15)", True),       # bande vide inférieure
                       BoxDrawer((0, 415), (640, 50), "bb\n(640x50)", True),   # zone bb
                       BoxDrawer((580, 15), (60, 400), "rb\n(60x400)", True),  # zone rb
                       BoxDrawer((0, 15), (580, 400), "")])                    # zone page_rb
    return layout_image


# Layouts de chacune des pages d'initialisation
def page_rb1():
    # Initialise les éléments de base de l'image
    layout_image = page_rb_initialise("page_rb1_layout.png")

    # Rajoute chacun des composants à l'image
    layout_image.draw([INI.Combobox((55, 39), (280, 50), "Pupitre", 12, "rb1_A\n(280x50)"),
                       INI.Button((355, 39), (160, 50), "rb1_B\n(160x50)"),
                       INI.Checkbutton((55, 104), 20, "Connecté à Renard ?", 12, "rb1_C (280x20)"),
                       INI.Checkbutton((335, 104), 20, "Connecté par une caméra ?", 12, "rb1_D (150x20)"),
                       INI.Combobox((55, 169), (280, 60), "Interface pupitre", 12, "rb1_E\n(280x50)"),
                       INI.Switchbutton((55, 260), (111, 50), "Niveau de registre", 12, "rb1_F\n(111x50)"),
                       INI.Combobox((225, 260), (111, 50), "Langue", 12, "rb1_G\n(111x50)"),
                       INI.Checkbutton((55, 329), 20, "Activation du PCC (Poste de Commande Centralisé) ?", 12, "rb1_H (320x20)"),
                       INI.Checkbutton((55, 369), 20, "Affichage en direct des données ?", 12, "rb1_I (280*20)"),
                       INI.Checkbutton((335, 354), 20, "Tableau de bord ?", 12, "rb1_J (280*20)"),
                       INI.Checkbutton((335, 384), 20, "Sauvegarder les données ?", 12, "rb1_K (150*20)")])

    # Enregistre l'image
    layout_image.save()

def page_rb2_structure():
    # Définit les variables nécessaires
    input_height = 24
    gen_width = 480

    # Initialise les éléments de base de l'image
    layout_image = page_rb_initialise("page_rb2_structure.png")

    # Rajoute chacun des composants à l'image
    layout_image.draw([BoxDrawer((54, 40 + input_height), (gen_width - 54, 50 * 3), "rb2_values_A\n(426x150)", True),
                       BoxDrawer((54, 40 + input_height + 3 * 50), (gen_width - 54, 50 * 1 + 12), "rb2_values_B\n(426x62)", True),
                       BoxDrawer((54, 40 + input_height + 4 * 50 + 12), (gen_width - 54, 50 * 1 - 12), "rb2_values_C\n(426x38)", True),
                       BoxDrawer((54, 40 + input_height + 5 * 50), (gen_width - 54, 50 * 2), "rb2_values_D\n(426*100)", True),
                       INI.Stringinput((54, 40), (gen_width - 54, input_height), "Configuration du train", 12, "rb2_A (426x24)"),
                       INI.Switchbutton((gen_width, 40), (100, input_height), "", 12, "rb2_B (100x24)"),
                       INI.Combobox((gen_width, 14 + 1 * 50), (100, 50), "", 12, "rb2_C\n(100x50)"),
                       INI.Button((gen_width, 14 + 3 * 50), (100, 50), "rb2_D\n(100x50)"),
                       INI.Button((gen_width, 14 + 4 * 50), (100, 50), "rb2_E\n(100x50)"),
                       INI.Button((gen_width, 14 + 6 * 50), (100, 50), "rb2_F\n(100x50)")])
    layout_image.save()

def page_rb8():
    # Initialise les éléments de base de l'image
    layout_image = page_rb_initialise("page_rb8_layout.png")

    # Rajoute chacun des composants à l'image
    layout_image.draw([INI.Button((54, 15), (46, 40), "rb8_A\n(46x40)"),
                       INI.Button((100, 15), (380, 40), "rb8_B\n(380x40)"),
                       INI.Button((480, 15), (46, 40), "rb8_C\n(48x40)"),
                       INI.Button((54, 55), (472, 76), "rb8_D.1\n(472x76)"),
                       INI.Button((54, 131), (472, 76), "rb8_D.2\n(472x76)"),
                       INI.Button((54, 207), (472, 76), "rb8_D.3\n(472x76)"),
                       INI.Button((54, 283), (472, 76), "rb8_D.4\n(472x76)"),
                       INI.Button((434, 359), (46, 40), "rb8_E\n(46x40)"),
                       INI.Button((480, 359), (46, 40), "rb8_F\n(46x40)"),
                       INI.Checkbutton((15, 379), 20, "Eteindre les écrans qui ne sont pas utilisés ?)", 12, "rb8_G (400x20)")])
    layout_image.save()

    # Génère l'image pour l'élément de paramétrage écran
    window_parameters_layout = ImageDrawer("initialisation/window_parameters.png", 472, 76, 4)
    window_parameters_layout.draw([INI.Button((0, 0), (472, 76), ""),
                                   INI.Text((11, 11), "AHHHHHHHHHHHHHHHHHHHHHHHHHHHH", 12, "SPI_A (300x14)"),
                                   INI.Combobox((1, 45), (100, 30), "Index", 12, "SPI_C\n(100x30)"),
                                   INI.Checkbutton((346, 10), 20, "Plein écran ?    ", 12, "SPI_B (60x20)"),
                                   INI.IntegerInput((134, 45), (60, 30), "W:", "pxx", 12, "SPI_D\n(60x30)"),
                                   INI.IntegerInput((218, 45), (60, 30), "W:", "pxx", 12, "SPI_E\n(60x30)"),
                                   INI.IntegerInput((325, 45), (60, 30), "w:", "pxx", 12, "SPI_F\n(60x30)"),
                                   INI.IntegerInput((411, 45), (60, 30), "W:", "pxx", 12, "SPI_G\n(60x30)")])
    window_parameters_layout.save()

image = ImageDrawer(image_name="image.png",
                    width=640,
                    height=480,
                    scale_factor=1)
