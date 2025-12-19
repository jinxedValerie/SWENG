from machine import Pin
from time import sleep
import sys

green_LED = Pin(15,Pin.OUT)
red_LED = Pin(11,Pin.OUT)
button = Pin(13, Pin.IN, Pin.PULL_UP)

# Morsecode 1 ist lang, 0 ist kurz
MORSE = {
    'A': [0,1],
    'B': [1,0,0,0],
    'C': [1,0,1,0],
    'D': [1,0,0],
    'E': [0],
    'F' : [0,0,1,0],
    'G' : [1,1,0],
    'H' : [0,0,0,0],
    'I' : [0,0],
    'J' : [0,1,1,1],
    'K' : [1,0,1],
    'L' : [0,1,0,0],
    'M' : [1,1],
    'N' : [1,0],
    'O' : [1,1,1],
    'P' : [0,1,1,0],
    'Q' : [1,1,0,1],
    'R' : [0,1,0],
    'S' : [0,0,0],
    'T' : [1],
    'U' : [0,0,1],
    'V' : [0,0,0,1],
    'W' : [0,1,1],
    'X' : [1,0,0,1],
    'Y' : [1,0,1,1],
    'Z' : [1,1,0,0],
}

DASH_DURATION = 0.5
DOT_DURATION = 0.1
PAUSE = 0.2


def button_is_pressed() -> bool: # fragt Status vom Button ab
    if button.value() == 0:
        return True
    else:
        return False


def dot():  # Grüne soll kurz leuchten
    green_LED.on()   
    sleep(DOT_DURATION)
    green_LED.off()


def dash():  # Rote soll lang leuchten
    red_LED.on()   
    sleep(DASH_DURATION)
    red_LED.off()


def show_char(char: str): # setzt aktiven Buchstaben

    pattern = MORSE[char.upper()]
    print(char, end="")     # Terminal Ausgabe: anzeigen des aktuelen Zeichens für die Überprüfung

    for signal in pattern:  # geht durch das Pattern  0 oder 1
        if signal == 0:     # grüne oder rote LED leuchtet
            dot()
        else:
            dash() 

        sleep(PAUSE)        # eine Pause nach Zeichen
    sleep(PAUSE)            # Doppelte Pause nach Charakter


def show_word(word: str):   # setzt aktives Wort

    for char in word:       # geht durch das Wort 
        show_char(char)
    
    sleep(PAUSE*2)          # vierfache Pause nach Pause
    print(" ", end="")      # Terminal Ausgabe: Leerzeichen zwischen den Wörtern

def second_button_press(pin: Pin):  # Interrupt-Handler, schaltet LEDs aus und beendet das Programm
    green_LED.off()
    red_LED.off()
    print("\n\nButton was pressed for the second time!")
    sys.exit()

def main():
    names = input("Namen ohne Sonderzeichen, getrennt durch Leerzeichen: ").split(" ") # erstellt eine Liste von Namen, getrennt durch Leerzeichen
    
    while not button_is_pressed():  # warten auf Knopfdruck
        pass
    while button_is_pressed():  # fallende flanke
        pass

    button.irq(second_button_press, Pin.IRQ_RISING)     # setzt Interrupt-Handler auf

    while True:     # Hauptschleife
        for name in names:
            show_word(name)

if __name__== "__main__":
    main()