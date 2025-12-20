#!/usr/bin/env python3

# Optionale Teilaufgabe, Kommandozeilenargumente
# ermöglicht das Angeben einer anderen Labyrinth-Daten-Datei per Kommandozeile
# die Anpassung dieses Quellcodes ist dafür notwendig
#
# Aufruf des Demos von der Kommandozeile:
#  python3 kommandozeilen_argumente.py --demo ein-Wert

# Tutorial:
#  https://realpython.com/command-line-interfaces-python-argparse/#adding-arguments-and-options

import argparse

def get_args():
    """Beispiel um Kommandozeilenargumente einzulesen."""
    parser = argparse.ArgumentParser(description="Kommandozeilenparameter Demo")
    parser.add_argument('-d', '--demo', metavar='Argument',
                        default="ein Default-Wert",
                        help="Demonstration zur Nutzung von Kommandozeilenparameter mit Python")
    return parser.parse_args()

def demo():
    """Beispiel zur Nutzung des Kommandozeilenparameters."""

    # Kommandozeilenargumente einlesen und Information auf Konsole ausgeben
    # Nutzungsbeispiel:
    #    python3 main.py --demo "jetzt ein spezieller Wert"
    args = get_args()
    print("Demo-Kommandozeilenparameter-Wert: " + args.demo + ".")


if __name__ == '__main__':
    demo()
