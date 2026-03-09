import gfx_stack as gfx
import player
from map import Map

def draw(map: Map):
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

    gfx.set_pixel(start, 'Plum')

    gfx.set_pixel(finish, 'Clairvoyant')
                
    for coin in coins:
        (pos),value = coin
        gfx.set_pixel(pos, 'Tahiti Gold')

    pos_player = player.position()
    gfx.set_pixel(pos_player, "Brown")
    
    moved = player.seen_pos()
    for position in moved:    
        gfx.set_pixel(position, "Mandy")

    while not gfx.stop_prog:
        gfx.event_loop()

    gfx.quit_prog()
