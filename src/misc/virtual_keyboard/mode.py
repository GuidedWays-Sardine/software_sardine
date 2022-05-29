# Librairies par défaut
import os
import sys
from enum import Enum
import unicodedata
from functools import cache


# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))
import src.misc.log as log


class KeyboardMode(Enum):
    """Liste des différents claviers disponibles"""
    NUMPAD = []

    ENGLISH = [["1!",  "2\"", "3£", "4$€", "5%", "6^", "7&", "8*", "9(", "0)", "-_", "=+", ""],
               ["qQ",  "wW",  "eE", "rR",  "tT", "yY", "uU", "iI", "oO", "pP", "[{", "]}"],
               ["aA",  "sS",  "dD", "fF",  "gG", "hH", "jJ", "kK", "lL", ";:", ",@", "#~", ""],
               ["\\|", "zZ",  "xX", "cC",  "vV", "bB", "nN", "mM", ",<", ".>", "/?", ""]]

    FRANCAIS = [["&1",  "é2~", "\"3#", "'4{", "(5[", "-6|", "è7`", "_8\\", "ç9^", "à0@", "°)]", "+=}", ""],
                ["aA",  "zZ",  "eE€",  "rR",  "tT",  "yY",  "uU",  "iI",   "oO",  "pP",  "^¨",  "$£¤"],
                ["qQ",  "sS",  "dD",   "fF",  "gG",  "hH",  "jJ",  "kK",   "lL",  "mM",  "ù%",  "*µ", ""],
                ["<>",  "wW",  "xX",   "cC",  "vV",  "bB",  "nN",  ",?",   ";.",  ":/",  "!§",  ""]]
