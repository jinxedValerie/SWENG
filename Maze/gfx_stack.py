#!/usr/bin/env python3
# Grafik Utilities für das Software Engineering Grundlagen Praktikum WS2024/25

import pygame
import math

color_dict = {
    "Black" :		 (   0,    0,    0),  # schwarz
    "Valhalla" :	 (  34,   32,   52),  # dunkelgrau
    "Loulou" :		 (  69,   40,   60),  # lila-braun
    "Oiled Cedar" :	 ( 102,   57,   49),  # dunkelbraun
    "Rope" :		 ( 143,   86,   59),  # hellbraun
    "Tahiti Gold" :	 ( 223,  113,   38),  # orange
    "Twine" :		 ( 217,  160,  102),  # ocker
    "Pancho" :		 ( 238,  195,  154),  # sandfarben
    "Golden Fizz" :	 ( 251,  242,   54),  # gelb
    "Atlantis" :	 ( 153,  229,   80),  # hellgrün
    "Christi" :		 ( 106,  190,   48),  # grün
    "Elf Green" :	 (  55,  148,  110),  # türkis
    "Dell" :		 (  75,  105,   47),  # dunkelgrün
    "Verdigris" :	 (  82,   75,   36),  # braun-grün
    "Opal" :		 (  50,   60,   57),  # ...
    "Deep Koamaru" :	 (  63,   63,  116),  # dunkles lila
    "Venice Blue" :	 (  48,   96,  130),  # ... blau
    "Royal Blue" :	 (  91,  110,  225),  # lila-blau
    "Cornflower" :	 (  99,  155,  255),  # helles blau
    "Viking" :		 (  95,  205,  228),  # hellblau
    "Light Steel Blue" : ( 203,  219,  252),  # helles blaugrau
    "White" :		 ( 255,  255,  255),  # weiß
    "Heather" :		 ( 155,  173,  183),  # hell grau
    "Topaz" :		 ( 132,  126,  135),  # ...grau
    "Dim Gray" :	 ( 105,  106,  106),  # ...grau
    "Smokey Ash" :	 (  89,   86,   82),  # dunkelgrau
    "Clairvoyant" :	 ( 118,   66,  138),  # lila
    "Brown" :		 ( 172,   50,   50),  # rot
    "Mandy" :		 ( 217,   87,   99),  # hellrot
    "Plum" :		 ( 215,  123,  186),  # rosa
    "Rainforest" :	 ( 143,  151,   74),  # olivgrün
    "Stinger" :		 ( 138,  111,    4) } # grün-braun
# ursprüngliche Quelle der 32-Farbpalette, Namen und Farbwerte (freie Lizenz):
# http://pixeljoint.com/forum/forum_posts.asp?TID=16247

# globale Variablen im Modul
stop_prog = False # Flag: der Wert 'True' signalisiert den Wunsch des Anwenders zum Programmende
space_key = False # Flag: die Leertaste wurde vom Anwender betätigt, muss vom Programmierer zurückgesetzt werden

# Modul-interne Vars, global für Debuggingzwecke
screen = None # Fenster-Objekt in welches die Leinwand gezeichnet wird
surface = None # Leinwand-Objekt zum Zeichnen
clock = None # Timer-Objekt
screen_wxh = (0,0) # Debugging: angeforderte Größe des Fensters
surface_wxh = (0,0) # Debugging: angeforderte Größe der Leinwand

def init_once(surface_resolution=(160, 120),
              window_title="Software Engineering Grundlagen Praktikum 3, mögliche Eingaben: Leertaste und 'q'",
              screen_resolution = (640, 480)):
    """Wrapper initialisiere pygame und alles was sonst noch benötigt wird."""
    global stop_prog, screen, clock, surface, screen_wxh, surface_wxh
    stop_prog = False
    screen_wxh = screen_resolution
    surface_wxh = surface_resolution
    screen = pygame.display.set_mode(screen_wxh)
    surface = pygame.Surface(surface_wxh)
    pygame.display.set_caption(window_title)
    clock = pygame.time.Clock()
    pygame.init()

def quit_prog():
    """Wrapper aufräumen und vorbereiten für pygame Neustart."""
    pygame.display.quit()
    pygame.quit()

def set_pixel(pos, color):
    """Zeichne ein Pixel mit dem Farbnamen color an Position pos(x,y) in das Anwendungsfenster."""
    # eigentlich wird auf das Surface gezeichnet und dieses später auf das Fenster übertragen
    global surface
    color_val = color_dict[color]
    surface.set_at(pos, color_val)


def color_demo_paint_on_surface():
    """Zeichnet ein Testbild ins Fenster zur einfachen Funktionsüberprüfung."""
    color_it = iter(color_dict)
    for y in range(surface_wxh[1]):
        if y % math.ceil(surface_wxh[1] / 32) == 0:
            color_name = next(color_it)
        for x in range(surface_wxh[0]):
            set_pixel((x,y), color_name)


def event_loop():
    """Events behandeln, Leinwand auf Fensterzeichnen und blockieren für 50ms."""
    global clock, stop_prog, space_key
    # Abfrage 'q'- und Leer-Taste und Window-Close-Button
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_key = False
        if event.type == pygame.QUIT:
            stop_prog = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                stop_prog = True
            if event.key == pygame.K_SPACE:
                 space_key = True

    # zeichnen
    # vor dem Zeichnen das surface heranzoomen
    pygame.transform.scale(surface, screen_wxh, screen)
    pygame.display.flip()
    # Programm auf 20 FPS drosseln
    clock.tick(20)

def main():
    """Simpler Modultest."""
    init_once()

    color_demo_paint_on_surface()

    while not stop_prog:
        event_loop()

    quit_prog()

if __name__ == '__main__':
    main()
