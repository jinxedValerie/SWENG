import gfx_stack as gfx
import cli
import map as map_module
import player as player_module
import visuals
import time

def main():
    file_path = cli.get_file_path()

    map = map_module.Map(file_path)

    player = player_module.Player(map)

    # Grafik-Fenster öffnen
    # erzeuge eine 80 x 60 Pixel Zeichenfläche
    # Passen Sie die Größe der Zeichenfläche, an die Größe des Labyrinths an!
    gfx.init_once(map.size())


    # zeichnen, aktualisieren und auf Nutzereingaben warten
    while not gfx.stop_prog:
        visuals.draw(map, player)

        if map.finish() != player.position():
            player.move()
        
        time.sleep(0.25)

        gfx.event_loop()

    # aufräumen
    gfx.quit_prog()

if __name__ == '__main__':
    main()