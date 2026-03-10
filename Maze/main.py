"""
Geschrieben von allen
"""

import gfx_stack as gfx
import cli
import map as map_module
import player as player_module
import visuals
import time

def main():
    file_path = cli.get_file_path()
    if not file_path:
        file_path = "./mazes/Labyrinth-1.txt"
    
    map = map_module.Map(file_path)

    player = player_module.Player(map)

    gfx.init_once(map.size())


    while not gfx.stop_prog:
        visuals.draw(map, player)

        if map.get_finish() != player.position():
            player.move()
        
        # time.sleep(0.25)

        gfx.event_loop()

    # aufräumen
    gfx.quit_prog()

if __name__ == '__main__':
    main()