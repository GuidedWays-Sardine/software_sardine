# Librairies par défaut python
import sys
import os


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

import src.train.train_database.System.Traction.Boggie.boggie as boggie

class Traction:
    # Define attributes

   boggie=boggie
   def __init__(self):
       self.boggie=boggie.Boggie()









