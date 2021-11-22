# Librairies par défaut
import sys
import os
import time

# Librairies de traitement de données
import pandas as pd
import numpy as np

# librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log.log as log


class Spline:
    # Informations générales sur la spline
    electrification = ""
    line_name = ""
    line_code = 0

    # Toutes les bases de données avec les informations nécessaires
    curves = None
    slopes = None
    max_speed = None

    def __init__(self):
        print("e")