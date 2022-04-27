# Libraires par défaut
import sys
import os
import time


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
import src.misc.units_converter as uc

if __name__ == "__main__":
    log.initialise(save=False, terminal=False)

    # Essaye différentes conversions dont certaines avec une erreur
    for unit in ["t/m", "kN/t/(km/h)^2", "N/kg/(m/s)^2", "N/kg/(m/s", "kg^2.e", "kg/(mxs)^2,0", "AHHHHH"]:
        try:
            print(uc.get_unit(unit))
        except Exception as error:
            log.error("Erreur de conversion", exception=error)

    # Essaye de charger la même unité gourmande pleins de fois pour voir l'impact sur les performances
    initial_time = time.perf_counter()
    for _ in range(1000000):
        uc.get_unit("kN/t/(km/h*(floz*gal)^3.0)^2")
    print((time.perf_counter() - initial_time) / 1000000)

    print(uc.get_unit("C") / uc.get_unit("F"))
    print(uc.get_conversion_list(("K", "C", "F")))
