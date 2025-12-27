from enum import Enum, auto
from typing import TypeAlias

VPixel_Position: TypeAlias = tuple[int, int]
Block_Position: TypeAlias = tuple[int, int]

VPixel_Resolution: TypeAlias = tuple[int, int]
Pixel_Resolution: TypeAlias = tuple[int, int]

class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    @classmethod
    def _order(cls):
        return (cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST)
    
    @property
    def dx(self) -> int:
        return self.value[0]
    
    @property
    def dy(self) -> int:
        return self.value[1]

    def rotate(self, steps: int) -> "Direction":
        cur_idx = self._order().index(self)
        next_idx = (cur_idx + steps) % 4
        return self._order()[next_idx]

    def right(self):
        return self.rotate(1)

    def left(self):
        return self.rotate(-1)
    
    def opposite(self):
        return self.rotate(2)
    
    def needed_rotations(self, target: 'Direction') -> int:
        current_idx = self._order().index(self)
        target_idx = self._order().index(target)
        return (target_idx - current_idx) % 4

class Color(Enum):
    BLACK = "Black"
    WHITE = "White"
    RED = "Brown"
    GREEN = "Christi"
    BLUE = "Venice Blue"
    PURPLE = "Clairvoyant"