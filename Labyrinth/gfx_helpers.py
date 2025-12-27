import gfx_stack
import math
from type_defs import Direction, Color, VPixel_Position, VPixel_Resolution, Pixel_Resolution
from typing import Any, Literal

def sign(a: int) -> Literal[1] | Literal[-1]:
    if a >= 0:
        return 1
    return -1

def draw_rectange(x: int, y: int, width: int, height: int, color: Color):
    draw_direction_x, draw_direction_y = sign(width), sign(height)
    for width_offset in range(0, width, draw_direction_x):
        for height_offset in range(0, height, draw_direction_y):
            gfx_stack.set_pixel(
                (x + width_offset,
                 y + height_offset), 
                color.value
            )

def draw_center_padded_rectangle(x: int, y: int, width: int, height: int, color: Color, padding_ratio: float):
    inner_width, inner_height = math.floor(width * padding_ratio), math.floor(height * padding_ratio)
    padding_x, padding_y = (width - inner_width) // 2, (height - inner_height) // 2
    draw_rectange(x + padding_x, y + padding_y, inner_width, inner_height, color)

def create_default_matrix(x: int, y: int, value: Any) -> list[list[Any]]:
    return [[value for _ in range(x)] for _ in range(y)]

def rotate_matrix_clockwise_90(matrix: list[list[Any]]) -> list[list[Any]]: 
    return [list(a) for a in zip(*reversed(matrix))]

def draw_equilateral_triangle(top_left: VPixel_Position, size: int, direction: Direction, color: Color):
    canvas: list[list[bool]] = create_default_matrix(size, size, False)
    width, padding = size, 0

    y = 0
    while (width > 0):
        for x in range(width):
            canvas[y][x + padding] = True
        
        padding += 1
        width -= 2
        y += 1
    
    for _ in range(Direction.SOUTH.needed_rotations(direction)):
        canvas = rotate_matrix_clockwise_90(canvas)


    for y_offset, row in enumerate(canvas):
        for x_offset, pixel_set in enumerate(row):
            if not pixel_set:
                continue
            gfx_stack.set_pixel(
                (
                    top_left[0] + x_offset,
                    top_left[1] + y_offset
                ),
                color.value
            )



gfx_initialized = False

def init_gfx_once(vpixel_resolution: VPixel_Resolution, max_resolution: Pixel_Resolution = (640, 480)):
    global gfx_initialized
    
    if not gfx_initialized:

        window_size: Pixel_Resolution
        if vpixel_resolution[0] / vpixel_resolution[1] > max_resolution[0] / max_resolution[1]:   # make window always fit into max_resolution
            window_size = (
                max_resolution[0],
                round((max_resolution[0] / vpixel_resolution[0]) * vpixel_resolution[1])
            )
        else:
            window_size = (
                round((max_resolution[1] / vpixel_resolution[1]) * vpixel_resolution[0]),
                max_resolution[1]
            )
        print(window_size)
        gfx_stack.init_once(vpixel_resolution, screen_resolution=window_size)
        gfx_initialized = True