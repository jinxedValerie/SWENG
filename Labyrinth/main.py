#!/usr/bin/env python3
# main

import gfx_stack as gfx
import kommandozeilen_argumente as cmdargs
from avatar import Avatar
from map import Map
from pathlib import Path
from draw import draw_map, init_draw, draw_avatar, draw_step_trace

found_end = False

def main():
    """Beispiel einer Mainfunktion für den Versuch."""

    cmdargs.demo()

    # Grafik-Fenster öffnen
    # erzeuge eine 80 x 60 Pixel Zeichenfläche
    # Passen Sie die Größe der Zeichenfläche, an die Größe des Labyrinths an!
    # gfx.init_once((80, 64))

    map = Map(Path("/home/valerie/projects/uni/SWENG1/Labyrinth/maps/Labyrinth-1.txt"))
    init_draw(map.map_size(), max_resolution=(1200, 800))

    avatar = Avatar(map.start)
    # zeichnen, aktualisieren und auf Nutzereingaben warten
    while not gfx.stop_prog:
        global found_end
        # zeichnen des Testbildes
        # gfx.color_demo_paint_on_surface()

        draw_map(map, found_end)
        draw_step_trace(avatar, trace_width_ratio=0.5) 
        draw_avatar(avatar)

        if gfx.space_key:
            avatar.stumble_around(map)

        if avatar.pos == map.end:
            found_end = True


        gfx.event_loop()

    # aufräumen
    gfx.quit_prog()

if __name__ == '__main__':
    main()


