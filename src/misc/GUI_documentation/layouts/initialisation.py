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
    general_layout_image = ImageDrawer("general_layout.png")
    general_layout_image.draw([BoxDrawer(0, 0, 640, 480, ""),                       # contour de l'application
                               BoxDrawer(0, 0, 640, 15, "(640x15)"),                # bande vide supérieure
                               BoxDrawer(0, 465, 640, 15, "(640x15)"),              # bande vide inférieure
                               BoxDrawer(0, 415, 640, 50, "bb\n(640x50)"),          # zone bb
                               BoxDrawer(580, 15, 60, 400, "rb\n(60x400)"),         # zone rb
                               BoxDrawer(0, 15, 580, 400, "page_rb\n(580x400)")])   # zone page_rb
    general_layout_image.save()


def detailed_layout():
    detailed_layout_image = ImageDrawer("detailed_layout.png")
    detailed_layout_image.draw([BoxDrawer(0, 0, 640, 480, ""),                      # contour de l'application
                                BoxDrawer(0, 0, 640, 15, "(640x15)"),               # bande vide supérieure
                                BoxDrawer(0, 465, 640, 15, "(640x15)"),             # bande vide inférieure
                                BoxDrawer(0, 415, 640, 50, "")] +                   # zone bb
                                [BoxDrawer(120*(i-1) + (160 if i > 1 else 0), 415, 120, 50, f"bb{i}\n(120x50)") for i in range(4)] +                               # boutons zone bb
                                [BoxDrawer(580, 15, 60, 400, "")] +                 # zone rb
                                [BoxDrawer(580, 15+50*(i-1), 60, 50, f"rb{i}\n(60x50)") for i in range(1, 9)] +
                                [BoxDrawer(0, 15, 580, 400, "page_rb\n(580x400)")]) # zone page_rb
    detailed_layout_image.save()


def page_rb_initialise(file_name):
    layout_image = ImageDrawer(f"initialisation/{file_name}", scale_factor=4)
    layout_image.draw([BoxDrawer(0, 0, 640, 480, ""),                      # contour de l'application
                       BoxDrawer(0, 0, 640, 15, "(640x15)", True),         # bande vide supérieure
                       BoxDrawer(0, 465, 640, 15, "(640x15)", True),       # bande vide inférieure
                       BoxDrawer(0, 415, 640, 50, "bb\n(640x50)", True),   # zone bb
                       BoxDrawer(580, 15, 60, 400, "rb\n(60x400)", True),  # zone rb
                       BoxDrawer(0, 15, 580, 400, "")])                    # zone page_rb
    return layout_image


# Layouts de chacune des pages d'initialisation
def page_rb1():
    # Initialise les éléments de base de l'image
    layout_image = page_rb_initialise("page_rb1_layout.png")

    # Rajoute chacun des composants à l'image
    layout_image.draw([INI.Combobox(50, 39, 280, 50, "Pupitre", 12, "rb1_A\n(280x50)"),
                       INI.Checkbutton(50, 104, 20, "Connecté à Renard ?", 12, "rb1_B (280x20)"),
                       INI.Checkbutton(335, 104, 20, "Connecté par une caméra ?", 12, "rb1_C (150x20)"),
                       INI.Combobox(50, 169, 280, 60, "Interface pupitre", 12, "rb1_D\n(280x50)"),
                       INI.Switchbutton(50, 260, 111, 50, "Niveau de registre", 12, "rb1_E\n(111x50)"),
                       INI.Combobox(225, 260, 111, 50, "Langue", 12, "rb1_F\n(111x50)"),
                       INI.Checkbutton(50, 329, 20, "Activation du PCC (Poste de Commande Centralisé) ?", 12, "rb1_G (320x20)"),
                       INI.Checkbutton(50, 369, 20, "Affichage en direct des données ?", 12, "rb1_H (280*20)"),
                       INI.Checkbutton(335, 354, 20, "Tableau de bord ?", 12, "rb1_I (280*20)"),
                       INI.Checkbutton(335, 384, 20, "Sauvegarder les données ?", 12, "rb1_J (150*20)")])

    # Enregistre l'image
    layout_image.save()


def page_rb8():
    # Initialise les éléments de base de l'image
    layout_image = page_rb_initialise("page_rb8_layout.png")

    # Rajoute chacun des composants à l'image
    layout_image.draw([INI.Button(54, 15, 46, 40, "rb8_A\n(46x40)"),
                       INI.Button(100, 15, 380, 40, "rb8_B\n(380x40)"),
                       INI.Button(480, 15, 46, 40, "rb8_C\n(48x40)"),
                       INI.Button(54, 55, 472, 76, "rb8_D.1\n(472x76)"),
                       INI.Button(54, 131, 472, 76, "rb8_D.2\n(472x76)"),
                       INI.Button(54, 207, 472, 76, "rb8_D.3\n(472x76)"),
                       INI.Button(54, 283, 472, 76, "rb8_D.4\n(472x76)"),
                       INI.Button(434, 359, 46, 40, "rb8_E\n(46x40)"),
                       INI.Button(480, 359, 46, 40, "rb8_F\n(46x40)"),
                       INI.Checkbutton(15, 379, 20, "Eteindre les écrans qui ne sont pas utilisés ?)", 12, "rb8_G (400x20)")])
    layout_image.save()

    # Génère l'image pour l'élément de paramétrage écran
    window_parameters_layout = ImageDrawer("initialisation/window_parameters.png", 472, 76, 4)
    window_parameters_layout.draw([INI.Button(0, 0, 472, 76, ""),
                                   INI.Text(14, 14, "AHHHHHHHHHHHHHHHHHHHHHHHHHHHH", 12, "SPI_A (300x14)"),
                                   INI.Combobox(1, 45, 100, 30, "Index", 12, "SPI_C\n(100x30)"),
                                   INI.Checkbutton(346, 10, 20, "Plein écran ?    ", 12, "SPI_B (60x20)"),
                                   INI.IntegerInput(134, 45, 60, 30, "W:", "pxx", 12, "SPI_D\n(60x30)"),
                                   INI.IntegerInput(218, 45, 60, 30, "W:", "pxx", 12, "SPI_E\n(60x30)"),
                                   INI.IntegerInput(325, 45, 60, 30, "w:", "pxx", 12, "SPI_F\n(60x30)"),
                                   INI.IntegerInput(411, 45, 60, 30, "W:", "pxx", 12, "SPI_G\n(60x30)")])
    window_parameters_layout.save()
