from enum import Enum, auto
from typing import TypeAlias
from random import randint

VPixel_Position: TypeAlias = tuple[int, int]
Block_Position: TypeAlias = tuple[int, int]

VPixel_Resolution: TypeAlias = tuple[int, int]
Pixel_Resolution: TypeAlias = tuple[int, int]

def add_positions(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (
        a[0] + b[0],
        a[1] + b[1]
    )

class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    @classmethod
    def _order(cls):
        return (cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST)
    
    @classmethod
    def random_direction(cls) -> "Direction":
        return cls._order()[randint(0, 3)]

    @property
    def deltas(self) -> tuple[int, int]:
        return self.value

    @property
    def dx(self) -> int:
        return self.value[0]
    
    @property
    def dy(self) -> int:
        return self.value[1]

    def rotate_clockwise(self, steps: int) -> "Direction":
        cur_idx = self._order().index(self)
        next_idx = (cur_idx + steps) % 4
        return self._order()[next_idx]

    def right(self):
        return self.rotate_clockwise(1)

    def left(self):
        return self.rotate_clockwise(-1)
    
    def opposite(self):
        return self.rotate_clockwise(2)
    
    def needed_rotations(self, target: 'Direction') -> int:
        current_idx = self._order().index(self)
        target_idx = self._order().index(target)
        return (target_idx - current_idx) % 4

class Block(Enum):
    WALL = auto()
    WAY = auto()

    @property
    def walkable(self) -> bool:
        match self:
            case Block.WALL:
                return False
            case Block.WAY:
                return True

class Color(Enum):
    BLACK = "Black"
    WHITE = "White"
    RED = "Brown"
    GREEN = "Christi"
    BLUE = "Venice Blue"
    PURPLE = "Clairvoyant"