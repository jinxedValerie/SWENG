from typing import TypeAlias, TextIO
from enum import Enum, auto
from pathlib import Path

Position: TypeAlias = tuple[int, int]

class Block(Enum):
    WALL = auto()
    WAY = auto()


Grid: TypeAlias = list[list[Block]]
class Map:
    grid: Grid
    start: Position
    end: Position
    bonus_points: list[Position]

    def __init__(self, filepath: Path) -> None:
        self.grid, self.start, self.end, self.bonus_points = self.parse_map(filepath)

    @staticmethod
    def parse_map(filepath: Path) -> tuple[Grid, Position, Position, list[Position]]:
        
        file: TextIO = open(filepath)

        file_data: list[str] = file.readlines()
        assert type(file_data) is list[str]
        file.close()
        
        grid: Grid = Grid()
        start: Position
        finish: Position
        bonus_points: list[Position] = []

        for y, row in enumerate(file_data):
            parsed_row: list[Block] = []

            for x, char in enumerate(row):
                match char:     # TODO other format
                    case "W":
                        parsed_row.append(Block.WALL)

                    case ".":
                        parsed_row.append(Block.WAY)
                    
                    case "S":
                        start = (x, y)
                        parsed_row.append(Block.WAY)
                    
                    case "Z":
                        finish = (x, y)
                        parsed_row.append(Block.WAY)
                    
                    case _:     # Numbers
                        bonus_points.append((x, y))
                        parsed_row.append(Block.WAY)
            
            grid.append(parsed_row)

        return (grid, start, finish, bonus_points)