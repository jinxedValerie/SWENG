#!/usr/bin/env python3
# main

import gfx_stack as gfx
import kommandozeilen_argumente as cmdargs
from map import Map
from pathlib import Path

def paint_smiley():
    """einfache Demonstration zum Zeichnen von Pixeln.
    Farbnamen sind im Modul gfx_stack.py zu finden."""
    gfx.set_pixel((30,20), "Black")
    gfx.set_pixel((31,20), "Black")
    gfx.set_pixel((30,21), "Black")
    gfx.set_pixel((31,21), "Light Steel Blue")

    gfx.set_pixel((50,21), "Light Steel Blue")
    gfx.set_pixel((51,21), "Black")
    gfx.set_pixel((50,20), "Black")
    gfx.set_pixel((51,20), "Black")

    gfx.set_pixel((30,30), "Mandy")
    gfx.set_pixel((32,32), "Brown")
    gfx.set_pixel((34,33), "Brown")
    gfx.set_pixel((36,34), "Brown")
    gfx.set_pixel((38,35), "Brown")

    gfx.set_pixel((40,35), "Brown")

    gfx.set_pixel((42,35), "Brown")
    gfx.set_pixel((44,34), "Brown")
    gfx.set_pixel((46,33), "Brown")
    gfx.set_pixel((48,32), "Brown")
    gfx.set_pixel((50,30), "Mandy")


def main():
    """Beispiel einer Mainfunktion für den Versuch."""

    cmdargs.demo()

    # Grafik-Fenster öffnen
    # erzeuge eine 80 x 60 Pixel Zeichenfläche
    # Passen Sie die Größe der Zeichenfläche, an die Größe des Labyrinths an!
    # gfx.init_once((80, 64))

    map = Map(Path("/home/valerie/projects/uni/SWENG1/Labyrinth/maps/Labyrinth-2.txt"))

    # zeichnen, aktualisieren und auf Nutzereingaben warten
    while not gfx.stop_prog:
        # zeichnen des Testbildes
        # gfx.color_demo_paint_on_surface()

        map.draw_map(window_size=(1920, 1080))

        # Beispiel reagieren auf Space key
        if gfx.space_key == True:
            print("Leertaste registriert")
            # Smiley zeichnen
            # paint_smiley()

        gfx.event_loop()

    # aufräumen
    gfx.quit_prog()

if __name__ == '__main__':
    main()


