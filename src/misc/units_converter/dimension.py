# Librairies par défaut
import sys
import os
from math import isclose
import re
import functools


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary as sd


class Dimension:
    """Classe permettant de définir chaque unité, dépendament de ses dimensions et des units SI"""

    # Nom de l'unité (pour affichage)
    __name = ""

    # Dimensions du système international (en SettingsDictionary pour les rendre insensible au majuscules et minuscules)
    __dimensions = sd.SettingsDictionary({"length": 0.0,  # meter (m)     [L]
                                          "mass": 0.0,  # kilogram (kg) [M]
                                          "time": 0.0,  # second (s)    [T]
                                          "current": 0.0,  # Amps (A)      [I]
                                          "temperature": 0.0,  # Kelvin (K)    [Θ]
                                          "light_intensity": 0.0,  # candela (cd)  [N]
                                          "matter_quantity": 0.0})  # mol (mol)     [J]

    # Facteur (comparé au système international)
    __factor = 0

    # décallage (comparé au système international)
    __offset = 0

    @functools.cache
    def __init__(self, name, factor=1.0, offset=0.0,
                 length=0, mass=0, time=0, current=0, temperature=0, light_intensity=0, matter_quantity=0):
        """Initialise une unité grâce à son facteur et décallage ainsi que ses dimensions

        Parameters
        ----------
        name: `str`
            Nom réduit de l'unité ;
        factor: `float | int`
            Facteur entre l'unité SI et cette unité (Unit = SI * factor + offset) ;
        offset: `float | int`
            Décallage en 0 entre l'unité SI et cette unité (Unit = SI * factor + offset) ;
        length: `float | int`
            Dimension pour l'unité de longueur (SI : m) ;
        mass: `float | int`
            Dimension pour l'unité de la masse (SI : kg) ;
        time: `float | int`
            Dimension pour l'unité de temps (SI : s) ;
        current: `float | int`
            Dimension pour l'unité de courrant (SI : A) ;
        temperature: `float | int`
            Dimension pour l'unité de température (SI : K) ;
        light_intensity: `float | int`
            Dimension pour l'unité d'intensité lumineuse (SI : cd) ;
        length: `float | int`
            Dimension pour l'unité de quantité de matière (SI : mol).

        Raises
        ------
        ValueError:
            Jetée si les dimensions de l'unité envoyé sont invalides (K^2, ...) ;
        ZeroDivisionError:
            Jetée si le facteur envoyé vaut 0 (impossible).
        """
        # S'assure que le facteur ne vaut pas 0 (sinon risque de division par défaut
        if factor == 0:
            raise ZeroDivisionError("Le facteur entre une unité et son équivalent ne peut pas valoir 0.")

        # S'assure que la température n'a pas une dimension différent de 1, 0, -1
        if temperature not in (-1, 0, 1):
            raise ValueError("La dimensions de température ne peut pas être différente de -1 ; 0 ; 1. " +
                             f"[Θ1] = {self.__dimensions['temperature']} ({self.__name})")

        # Sinon initialise chacun des membres
        self.__name = name.replace("x", "*").replace("**", "^").replace("²", "^2").replace(",", ".")
        self.__factor = factor
        self.__offset = offset
        self.__dimensions = {"length": length,
                             "mass": mass,
                             "time": time,
                             "current": current,
                             "temperature": temperature,
                             "light_intensity": light_intensity,
                             "matter_quantity": matter_quantity}

    def __hash__(self):
        """Retourne la référence vers la dimension."""
        return id(self)

    def __eq__(self, other):
        """Retourne si les dimensions des deux unités sont égales. Ne prend pas en compte le ratio et l'offset.

        Returns
        -------
        same_dimension: `bool`
            Retourne vrai si la dimension des deux unités est identique
        """
        return isinstance(other, Dimension) and \
            all(isclose(self.__dimensions[key], other.__dimensions[key]) for key in list(self.__dimensions.keys()))

    def __rmul__(self, other):
        """Opérateur de multiplication : * (inversé)

        Parameters
        ----------
        other: `int | float`
            Ratio par lequel cette dimension sera multipliée.

        Returns
        -------
        multiplication: `float`
            Valeur qui découle de la conversion depuis les unités SI

        Raises
        ------
        ValueError
            Jetée si la multiplication des deux unités donnent une unité invalide (K^2, ...) ;
        TypeError
            Jetée si "other" n'est ni une Dimension, ni un float, ni un int.
        """
        return self * other

    def __mul__(self, other):
        """Opérateur de multiplication : *

        Parameters
        ----------
        other: `Dimension | int | float`
            Unité ou ratio par lequel cette dimension sera multipliée.

        Returns
        -------
        multiplication: `Dimension | float`
            other == Dimension -> Dimension qui découle de la multiplication des deux dimensions
            other == int ou float -> Valeur qui découle de la conversion depuis les unités SI

        Raises
        ------
        ValueError
            Jetée si la multiplication des deux unités donnent une unité invalide (K^2, ...) ;
        TypeError
            Jetée si "other" n'est ni une Dimension, ni un float, ni un int.
        """
        # Si la valeur est un nombre, retourne la conversion de ce nombre de l'unité SI à l'unité envoyée
        if isinstance(other, (float, int)):
            return (other - self.__offset) * self.__pow__(-1).__factor
        # On sait que la seul dimension avec des unités à décallage est la température (avec le Celsius et le Farenheit)
        # Si des [Θ] sont divisés par des [Θ]^-1 ou inversement, jette une erreur (les [Θ]^2 n'existent pas)
        elif isinstance(other, Dimension) and \
                (not (self.__dimensions["temperature"] + other.__dimensions["temperature"]) in (-1, 0, 1) or
                 (not isclose(self.__offset, 0) and not isclose(other.__offset, 0))):
            raise ValueError("La dimensions de température ne peut pas être différente de -1 ; 0 ; 1. " +
                             f"[Θ1] = {self.__dimensions['temperature']} ({self.__name}) ; " +
                             f"[Θ2] = {other.__dimensions['temperature']} ({other.__name}) -> " +
                             f"[Θ1]*[Θ2] = {self.__dimensions['temperature'] + other.__dimensions['temperature']}")
        # Sinon, les unités sont bonnes, retourne la division des deux unités
        elif isinstance(other, Dimension):
            return Dimension(name=f"{self.__name}*{other.__name}",
                             factor=self.__factor * other.__factor,
                             offset=self.__offset + other.__offset,
                             length=self.__dimensions["length"] + other.__dimensions["length"],
                             mass=self.__dimensions["mass"] + other.__dimensions["mass"],
                             time=self.__dimensions["time"] + other.__dimensions["time"],
                             current=self.__dimensions["current"] + other.__dimensions["current"],
                             temperature=self.__dimensions["temperature"] + other.__dimensions["temperature"],
                             light_intensity=self.__dimensions["light_intensity"] + other.__dimensions["light_intensity"],
                             matter_quantity=self.__dimensions["matter_quantity"] + other.__dimensions["matter_quantity"])
        # Récupère dans le cas où le type n'est pas correct
        else:
            raise TypeError("unsupported operand type(s) for /: 'Dimension' and " +
                            str(type(other)).split("\'")[1] if str(type(other)).count("\'") >= 2 else str(type(other)))

    def __rtruediv__(self, other):
        """Operateur de division : / (inversé)

        Parameters
        ----------
        other: `ìnt | float`
            Ratio par lequel la dimension seré divisée.

        Returns
        -------
        conversion: `float`
            Valeur convertit de l'unité envoyé à son équivalent SI.

        Raises
        ------
        TypeError:
            Jeté si la division ne se fait pas entre un nombre et une dimension.
        """
        # Si la valeur est un nombre, retourne la conversion de ce nombre de l'unité envoyé à son équivalent SI
        if isinstance(other, (int, float)):
            return other * self.__factor + self.__offset
        # Sinon jette une erreur pour indiquer que les types ne sont pas compatibles
        else:
            raise TypeError("unsupported operand type(s) for /: " +
                            str(type(other)).split("\'")[1] if str(type(other)).count("\'") >= 2 else str(type(other)) +
                            " and 'Dimension'")

    def __truediv__(self, other):
        """Opérateur de division : /

        Parameters
        ----------
        other: `Dimension | int | float`
            Unité ou ratio par lequel cette dimension sera divisée.

        Returns
        -------
        division: `Dimension | float`
            other == Dimension -> Dimension qui découle de la division des deux dimensions
            other == int ou float -> Valeur qui découle de la conversion vers les unités SI

        Raises
        ------
        ZeroDivisionError
            Jetée si la valeur de la division est 0 ;
        ValueError
            Jetée si la division des deux unités donnent une unité invalide (K^2, ...) ;
        TypeError
            Jetée si "other" n'est ni une Dimension, ni un float, ni un int.
        """
        # Vérifie que le nombre dans la division n'est pas 0, sinon jette une erreur
        if isinstance(other, (float, int)) and other == 0:
            raise ZeroDivisionError(f"division by zero ({self.__name}/0)")
        # Si la valeur dans la division est un nombre, retourne la multiplication de l'unité par l'inverse de other
        elif isinstance(other, (float, int)):
            return self * (1/other)
        # On sait que la seul dimension avec des unités à décallage est la température (avec le Celsius et le Farenheit)
        # Si des [Θ] sont divisés par des [Θ]^-1 ou inversement, jette une erreur (les [Θ]^2 n'existent pas)
        elif isinstance(other, Dimension) and \
                not (self.__dimensions["temperature"] - other.__dimensions["temperature"]) in (-1, 0, 1):
            raise ValueError("La dimensions de température ne peut pas être différente de -1 ; 0 ; 1. " +
                             f"[Θ1] = {self.__dimensions['temperature']} ({self.__name}) ; " +
                             f" [Θ2] = {other.__dimensions['temperature']} ({other.__name}) -> " +
                             f"[Θ1] / [Θ2] = {self.__dimensions['temperature'] - other.__dimensions['temperature']}")
        # Sinon, les unités sont bonnes, retourne la division des deux unités
        elif isinstance(other, Dimension):
            is_complex = (len(re.findall(r"[/*]", other.__name)) > 0)      # Pour savoir si l'unité doit être encadrée
            return Dimension(name=f"{self.__name}/{f'({other.__name})' if is_complex else other.__name}",
                             factor=self.__factor / other.__factor,
                             offset=(self.__offset - other.__offset) / other.__factor * (not isclose(other.__offset, 0)),
                             length=self.__dimensions["length"] - other.__dimensions["length"],
                             mass=self.__dimensions["mass"] - other.__dimensions["mass"],
                             time=self.__dimensions["time"] - other.__dimensions["time"],
                             current=self.__dimensions["current"] - other.__dimensions["current"],
                             temperature=self.__dimensions["temperature"] - other.__dimensions["temperature"],
                             light_intensity=self.__dimensions["light_intensity"] - other.__dimensions["light_intensity"],
                             matter_quantity=self.__dimensions["matter_quantity"] - other.__dimensions["matter_quantity"])
        # Récupère dans le cas où le type n'est pas correct
        else:
            raise TypeError("unsupported operand type(s) for /: 'Dimension' and " +
                            str(type(other)).split("\'")[1] if str(type(other)).count("\'") >= 2 else str(type(other)))

    def __pow__(self, power, modulo=None):
        """Opérateur de puissance : **

        parameters
        ----------
        power: `int | float`
            Puissance ;
        modulo: `None`
            Modulo de la puissance, négligé ici (utilisé en cryptographie pour les exponentiation modulaires).

        Returns
        -------
        dimension: `Dimension`
            dimension mis à la puissance

        Raises
        ------
        TypeError:
            Jetée si la puissance n'est pas un nombre réel ;
        ValueError:
            Jetée si l'unité résultante aurait Une dimension température différence de -1, 0 ou 1.
        """
        # Si le type de la puissance est un int ou un float
        if isinstance(power, (int, float)):
            # On sait que la seul dimension avec des unités à décallage est la température (avec Celsius et Farenheit)
            # Si des [Θ] sont divisés par des [Θ]^-1 ou inversement, jette une erreur (les [Θ]^2 n'existent pas)
            if self.__dimensions["temperature"] != 0 and power not in (-1, 0, 1):
                raise ValueError("La dimensions de température ne peut pas être différente de -1 ; 0 ; 1. " +
                                 f"[Θ1] = {self.__dimensions['temperature']} ({self.__name}) ; power = {power} -> " +
                                 f"[Θ1]^power = {self.__dimensions['temperature'] * power}")
            else:
                # Sinon retourne la dimension mis à la puissance envoyée
                is_complex = (len(re.findall(r"[/*]", self.__name)) > 0)
                return Dimension(name=f"{f'({self.__name})' if is_complex else self.__name}^{power}",
                                 factor=self.__factor**power,
                                 offset=self.__offset * (power == 1),
                                 length=self.__dimensions["length"] * power,
                                 mass=self.__dimensions["mass"] * power,
                                 time=self.__dimensions["time"] * power,
                                 current=self.__dimensions["current"] * power,
                                 temperature=self.__dimensions["temperature"] * power,
                                 light_intensity=self.__dimensions["light_intensity"] * power,
                                 matter_quantity=self.__dimensions["matter_quantity"] * power)
        else:
            raise TypeError("unsupported operand type(s) for **: 'Dimension' and " +
                            str(type(power)).split("\'")[1] if str(type(power)).count("\'") >= 2 else str(type(power)))

    def __str__(self):
        """Convertit la dimension en un texte lisible pour l'utilisateur.

        Returns
        -------
        dimension: `str`
            Version lisible de la classe.
        """
        symbols = (("length", "L"),
                   ("mass", "M"),
                   ("time", "T"),
                   ("current", "I"),
                   ("temperature", "Θ"),
                   ("light_intensity", "N"),
                   ("matter_quantity", "J"))

        if not any(self.__dimensions[key[0]] for key in symbols if not isclose(self.__dimensions[key[0]], 0)):
            return f"Dimension({self.__name}, factor={self.__factor}, offset={self.__offset}, Dimension = 1)"
        else:
            return f"Dimension({self.__name}, factor={self.__factor}, offset={self.__offset}, Dimension = " +\
                   f"{' '.join([f'[{key[1]}]^{self.__dimensions[key[0]]}' for key in symbols if not isclose(self.__dimensions[key[0]], 0)])})"

    def __repr__(self):
        """Convertit la dimension en un texte lisible pour l'utilisateur.

        Returns
        -------
        dimension: `str`
            Version lisible de la classe.
        """
        return str(self)

    def si_to_unit(self):
        """Retourne les coefficients de conversions pour passer de l'équivalent SI à cette unité.

        Returns
        -------
        factor: `float`
            Facteur de multiplication ;
        offset: `float`
            Décallage à rajouter.
        """
        return 1/self.__factor, - self.__offset / self.__factor

    def unit_to_si(self):
        """Retourne les coefficients de conversions pour passer de cette unité à l'équivalent SI.

        Returns
        -------
        factor: `float`
            Facteur de multiplication ;
        offset: `float`
            Décallage à rajouter.
        """
        return self.__factor, self.__offset
