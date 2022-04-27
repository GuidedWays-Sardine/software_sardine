# Libraires par défaut
import sys
import os
from enum import Enum


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
from src.misc.units_converter.dimension import Dimension


# Dictionaire contenant toutes les unités SI de base
# factor ; offset tel que : [Unit] = [SI] * factor + offset     ; google : [Unit] to [SI]
Units = { # Unités SI
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
         "feet": Dimension("feet", factor=1/3.281, length=1),
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
         "W": Dimension("W", factor=1, mass=1, length=2, time=-3),                    # Watt
         "kW": Dimension("kW", factor=10**3, mass=1, length=2, time=-3),
         "MW": Dimension("MW", factor=10**6, mass=1, length=2, time=-3),
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
         "gal": Dimension("gal", factor=1/264, length=3)
}


# Convertit toutes les unités en un dictionaire {string: unit} pour la conversion de la fonction get_unit
# UNIT_DICT = {str(u).lower(): u() for u in Unit}


def get_unit(unit_string):
    if not unit_string:
        Dimension(name="1", offset=0, factor=1)

    a = __divide_unit_string(unit_string)[0]

    return __string_to_unit(a)


def __divide_unit_string(unit_string):
    """divise le texte d'une unité à chaque fois que l'un des charactère suivant est rencontré : (* ; ^ ; /).
    Si une parenthèse fermée ou la fin du texte est trouvée, retourne.
    Si une parenthèse ouverte est trouvée, rappelle la fonction récursivement

    Parameters
    ----------
    unit_string: `string`
        L'unité à traiter

    Returns
    -------
    unit_list: `list[string, list]`
        L'unité divisé selon ses unités, opérateur etc...
    """
    index = 0
    current = ""
    unit = []

    # Tant que l'on n'est pas à la fin du string
    while index < len(unit_string) and unit_string[index] != ")":
        # Cas où une parenthèse est ouverte : appelle la fonction récursivement et appelle le résultat
        if unit_string[index] == "(":
            index += 1
            mid_unit, mid_index = __divide_unit_string(unit_string[index:])
            index += mid_index

            if index == len(unit_string):
                raise ValueError("Pas suffisament de fermetures de parenthèses")
            unit.append(mid_unit)

            index += 1
            current = ""
        elif unit_string[index] in ("*", "/", "^"):
            if index == len(unit_string) - 1:
                raise ValueError("Une unité ne peut pas se finir par un / * ^")
            else:
                if current:
                    unit.append(current)
                unit.append(unit_string[index])
                current = ""
                index += 1
        else:
            current += unit_string[index]
            index += 1

    if current:
        unit.append(current)

    return unit, index


def __string_to_unit(unit_list):
    if len(unit_list) == 0:
        return Dimension("1", factor=1, offset=1)


    index = 0
    if isinstance(unit_list[0], list):
        # Récupère l'unité dans les parenthèses
        unit = __string_to_unit(unit_list[0])

        # Ajoute la puissance si une puissance spécifique est envoyée
        if len(unit_list) > 3 and unit_list[1] == "^" and unit_list[2].isnumeric():
            unit = unit ** float(unit_list[2])
            index += 2
    elif isinstance(unit_list[0], str) and unit_list[0] in Units:
        # Si c'est juste un string, récupère l'unité
        unit = Units[unit_list[0]]

        # Ajoute la puissance si une puissance spécifique est envoyée
        if len(unit_list) > 3 and unit_list[1] == "^" and unit_list[2].isnumeric():
            unit = unit ** float(unit_list[2])
            index += 2
    else:
        raise ValueError(f"L'unité \"{unit_list[0]}\" n'existe pas dans la liste d'unités (Units).")
    index += 1

    while index < len(unit_list):
        if index < len(unit_list) + 1 and unit_list[index] == "^":
            raise ValueError("Impossible d'avoir 2 puissances à la sute")
        elif index < len(unit_list) + 1 and unit_list[index] in ("/", "*"):

            if isinstance(unit_list[index + 1], str):
                new_unit = Units[unit_list[index + 1]]
            elif isinstance(unit_list[index + 1], list):
                new_unit = __string_to_unit(unit_list[index + 1])
            else:
                raise TypeError(f"unité de type : \"{type(unit_list[index + 1])}\"")

            if index + 3 < len(unit_list) and unit_list[index + 2] == "^" and unit_list[index + 3].isnumeric():
                new_unit = new_unit ** float(unit_list[index + 3])

            if unit_list[index] == "/":
                unit = unit / new_unit
            elif unit_list[index] == "*":
                unit = unit * new_unit

            index += 2 + 2 * (index + 3 < len(unit_list) and unit_list[index + 2] == "^")
        elif index >= len(unit_list) + 1:
            raise ValueError(f"L'unité ne peut pas se finir par un opérateur {unit_list}")
        else:
            raise ValueError(f"Operator {unit_list[index]} inconnu ({unit_list[index - 1]}{unit_list[index]}{unit_list[index + 1]})")

    return unit

def convert_factor(base_unit, new_unit):
    if base_unit == new_unit:
        return (new_unit / base_unit).factor
    else:
        raise ValueError(f"Les dimensions envoyées ne sont pas bonnes\n\t{base_unit}\n\t{new_unit}")

def convert_offset(base_unit, new_unit):
    if base_unit == new_unit:
        return (new_unit / base_unit).offset
    else:
        raise ValueError(f"Les dimensions envoyées ne sont pas bonnes\n\t{base_unit}\n\t{new_unit}")


if __name__ == "__main__":
    print(get_unit("g")/get_unit("kg"))
    print(get_unit("kN/t/(km/h)^2"))
    print(get_unit("N/kg/(m/s)^2"))
    print(12 / get_unit("kN/t/(km/h)^2") * get_unit("N/kg/(m/s)^2"))

