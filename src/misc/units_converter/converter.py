# Libraires par défaut
import sys
import os
import re


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log
from src.misc.units_converter.dimension import Dimension
from src.misc.units_converter.units import Units


def __get_unit(unit_name):
    """Retourne la nouvelle unité générée à partir des unités par défaut

    Parameters
    ----------
    unit_name: `str`
        Unité comme chaine de charactère.

    Returns
    -------
    unit: `Dimension`
        Unité convertit à partir du nom de l'unité envoyé.

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
    __unit = unit_name
    # Remplace les charactères non pris en compte mais lisible par des charactères normalisés
    for pattern in (("x", "*"), (",", "."), ("²", "^2"), ("[", "("), ("]", ")"), ("{", "("), ("}", ")")):
        __unit = __unit.replace(pattern[0], pattern[1])

    # Si des charactères ont été modifiés laisse un message de debug
    if __unit != unit_name:
        log.debug(f"Utilisation de charactères déconseillés (\"{unit_name}\" -> \"{__unit}\").")

    # Si des characètres inconnus sont restants, jette une erreur
    if not re.match(r"^[a-zA-Z0-9.*/()^]*$", unit_name):
        raise ValueError(f"Certains charactères de l'unité \"{__unit}\" ne sont pas supportés. " +
                         f"Charactères supportés : a-z ; A-Z ; 0-9 ; . ; * ; / ; ^ ; ( ; )")

    # Convertir la chaine de charactère de l'unité en liste d'opérateurs et de valeurs
    try:
        __unit_list = __divide_unit_string(__unit)
    except RecursionError as error:
        raise RecursionError(f"Certaines parenthèses ne sont pas correctement fermées dans \"{__unit}\".") from error
    except ValueError as error:
        raise ValueError(f"Une unité ne peut pas se finir par un opérateur (* ; / ; ^) \"{__unit}\".") from error

    try:
        return __convert_unit_list(__unit_list[0])
    except ValueError as error:
        if not error.args:
            raise ValueError(f"Suite d'opérateurs incohérents. Deux puissances ne peuvent pas se succéder ({__unit}).") \
                from error
        else:
            raise ValueError(f"Suite d'opérateurs incohérents. {error.args[0]} trouvé au lieu de * ou / ({__unit}).") \
                from error
    except KeyError as error:
        raise KeyError(f"La sous-unité \"{error.args[0]}\" de l'unité \"{__unit}\" n'a pas été définie.") from error
    except TypeError as error:
        raise TypeError(f"Puissance \"{error.args[0]}\" incohérente dans l'unité \"{__unit}\".") from error


def __divide_unit_string(unit_string):
    """Dvise le texte d'une unité à chaque fois que l'un des charactère suivant est rencontré : (* ; ^ ; /).
    Si une parenthèse fermée ou la fin du texte est trouvée, retourne.
    Si une parenthèse ouverte est trouvée, rappelle la fonction récursivement.

    Parameters
    ----------
    unit_string: `string`
        Unité à traiter.

    Returns
    -------
    unit_list: `list[string, list]`
        Unité divisé selon ses unités et opérateur ;
    index: `int`
        Index auquel la récursion s'est arrétée (en fin de chaine de charactère ou sur une fermeture de parenthèse).

    Raises
    ------
    RecursionError:
        Jetée si l'unité n'a pas suffisament de parenthèses fermées ;
    ValueError:
        Jetée si l'unité envoyée se termine par un opérateur (* ; / ; ^) et non par une unité ou une puissance.
    """
    index = 0
    current = ""
    unit = []

    # Tant que l'on n'est pas à la fin du string
    while index < len(unit_string) and unit_string[index] != ")":
        # Cas où une parenthèse est ouverte : appelle la fonction récursivement et appelle le résultat
        if unit_string[index] == "(":
            # Appelle la fonction récursivement, récupère l'index de fin de parenthèse et les unités dans celles-ci
            mid_unit, mid_index = __divide_unit_string(unit_string[index+1:])
            unit.append(mid_unit)

            # Si l'index de retour ne pointe pas sur une parenthèse fermée, jette une erreur de récursion
            if index == len(unit_string):
                raise RecursionError()

            # Passe l'index après la fermeture de parenthèse, réinitialise l'élément courrant et continue
            index += mid_index + 2
            current = ""
        # Cas où l'on a un opérateur
        elif unit_string[index] in ("*", "/", "^"):
            # S'assure que ce n'est pas la fin du string (une unité ne peut pas se finir par un opérateur)
            if index == len(unit_string) - 1:
                raise ValueError()

            # Sinon ajoute l'unité précédente, l'opérateur actuel et passe à la suite
            if current:
                unit.append(current)
            unit.append(unit_string[index])
            current = ""
            index += 1
        # Cas autre, la lettre appartient à une unité ou une puissance, l"ajouté à la fin de current et continue
        else:
            current += unit_string[index]
            index += 1

    # Ajoute la dernière unité et retourne l'unité et l'index actuel
    if current:
        unit.append(current)

    return unit, index


def __convert_unit_list(unit_list):
    """Retourne l'unité à partir d'une liste d'unités, de puissances et d'opérateurs

    Parameters
    ----------
    unit_list: `list[str, list]`
        Liste contenant la suite d'unités et d'opérateurs.

    Returns
    -------
    unit: `Dimension`
        Unité convertit.

    Raises
    ------
    KeyError:
        Jetée si l'une des sous-unité n'a pas été définie ;
    TypeError
    """
    # Initialise la première unité, utilisée comme base pour les opérations qui suivent
    index = 0
    # Différencie l'unité complexe (entre parenthèses) récupéré par récursion et une unité simple
    if isinstance(unit_list[0], list):
        unit = __convert_unit_list(unit_list[0])
    else:
        unit = Units[unit_list[0]]  # Jette KeyError si la clé est inexistante

    # Ajoute la puissance si une puissance spécifique est envoyée
    if len(unit_list) > 3 and unit_list[1] == "^" and unit_list[2].isnumeric():
        unit = unit ** float(unit_list[2])
        index += 2
    index += 1

    # Tant que l'on n'est pas à la fin de l'unité
    while index < len(unit_list):
        # Si une puissance est détecté, cela signifie que l'unité contient deux puissances à la suite
        if index < len(unit_list) + 1 and unit_list[index] == "^":
            raise ValueError()
        # Si un opérateur est trouvé, l'applique sur les deux unités
        elif index < len(unit_list) + 1 and unit_list[index] in ("/", "*"):
            # Différencie l'unité complexe (entre parenthèses) récupéré par récursion et une unité simple
            if isinstance(unit_list[index + 1], list):
                new_unit = __convert_unit_list(unit_list[index + 1])
            else:
                new_unit = Units[unit_list[index + 1]]  # Jette KeyError si la clé est inexistante

            # Ajoute la puissance si une puissance spécifique est envoyée
            if index + 3 < len(unit_list) and unit_list[index + 2] == "^":
                if re.match(r"^-?\d+(?:\.?\d?)$", unit_list[index + 3]):
                    new_unit = new_unit ** float(unit_list[index + 3])
                else:
                    raise TypeError(unit_list[index + 3])

            # Applique l'opérateur détecté
            if unit_list[index] == "/":
                unit = unit / new_unit
            elif unit_list[index] == "*":
                unit = unit * new_unit

            index += 2 + 2 * (index + 3 < len(unit_list) and unit_list[index + 2] == "^")
        # Sinon, une incohérence a été trouvée
        else:
            raise ValueError(unit_list[index])

    # Retourne l'unité convertit
    return unit
