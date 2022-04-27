# Librairies par défaut
import sys
import os
from math import isclose
import re


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.settings_dictionary as sd


class Dimension:
    """Classe permettant de définir chaque unité, dépendament de ses dimensions et des units SI"""

    # Nom de l'unité (pour affichage)
    name = ""

    # Dimensions du système international (en SettingsDictionary pour les rendre insensible au majuscules et minuscules)
    dimensions = sd.SettingsDictionary({"length": 0.0,  # meter (m)     [L]
                                        "mass": 0.0,  # kilogram (kg) [M]
                                        "time": 0.0,  # second (s)    [T]
                                        "current": 0.0,  # Amps (A)      [I]
                                        "temperature": 0.0,  # Kelvin (K)    [Θ]
                                        "light_intensity": 0.0,  # candela (cd)  [N]
                                        "matter_quantity": 0.0})  # mol (mol)     [J]

    # Facteur (comparé au système international)
    factor = 0

    # décallage (comparé au système international)
    offset = 0

    def __init__(self, name, factor=1.0, offset=0.0,
                 length=0, mass=0, time=0, current=0, temperature=0, light_intensity=0, matter_quantity=0):
        self.name = name.replace("x", "*").replace("**", "^").replace("²", "^2")
        self.factor = factor
        self.offset = offset
        self.dimensions = {"length": length,
                           "mass": mass,
                           "time": time,
                           "current": current,
                           "temperature": temperature,
                           "light_intensity": light_intensity,
                           "matter_quantity": matter_quantity}

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        """Retourne si les dimensions des deux unités sont égales. Ne prend pas en compte le ratio et l'offset.

        Returns
        -------
        same_dimension: `bool`
            Retourne vrai si la dimension des deux unités est identique
        """
        return isinstance(other, Dimension) and \
               all(isclose(self.dimensions[key], other.dimensions[key]) for key in list(self.dimensions.keys()))

    def __rmul__(self, other):
        """Opérateur de multiplication : *

        Parameters
        ----------
        other: `int | float`

        Returns
        -------
        division: `Dimension`
            Dimension qui découle de cette multiplication.

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
        division: `Dimension`
            Dimension qui découle de cette multiplication.

        Raises
        ------
        ValueError
            Jetée si la multiplication des deux unités donnent une unité invalide (K^2, ...) ;
        TypeError
            Jetée si "other" n'est ni une Dimension, ni un float, ni un int.
        """
        # Si la valeur dans la multiplication est un int ou un float, retourne une dimension multipliée par la valeur
        if isinstance(other, (float, int)):
            return (other - self.offset) * self.__pow__(-1).factor
        # On sait que la seul dimension avec des unités à décallage est la température (avec le Celsius et le Farenheit)
        # Si des [Θ] sont divisés par des [Θ]^-1 ou inversement, jette une erreur (les [Θ]^2 n'existent pas)
        elif isinstance(other, Dimension) and \
                (not (self.dimensions["temperature"] + other.dimensions["temperature"]) in (-1, 0, 1) or
                 (not isclose(self.offset, 0) and not isclose(other.offset, 0))):
            raise ValueError("La dimensions de température ne peut pas être différente de -1 ; 0 ; 1." +
                             f"[Θ](1) = {self.dimensions['temperature']} ; [Θ](2) = {other.dimensions['temperature']}" +
                             f"[Θ](1) * [Θ](2) = {self.dimensions['temperature'] + other.dimensions['temperature']}")
        # Sinon, les unités sont bonnes, retourne la division des deux unités
        elif isinstance(other, Dimension):
            return Dimension(name=f"{self.name}*{other.name}",
                             factor=self.factor * other.factor,
                             offset=self.offset + other.offset,
                             length=self.dimensions["length"] + other.dimensions["length"],
                             mass=self.dimensions["mass"] + other.dimensions["mass"],
                             time=self.dimensions["time"] + other.dimensions["time"],
                             current=self.dimensions["current"] + other.dimensions["current"],
                             temperature=self.dimensions["temperature"] + other.dimensions["temperature"],
                             light_intensity=self.dimensions["light_intensity"] + other.dimensions["light_intensity"],
                             matter_quantity=self.dimensions["matter_quantity"] + other.dimensions["matter_quantity"])
        # Récupère dans le cas où le type n'est pas correct
        else:
            raise TypeError("unsupported operand type(s) for /: 'Dimension' and " +
                            str(type(other)).split("\'")[1] if str(type(other)).count("\'") >= 2 else str(type(other)))

    def __rtruediv__(self, other):
        """Operateur de division : / inversé

        Parameters
        ----------
        other: `ìnt | float`
            Ratio par lequel la dimension seré divisée
        """
        if isinstance(other, (int, float)):
            return other * self.factor + self.offset
        else:
            raise TypeError("unsupported operand type(s) for /: 'Dimension' and " +
                            str(type(other)).split("\'")[1] if str(type(other)).count("\'") >= 2 else str(type(other)))

    def __truediv__(self, other):
        """Opérateur de division : /

        Parameters
        ----------
        other: `Dimension | int | float`
            Unité ou ratio par lequel cette dimension sera divisée.

        Returns
        -------
        division: `Dimension`
            Dimension qui découle de cette division.

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
            raise ZeroDivisionError(f"division by zero ({self.name}/0)")
        # Si la valeur dans la division est un int ou un float, retourne une dimension divisé par la valeur
        elif isinstance(other, (float, int)):
            return Dimension(name=f"{self.name}/{other}",
                             factor=self.factor / other,
                             offset=self.offset,
                             length=self.dimensions["length"],
                             mass=self.dimensions["mass"],
                             time=self.dimensions["time"],
                             current=self.dimensions["current"],
                             temperature=self.dimensions["temperature"],
                             light_intensity=self.dimensions["light_intensity"],
                             matter_quantity=self.dimensions["matter_quantity"])
        # On sait que la seul dimension avec des unités à décallage est la température (avec le Celsius et le Farenheit)
        # Si des [Θ] sont divisés par des [Θ]^-1 ou inversement, jette une erreur (les [Θ]^2 n'existent pas)
        elif isinstance(other, Dimension) and \
                not (self.dimensions["temperature"] - other.dimensions["temperature"]) in (-1, 0, 1):
            raise ValueError("La dimensions de température ne peut pas être différente de -1 ; 0 ; 1." +
                             f"[Θ](1) = {self.dimensions['temperature']} ; [Θ](2) = {other.dimensions['temperature']}" +
                             f"[Θ](1) / [Θ](2) = {self.dimensions['temperature'] - other.dimensions['temperature']}")
        # Sinon, les unités sont bonnes, retourne la division des deux unités
        elif isinstance(other, Dimension):
            is_complex = (len(re.findall("[\\/\\*]", other.name)) > 0)      # Pour savoir si l'unité doit être encadrée
            return Dimension(name=f"{self.name}/{f'({other.name})' if is_complex else other.name}",
                             factor=other.factor / self.factor,
                             offset=(other.offset - self.offset) / self.factor * (not isclose(self.offset, 0)),
                             length=self.dimensions["length"] - other.dimensions["length"],
                             mass=self.dimensions["mass"] - other.dimensions["mass"],
                             time=self.dimensions["time"] - other.dimensions["time"],
                             current=self.dimensions["current"] - other.dimensions["current"],
                             temperature=self.dimensions["temperature"] - other.dimensions["temperature"],
                             light_intensity=self.dimensions["light_intensity"] - other.dimensions["light_intensity"],
                             matter_quantity=self.dimensions["matter_quantity"] - other.dimensions["matter_quantity"])
        # Récupère dans le cas où le type n'est pas correct
        else:
            raise TypeError("unsupported operand type(s) for /: 'Dimension' and " +
                            str(type(other)).split("\'")[1] if str(type(other)).count("\'") >= 2 else str(type(other)))

    def __pow__(self, power, modulo=None):
        # Si le type de la puissance est un int ou un float
        if isinstance(power, (int, float)):
            # On sait que la seul dimension avec des unités à décallage est la température (avec le Celsius et le Farenheit)
            # Si des [Θ] sont divisés par des [Θ]^-1 ou inversement, jette une erreur (les [Θ]^2 n'existent pas)
            if self.dimensions["temperature"] != 0 and power not in (-1, 0, 1):
                raise ValueError("La dimensions de température ne peut pas être différente de -1 ; 0 ; 1." +
                                 f"[Θ](1) = {self.dimensions['temperature']} ; power = {power}" +
                                 f"[Θ](1) ^ power = {self.dimensions['temperature'] * power}")
            else:
                is_complex = (len(re.findall("[\\/\\*]", self.name)) > 0)
                return Dimension(name=f"{f'({self.name})' if is_complex else self.name}^{power}",
                                 factor=self.factor**power,
                                 offset=self.offset * (power == 1),
                                 length=self.dimensions["length"] * power,
                                 mass=self.dimensions["mass"] * power,
                                 time=self.dimensions["time"] * power,
                                 current=self.dimensions["current"] * power,
                                 temperature=self.dimensions["temperature"] * power,
                                 light_intensity=self.dimensions["light_intensity"] * power,
                                 matter_quantity=self.dimensions["matter_quantity"] * power)
        else:
            raise TypeError("unsupported operand type(s) for **: 'Dimension' and " +
                            str(type(power)).split("\'")[1] if str(type(power)).count("\'") >= 2 else str(type(power)))

    def __str__(self):
        symbols = (("length", "L"),
                   ("mass", "M"),
                   ("time", "T"),
                   ("current", "I"),
                   ("temperature", "Θ"),
                   ("light_intensity", "N"),
                   ("matter_quantity", "J"))

        if not any(self.dimensions[key[0]] for key in symbols if not isclose(self.dimensions[key[0]], 0)):
            return f"Dimension({self.name}, factor={self.factor}, offset={self.offset}, Dimension = [Dimensionless]"
        else:
            return f"Dimension({self.name}, factor={self.factor}, offset={self.offset}, Dimension = " +\
                   f"{' '.join([f'[{key[1]}]^{self.dimensions[key[0]]}' for key in symbols if not isclose(self.dimensions[key[0]], 0)])})"

    def __repr__(self):
        return str(self)
