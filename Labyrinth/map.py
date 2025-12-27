from typing import TypeAlias, TextIO
from enum import Enum, auto
from pathlib import Path
from type_defs import Block_Position


class Block(Enum):
    WALL = auto()
    WAY = auto()

Grid: TypeAlias = list[list[Block]]

class Map:
    grid: Grid
    start: Block_Position
    end: Block_Position
    bonus_points: list[Block_Position]

    def __init__(self, filepath: Path) -> None:
        self.grid, self.start, self.end, self.bonus_points = self.parse_map(filepath)

    @staticmethod
    def parse_map(filepath: Path) -> tuple[Grid, Block_Position, Block_Position, list[Block_Position]]:
        file: TextIO = open(filepath)

        file_data: list[str] = file.read().splitlines()
        file.close()
        
        grid: Grid = Grid()
        start: Block_Position
        finish: Block_Position
        bonus_points: list[Block_Position] = []

        for y, row in enumerate(file_data):
            parsed_row: list[Block] = []
            for x, char in enumerate(row):
                if any(["." in data_row for data_row in file_data]):    # FORMAT 1
                    match char:
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
                        
                        case digit if digit.isdigit():     # Numbers
                            bonus_points.append((x, y))
                            parsed_row.append(Block.WAY)
                        
                        case _:
                            raise NotImplementedError(f"unkown format token: \"{char}\"")

                else:   # FORMAT 2
                    match char:
                        case "W":
                            parsed_row.append(Block.WAY)

                        case "X":
                            parsed_row.append(Block.WALL)
                        
                        case "S":
                            start = (x, y)
                            parsed_row.append(Block.WAY)
                        
                        case "Z":
                            finish = (x, y)
                            parsed_row.append(Block.WAY)
                        
                        case digit if digit.isdigit():     # Numbers
                            bonus_points.append((x, y))
                            parsed_row.append(Block.WAY)
                        
                        case _:
                            raise NotImplementedError(f"unkown format token: \"{char}\"")
            
            grid.append(parsed_row)

        return (grid, start, finish, bonus_points)

    def map_size(self) -> tuple[int, int]:
        return (len(self.grid[0]), len(self.grid))