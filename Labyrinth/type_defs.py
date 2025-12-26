from enum import Enum, auto
from typing import TypeAlias

Position: TypeAlias = tuple[int, int]
Resolution: TypeAlias = tuple[int, int]

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Color(Enum):
    BLACK = "Black"
    WHITE = "White"
    RED = "Brown"
    GREEN = "Christi"
    BLUE = "Venice Blue"
    PURPLE = "Clairvoyant"