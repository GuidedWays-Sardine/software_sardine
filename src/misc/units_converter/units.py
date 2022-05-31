# Libraires par défaut
import sys
import os
import functools


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
from src.misc.units_converter.dimension import Dimension


# Dictionnaire contenant toutes les unités SI de base
# factor ; offset tel que : [Unit] = [SI] * factor + offset     ; google : [Unit] to [SI]
Units = {   # Unités sans dimensions
         "":    Dimension("1",   factor=1),                                           # Sans dimensions
         "1":   Dimension("1",   factor=1),
         "%":   Dimension("%",   factor=10**-2),
         "‰":   Dimension("‰",   factor=10**-3),
            # Unités SI
         "m":   Dimension("m",   factor=1, length=1),
         "kg":  Dimension("kg",  factor=1, mass=1),
         "s":   Dimension("s",   factor=1, time=1),
         "A":   Dimension("A",   factor=1, current=1),
         "K":   Dimension("K",   factor=1, temperature=1),
         "cd":  Dimension("cd",  factor=1, light_intensity=1),
         "mol": Dimension("mol", factor=1, matter_quantity=1),
            # Unités dérivé
         "km": Dimension("km", factor=10**3, length=1),                               # Length
         "mm": Dimension("mm", factor=10**-3, length=1),
         "inch": Dimension("inch", factor=1/39.37, length=1),
         "\"": Dimension("inch", factor=1/39.37, length=1),
         "feet": Dimension("feet", factor=1/3.281, length=1),
         "foot": Dimension("feet", factor=1/3.281, length=1),
         "\'": Dimension("feet", factor=1/3.281, length=1),
         "yard": Dimension("yard", factor=1/1.094, length=1),
         "mile": Dimension("mile", factor=1609.34, length=1),
         "t": Dimension("t", factor=10**3, mass=1),                                   # Mass
         "Mg": Dimension("Mg", factor=10**3, mass=1),
         "mg": Dimension("mg", factor=10**-6, mass=1),
         "g": Dimension("g", factor=10**-3, mass=1),
         "lb": Dimension("lb", factor=1/2.205, mass=1),
         "oz": Dimension("oz", factor=1/35.274, mass=1),
         "min": Dimension("min", factor=60, time=1),                                  # Time
         "h": Dimension("h", factor=60*60, time=1),
         "kA": Dimension("kA", factor=10**3, current=1),                              # Current
         "mA": Dimension("mA", factor=10**-3, current=1),
         "C": Dimension("C", factor=1, offset=273.15, temperature=1),                 # Temperature
         "F": Dimension("F", factor=5/9, offset=255.372, temperature=1),
            # Unités complexes
         "W": Dimension("W", factor=1, mass=1, length=2, time=-3),                    # Watt/Horse Power
         "kW": Dimension("kW", factor=10**3, mass=1, length=2, time=-3),
         "MW": Dimension("MW", factor=10**6, mass=1, length=2, time=-3),
         "hp": Dimension("hp", factor=745.7, mass=1, length=2, time=-3),
         "N": Dimension("N", factor=1, mass=1, length=1, time=-2),                    # Newton
         "kN": Dimension("kN", factor=10**3, mass=1, length=1, time=-2),
         "MN": Dimension("MN", factor=10**6, mass=1, length=1, time=-2),
         "J": Dimension("J", factor=1, mass=1, length=2, time=-2),                    # Joule
         "kJ": Dimension("kJ", factor=10**3, mass=1, length=2, time=-2),
         "MJ": Dimension("MJ", factor=10**6, mass=1, length=2, time=-2),
         "V": Dimension("V", factor=1, mass=1, length=2, time=-3, current=-1),        # Volt
         "kV": Dimension("kV", factor=10**3, mass=1, length=2, time=-3, current=-1),
         "Ohm": Dimension("Ohm", factor=1, mass=1, length=2, time=-3, current=-2),    # Ohm
         "kOhm": Dimension("kOhm", factor=10**3, mass=1, length=2, time=-3, current=-2),
         "MOhm": Dimension("MOhm", factor=10**6, mass=1, length=2, time=-3, current=-2),
         "l": Dimension("l", factor=10**-3, length=3),                                # Volume
         "floz": Dimension("floz", factor=1/33814, length=3),
         "gal": Dimension("gal", factor=1/264, length=3),
         "Pa": Dimension("Pa", factor=1, mass=1, length=-1, time=-2),                 # Pascal/bar
         "hPa": Dimension("hPa", factor=10, mass=1, length=-1, time=-2),
         "bar": Dimension("bar", factor=10**5, mass=1, length=-1, time=-2)
}


@functools.cache
def add_base_unit(name, dimension) -> None:
    """Ajoute une unité dans la liste des unités par défaut.

    Parameters
    ----------
    name: `str`
        Nom raccourcis de l'unité (comme indiqué sur internet) ;
    dimension: `Dimension`
        Dimension relié à cette unité.
    """
    # Si l'unité n'est pas déjà dans la liste des unités, l'ajoute, sinon laisse un message de debug
    if name not in Units:
        Units[name] = dimension
    else:
        log.debug(f"Unité \"{name}\" déjà présente : {dimension} -> {Units[name]}")


@functools.cache
def get_unit(name):
    """Récupère l'unité correspondant au nom envoyé.

    Parameters
    ----------
    name: `str`
        Nom simplifié de l'unité.

    Returns
    -------
    unit: `Dimension`
        Unité générée à partir du nom envoyé.

    Raises
    ------
    ValueError:
        Jetée si la patterne envoyé contient des charactères non pris en compte ;
    RecursionError:
        Jetée si l'unité n'a pas suffisament de parenthèses fermées ;
    ValueError:
        Jetée si l'unité est illogique (fin d'unité sur un opérateur, enchainement de puissances) ;
    KeyError:
        Jetée si l'une des sous-unité n'a pas été définie ;
    TypeError:
        Jetée si l'une des puissance n'est pas convertible en nombre
    """
    # Si l'unité existe de base dans la liste des unités, la retourne sinon la génère et la retourne
    if name in Units:
        return Units[name]
    else:
        from src.misc.units_converter.converter import __get_unit
        return __get_unit(name)


def get_conversion_list(unit_list):
    """Récupère pour chacune des unités, leur nom, facteur et décalage.

    Parameters
    ----------
    unit_list: `list[str] | tuple[str] | str`
        Liste des unités de conversion (doivent avoir la même dimension).

    Returns
    -------
    conversion_list: `list[list[str, float, float]]`
        Liste des conversions d'unités.
    """
    conversion_list = []

    # Dans le cas où la liste d'unité n'est ni un list ni un tuple (donc un str), le transforme en tuple
    if isinstance(unit_list, str):
        unit_list = (unit_list,)

    # Pour chacune des unités de la liste
    for unit_name in unit_list:
        # Récupère l'unité et laisse un message de warning si une erreur a été détectée
        try:
            unit = get_unit(unit_name)
        except Exception as error:
            log.warning(f"Erreur avec l'unité \"{unit_name}\" lors de la création d'une liste de conversion",
                        exception=error)
        else:
            # Si c'est la première unité ou que les dimensions sont cohérentes avec les autres, l'ajoute
            if conversion_list and unit == get_unit(conversion_list[0][0]) or not conversion_list:
                conversion_list.append([unit_name, *unit.si_to_unit()])
            else:
                log.warning(f"Les dimensions d'une des unités de la liste de conversion n'est pas cohérente.\n\t" +
                            f"{unit} au lieu de {conversion_list[0]}")

    # Retourne la liste de conversion
    return conversion_list
