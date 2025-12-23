import gfx_stack
from enum import Enum

class COLOR(Enum):
    BLACK = "Black"
    WHITE = "White"
    RED = "Brown"
    GREEN = "Christi"
    BLUE = "Venice Blue"
    PURPLE = "Clairvoyant"

def draw_rectange(x: int, y: int, width: int, height: int, color: COLOR):
    for width_offset in range(width):
        for height_offset in range(height):
            gfx_stack.set_pixel(
                (x + width_offset,
                 y + height_offset),
                color.value
            )

gfx_initialized = False

def init_gfx_once(size: tuple[int, int], max_resolution: tuple[int, int] = (640, 480)):
    global gfx_initialized
    
    if not gfx_initialized:

        window_size: tuple[int, int]
        if size[0] / size[1] > max_resolution[0] / max_resolution[1]:   # make window always fit into max_resolution
            window_size = (
                max_resolution[0],
                round((max_resolution[0] / size[0]) * size[1])
            )
        else:
            window_size = (
                round((max_resolution[1] / size[1]) * size[0]),
                max_resolution[1]
            )
        print(window_size)
        gfx_stack.init_once(size, screen_resolution=window_size)
        gfx_initialized = True