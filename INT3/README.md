# Inhaltsverzeichnis

1. [Vorbemerkung](#vorbemerkung)
2. [Hauptschleife](#hauptschleife)
3. [Betriebsmodi](#betriebsmodi)
   1. [Sinus-Signale](#teilaufgabe-1-sinus-signale)
   2. [Dreieck-Signale](#teilaufgabe-2-dreieck-signale)
   3. [Schwellwertschalter](#teilaufgabe-3-schwellwertschalter)
   4. [Digitaler Filter](#teilaufgabe-4-digitaler-filter)
4. [Hilfsfunktionen](#hilfsfunktionen)
   1. [Dreiecksfunktion](#dreiecksfunktion)
   2. [DelayLine Filter](#delayline-filter)
5. [Berechnungen zum Digitalfilter](#berechnungen-zum-digitalfilter)

## Vorbemerkung

Für die Funktionsweise des Programms außerhalb der Hauptschleife `void Process_Data()`
und den Helper-Funktionen `float triangle_wave(...)`, `float delay_line_filter(...)`
wird auf die Aufgabenstellung verwiesen.

## Hauptschleife

`void Process_Data()`
Die Hauptschleife wird nach der angegebenen `SAMPLINGRATE` 50.000 mal pro Sekunde (50 kHz) aufgerufen.  
Bei jedem Durchlauf wird die global definierte Variable `NumPoints` zuerst um eins inkrementiert, um einen fortlaufenden Zähler über die Funktionsaufrufe zu haben.  
Danach wird NumPoints mittels Modulo-Arithmetik auf den Bereich [0, SAMPLINGRATE) begrenzt, um mögliche spätere Rundungsfehler und eventuellen overflow zu vermeiden.  
Vor dem lauf der Hauptfunktionen wird nun noch ein absolutes `t` in Sekunden (bzw. durch den Modulo auf [0, 1) begrenzt)
für die Verwendung in den Funktionen gesetzt.

## Betriebsmodi

`switch (State)` schaltet zwischen den Betriebsmodi um.

### Teilaufgabe 1: Sinus-Signale

Erzeugt zwei unabhängige, kontinuierliche Sinusschwingungen, die direkt an die Ausgangskanäle gesendet werden.

- **`Right_Out`:** Berechnet eine 1 kHz Sinusschwingung mittels `sinf`.
- **`Left_Out`:** Berechnet eine 2 kHz Sinusschwingung mittels `sinf`.

Zur Berechnung der Sinusschwingungen wird `float sinf`
und die allgemeine Schwingungsformel `sin(ωt)`, `ω = 2πf` verwendet.

### Teilaufgabe 2: Dreieck-Signale

Nutzt die Hilfsfunktion `triangle_wave`, um zwei identische Wellenformen mit einer festen Phasenverschiebung zu erzeugen.

- **`Right_Out`:** 1 kHz Dreiecksschwingung über `triangle_wave(1000.0f * t)`
- **`Left_Out`:** 1 kHz Dreiecksschwingung, aber mit einer Phasenverschiebung von einer viertel Periode.  
   Da die Hilfsfunktion 1t-Periodisch ist, ergibt sich also zu addierender Wert von `0.25f`.  
   `triangle_wave(1000.0f * t + 0.25f)`

### Teilaufgabe 3: Schwellwertschalter

Erzeugt ein Sinussignal, dessen Frequenz abhängig von der Amplitude des Eingangssignals ist.
Damit beim Umschalten zwischen den Frequenzen kein Sprung im Ausgangssignal entsteht,
wird ein kontinuierlicher Phasenakkumulator statt des absoluten `t`verwendet.

- **Kontrollsignal (`Right_Out`):**  
  Wiederausgabe des Eingangssignals `Left_In`.

- **Überwachung des Maximalwerts des Eingangs:**  
   Der Variablenwert `Max` wird zur Laufzeit kontinuierlich nach oben korrigiert, falls der aktuelle Eingangswert höher ist.

- **Frequenzlogik:**  
  Bewertet `Left_In` gegenüber einem 80%-Schwellenwert des ermittelten Maximums.
  Liegt der Wert darunter, wird `freq = 1000.0f` gesetzt. Liegt er gleichauf oder darüber, springt die Frequenz auf `freq = 5000.0f`.

- **Phasenakkumulator (`phase`):**
  Basiertend auf der Frequenz wird der in diesem durchlauf zu gehende Phasensprung berechnet,
  auf die Phase addiert, und zuletzt die Phase auf [0, 2pi) normiert.

- **Ausgabesignal (`Left_Out`):**  
  Der Ausgabewert kann nun direkt mit der aktuellen Phase und der Sinusfunktion berechnet werden.

### Teilaufgabe 4: Digitaler Filter

Wendet den Verzögerungsfilter auf das Eingangssignal an und normalisiert die Ausgabe dynamisch.

- **Kontrollsignal (`Right_Out`):**  
  Wiederausgabe des Eingangssignals `Left_In`.

- **Überwachung des Maximalwerts des Eingangs:**  
   Der Variablenwert `Max` wird zur Laufzeit kontinuierlich nach oben korrigiert, falls der aktuelle Eingangswert höher ist.

- **Ausgabesignal (`Left_Out`):**  
   Der Ausgabewert wird mit der Hilfsfunktion `float delay_line_filter(...)` berechnet, und dann auf den Maximalwert Normiert.  
  So wird aus dem Wertebereich [`-MAX`, `MAX`] ein Wertebereich von [-1, 1].  
  Somit wird das Ausgabesignal maximal (1 bzw. -1), wenn die Ausgabe der Filterfunktion den Maximalwert des Eingangssignals erreicht.

## Hilfsfunktionen

### Dreiecksfunktion

`float triangle_wave(float t)`

Generiert eine sich wiederholende Dreiecksschwingung, die mit einer Periodendauer von 1t zwischen -1 und 1 oszilliert.

Sie skaliert die Eingangszeit `t` so, dass sich das Signal bei jeder ganzen Zahl wiederholt (`t = 2 * t`),
und verwendet `fmodf(t, 2) - 1`, um die Periode auf einen verarbeitbaren Bereich zu begrenzen.
Die Grundform der Welle wird mit `float y = 1 - fabsf(t)` berechnet und schließlich über `(2 * y) - 1` auf den Wertebereich von -1 bis 1 skaliert.

### DelayLine Filter

`float delay_line_filter(float y)`

Implementiert den in Teilaufgabe 4 beschrieben nichtrekursiven Digitalfilter unter Verwendung eines Ringpuffers (`DelayLine`).

Zuerst wird der bereits gespeicherte Abtastwert vor zwanzig Zyklen mittels Modulo-Arithmetik abgerufen.
Dazu wind einfach `NumPoints` als forlaufender Index verwendet, welcher dann durch den Modulo auf den Grad der `DelayLine` beschränlt wird.
Mit diesem forlaufenden, sich wiederholenden Index wird dann der Abtastwert aus dem Ringpuffer entnommen (`DelayLine[NumPoints % Degree]`).  
Der Ausgangswert `out` ist dann einfach die Summe aus dem aktuellen Eingang `y` und diesem 'historischen' Wert.  
Der aktuelle Abtastwert `y` wird dann am selben Index für zukünftige Filterdurchläufe in den Puffer zurückgeschrieben.
Die Funktion gibt zur Normierung auf einen Wertebereich von -1 bis 1 `out / 2` zurück.

## Berechnungen zum Digitalfilter
