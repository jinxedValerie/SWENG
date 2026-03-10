"""
Geschrieben von Diana Masyluk
"""

import gfx_stack as gfx
from player import Player
from map import Map

def draw(map: Map, player: Player):
    width,height = map.size()
    start = map.get_start()
    finish = map.get_finish()
    coins = map.get_coins()

    for y in range(height):
        for x in range (width):
            pos = (x,y)
            type = map.check_coordinates(pos)
           
            if type == "Path":  
                gfx.set_pixel(pos,'Black')

            elif type == "Wall": 
                gfx.set_pixel(pos,'Deep Koamaru')
    
    for coin in coins:
        pos, value = coin
        gfx.set_pixel(pos, 'Tahiti Gold')

    moved = player.seen_pos()
    for position in moved:    
        gfx.set_pixel(position, "Mandy")

    pos_player = player.position()
    gfx.set_pixel(pos_player, "Brown")
    
    gfx.set_pixel(start, 'Plum')

    gfx.set_pixel(finish, 'Rainforest')


def self_test():
    gfx.init_once((3, 3))
    gfx.set_pixel((0, 2), 'Plum')
    gfx.set_pixel((1, 2), 'Plum')
    gfx.set_pixel((2, 2), 'Plum')
    gfx.set_pixel((1, 1), 'Plum')
    gfx.set_pixel((1, 0), 'Plum')
    
    while not gfx.stop_prog:
        gfx.event_loop()

    gfx.quit_prog()

if __name__ == "__main__":
    self_test()