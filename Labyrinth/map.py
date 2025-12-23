from typing import TypeAlias, TextIO, assert_never
from enum import Enum, auto
from pathlib import Path
from gfx_helpers import COLOR, draw_rectange, init_gfx_once
import math


class BLOCK(Enum):
    WALL = auto()
    WAY = auto()


Position: TypeAlias = tuple[int, int]
Grid: TypeAlias = list[list[BLOCK]]

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
        file.close()
        
        grid: Grid = Grid()
        start: Position
        finish: Position
        bonus_points: list[Position] = []

        for y, row in enumerate(file_data):
            parsed_row: list[BLOCK] = []

            for x, char in enumerate(row):
                if any(["." in data_row for data_row in file_data]):    # FORMAT 1
                    match char:     # TODO other format
                        case "W":
                            parsed_row.append(BLOCK.WALL)

                        case ".":
                            parsed_row.append(BLOCK.WAY)
                        
                        case "S":
                            start = (x, y)
                            parsed_row.append(BLOCK.WAY)
                        
                        case "Z":
                            finish = (x, y)
                            parsed_row.append(BLOCK.WAY)
                        
                        case _:     # Numbers
                            bonus_points.append((x, y))
                            parsed_row.append(BLOCK.WAY)

                else:   # FORMAT 2
                    match char:     # TODO other format
                        case "W":
                            parsed_row.append(BLOCK.WAY)

                        case "X":
                            parsed_row.append(BLOCK.WALL)
                        
                        case "S":
                            start = (x, y)
                            parsed_row.append(BLOCK.WAY)
                        
                        case "Z":
                            finish = (x, y)
                            parsed_row.append(BLOCK.WAY)
                        
                        case _:     # Numbers
                            bonus_points.append((x, y))
                            parsed_row.append(BLOCK.WAY)
            
            grid.append(parsed_row)

        return (grid, start, finish, bonus_points)
    
    def draw_map(self, window_size: tuple[int, int]):
        PIXELS_PER_BLOCK = 5    # vertice length not area
        POI_SIZE_RATIO = .6

        init_gfx_once(((len(self.grid[0]) - 1) * PIXELS_PER_BLOCK, len(self.grid) * PIXELS_PER_BLOCK), window_size)

        # draw background
        for y, row in enumerate(self.grid):
            for x, block in enumerate(row):
                color: COLOR
                match block:
                    case BLOCK.WALL:
                        color = COLOR.BLACK
                    case BLOCK.WAY:
                        color = COLOR.WHITE
                    case _:
                        assert_never(block)

                draw_rectange(x * PIXELS_PER_BLOCK, y * PIXELS_PER_BLOCK, PIXELS_PER_BLOCK, PIXELS_PER_BLOCK, color)

        # draw POIs
        outer_size = PIXELS_PER_BLOCK
        inner_size = math.floor(outer_size * POI_SIZE_RATIO)
        padding = (outer_size - inner_size) // 2
        draw_rectange((self.start[0] * PIXELS_PER_BLOCK) + padding, (self.start[1] * PIXELS_PER_BLOCK) + padding, inner_size, inner_size, COLOR.RED)
        draw_rectange((self.end[0] * PIXELS_PER_BLOCK) + padding, (self.end[1] * PIXELS_PER_BLOCK) + padding, inner_size, inner_size, COLOR.GREEN)

        # gfx_stack.set_pixel((self.start[0] * pixel_size, self.start[1] * pixel_size), "Brown")
        # gfx_stack.set_pixel((self.end[0] * pixel_size, self.end[1] * pixel_size), "Christi")