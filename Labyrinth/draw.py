from typing import assert_never

from avatar import Avatar
from map import Map, Block
from type_defs import Color, Pixel_Resolution, VPixel_Resolution, Block_Position, VPixel_Position
from gfx_helpers import init_gfx_once, draw_rectange, draw_center_padded_rectangle, draw_equilateral_triangle

POI_SIZE_RATIO = .6
BLOCK_SIZE = 5    # length of edges not area (more explicitly: VIRUAL_PIXELS_PER_BLOCK_LENGTH)
VPIXEL_RESOLUTION: VPixel_Resolution
MAX_RESOLUTION: Pixel_Resolution = (640, 480)

def init_draw(map_size: tuple[int, int], block_size: int = BLOCK_SIZE, max_resolution: Pixel_Resolution = MAX_RESOLUTION):
    global VPIXEL_RESOLUTION, MAX_RESOLUTION, BLOCK_SIZE 
    BLOCK_SIZE = block_size
    VPIXEL_RESOLUTION = (map_size[0] * BLOCK_SIZE, map_size[1] * BLOCK_SIZE)
    MAX_RESOLUTION = max_resolution
    init_gfx_once(VPIXEL_RESOLUTION, MAX_RESOLUTION)

def _block_to_vpixel(pos: Block_Position) -> VPixel_Position:
    return (
        pos[0] * BLOCK_SIZE,
        pos[1] * BLOCK_SIZE
    )

def draw_map(map: Map):
        # init_gfx_once((len(map.grid[0]) * BLOCK_SIZE, len(map.grid) * BLOCK_SIZE), MAX_RESOLUTION)

        # draw background
        for y, row in enumerate(map.grid):
            for x, block in enumerate(row):
                color: Color
                match block:
                    case Block.WALL:
                        color = Color.BLACK
                    case Block.WAY:
                        color = Color.WHITE
                    case _:
                        assert_never(block)

                draw_rectange(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, color)

        # draw POIs
        
        draw_center_padded_rectangle(map.start[0] * BLOCK_SIZE, map.start[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, Color.RED, POI_SIZE_RATIO)
        draw_center_padded_rectangle(map.end[0] * BLOCK_SIZE, map.end[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, Color.GREEN, POI_SIZE_RATIO)


        # outer_size = PIXELS_PER_BLOCK
        # inner_size = math.floor(outer_size * POI_SIZE_RATIO)
        # padding = (outer_size - inner_size) // 2
        # draw_rectange((self.start[0] * PIXELS_PER_BLOCK) + padding, (self.start[1] * PIXELS_PER_BLOCK) + padding, inner_size, inner_size, COLOR.RED)
        # draw_rectange((self.end[0] * PIXELS_PER_BLOCK) + padding, (self.end[1] * PIXELS_PER_BLOCK) + padding, inner_size, inner_size, COLOR.GREEN)
        
        for bonus_point in map.bonus_points:
            draw_center_padded_rectangle(bonus_point[0] * BLOCK_SIZE, bonus_point[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, Color.PURPLE, POI_SIZE_RATIO)

        # gfx_stack.set_pixel((self.start[0] * pixel_size, self.start[1] * pixel_size), "Brown")
        # gfx_stack.set_pixel((self.end[0] * pixel_size, self.end[1] * pixel_size), "Christi")