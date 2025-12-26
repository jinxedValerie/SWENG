#!/usr/bin/env python3
# main

import gfx_stack as gfx
import kommandozeilen_argumente as cmdargs
from map import Map
from pathlib import Path
from draw import draw_map, init_draw

def main():
    """Beispiel einer Mainfunktion für den Versuch."""

    cmdargs.demo()

    # Grafik-Fenster öffnen
    # erzeuge eine 80 x 60 Pixel Zeichenfläche
    # Passen Sie die Größe der Zeichenfläche, an die Größe des Labyrinths an!
    # gfx.init_once((80, 64))

    map = Map(Path("/home/valerie/projects/uni/SWENG1/Labyrinth/maps/Labyrinth-3.txt"))
    init_draw(map.map_size())

    # zeichnen, aktualisieren und auf Nutzereingaben warten
    while not gfx.stop_prog:
        # zeichnen des Testbildes
        # gfx.color_demo_paint_on_surface()

        draw_map(map)

        if gfx.space_key:
            print("Leertaste registriert")

        gfx.event_loop()

    # aufräumen
    gfx.quit_prog()

if __name__ == '__main__':
    main()


