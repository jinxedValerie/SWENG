import gfx_stack as gfx
import player
import map


def draw():
    width,height = map.size()
    start = map.get_start()
    finish = map.get_finish()
    coins = map.get_coins()

    for y in range(height):
        for x in range (width):
            type = map.check_coordinates(x,y)
            pos = (x,y)
           
            if type == "Path":  
                gfx.set_pixel(pos,'Black')

            elif type == "Wall": 
                gfx.set_pixel(pos,'Deep Koamaru')

            elif type == start:
                gfx.set_pixel(pos, 'Plum')

            elif type == finish: 
                gfx.set_pixel(pos, 'Clairvoyant')
                
           for coin_pos in range(len(coins)):
                if type == coins[coin_pos]:
                    gfx.set_pixel(coins[coin_pos], 'white')

    pos_player = player.position()
    gfx.set_pixel(pos_player, "Brown")
    moved = player.seen_pos()
    for p in range(len(moved)):    
        gfx.set_pixel(moved[p], "Mandy")

def main():
    
    draw_map()
    draw_player()

    while not gfx.stop_prog:
        gfx.event_loop()

    gfx.quit_prog()

if __name__ == "__main__":
    main()
    
