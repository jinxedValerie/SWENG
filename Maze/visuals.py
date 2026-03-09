import gfx_stack as gfx
import player
import map


def draw_map():
    width,hight = map.size()
    start = map.get_start()
    finish = map.get_finish()
    coins = map.get_coins()
    gfx.init_once(width,hight)

    for y in range(hight):
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
           
            elif type == coins:
                gfx.set_pixel(pos, 'white')

def draw_player():
    pos_player = player.position()
    gfx.set_pixel(pos_player, "Brown")
    moved = player.seen_pos()
    gfx.set_pixel(moved, "Mandy")

def main():
   
    draw_map()
    draw_player()

    while not gfx.stop_prog:
        gfx.event_loop()

    gfx.quit_prog()

if __name__ == "__main__":
    main()
    