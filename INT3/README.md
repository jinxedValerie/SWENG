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
6. [Programmcode](#programmcode)

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

Wenn die durch den Grad des Filters erzeugte Phasenverschiebung zwischen dem aktuellen und dem vorherigen Abtastwerts ein ganzzahliges Vielfaches einer Periodendauer (`n * T`) erreicht, wird der Ausgabewert des Filters maximal (Durchlassbereich).  
Umgekehrt wird der Ausgabewert minimal, wenn die Phasenverschiebung `n * T + T/2` erreicht (Sperrbereich)

Bei der festgelegten Abtastrate von `50 kHz` und Grad `i = 20` ergeben sich damit folgende Werte für Sperr- und Durchlassbereich:

`delta t = T * i = (1/f) * i = (1/50 kHz) * 20 = 20 us * 20 = 0,4 ms`
`T = 1/f`

- **Durchlassbereich**:  
  `delta t = n * T`  
  `f = n / delta t`  
  `f_1 = 2500 Hz` (mit n = 1, auch alle ganzzahligen Vielfache davon)
- **Sperrbereich**:
  `delta t = (n + 1/2) * T`  
  `f = (n + 1/2) / delta t`  
  `f_0 = 1250 Hz`, `f_1 = 3750 Hz`, ...

In der Praktikumsdurchführung konnten diese Werte experimentell bestätigt werden.

## Programmcode

```c
/*********************************************************/
/* Praktikum Mikrorechentechnik II */
/* Student’s practice Microcomputing II */
/* */
/* Function generator and digital FIR filter */
/* */
/* by A. Schmidt, TNT, IfN, TU Dresden */
/* October 2013 */
/*********************************************************/

// #include "ADDS_21161_EzKit.h"
// #include <def21161.h>
#include <math.h>
#include <stddef.h>

/*********************************************************/
/* sampling frequency : 50 kHz */
/* input signals : Right_In, Left_In */
/* output signals : Right_Out, Left_Out */
/* input/output signal type: float */
/* */
/* output signals externally limited to -1..+1 */
/*********************************************************/

/*** constants and extern variables***********************/
const float PI = 3.14159f;
const int SAMPLINGRATE = 50000;
extern int State;
extern float Left_In;
extern float Right_In;
extern float Left_Out;
extern float Right_Out;

/*** variables *******************************************/
int f = 0;                  // control variable
int h = 0;                  // control variable
unsigned int NumPoints = 0; // control variable
#define Degree 20           // degree of the filter, i.e. tap number
float DelayLine[Degree];    // delay line for filter of degree 20
int Index = 0;              // index for delay line
float Max = -10.0;          // to keep the maximum, initiated with a
                            // value well below any input signal

// repeating triangle function; repeats every 1 t; y: [-1, 1]
float triangle_wave(float t)
{
    t = 2 * t;              // make repeating every 1 t
    t = fmodf(t, 2) - 1;    // clamp t to [-1, 1)
    float y = 1 - fabsf(t); // core function
    return (2 * y) - 1;     // clamp y to [-1, 1]
}

float delay_line_filter(float y)
{
    // lets signal pass if phase difference is n ∗ 2π
    // doesn't let signal pass if phase difference is n ∗ 2π + π
    float out;
    out = y + DelayLine[NumPoints % Degree]; // core delay line filter functionality
    DelayLine[NumPoints % Degree] = y;       // store current value for later filter usage
    return out / 2;                          // clamp filter to [-1, 1]
}

/*** do the processing ***********************************/
void Process_Data()
{
    NumPoints++; // overflow?; should not practically happen during the tests, but might be relevant for long running applications
    NumPoints = fmodf(NumPoints, SAMPLINGRATE);
    float t = (float)NumPoints / (float)SAMPLINGRATE; // rounding errors?; might get inlined anyway, but for high values of t might still get inaccurate
    /*********************************************************/
    /* place here code for control signals */
    switch (State)
    {
    case 0:
    {
        Right_Out = sinf(2.0f * PI * 1000.0f * t);
        Left_Out = sinf(2.0f * PI * 2000.0f * t);

        break;
    }
    case 1:
    {
        Right_Out = triangle_wave(1000.0f * t);
        Left_Out = triangle_wave(1000.0f * t + 0.25f);
        break;
    }
    case 2:
    {
        Right_Out = Left_In;       // control signal
        static float phase = 0.0f; // continuis phase accumulator
        if (Max < Left_In)         // adjust maximum at runtime
        {
            Max = Left_In;
        }

        float freq;
        if (Left_In < 0.8f * Max) // adjust current frequency at runtime based on current input
        {
            freq = 1000.0f;
        }
        else
        {
            freq = 5000.0f;
        }

        float step = 2.0f * PI * freq / SAMPLINGRATE;
        phase += step;
        phase = fmodf(phase, 2.0f * PI);

        Left_Out = sinf(phase);

        break;
    }
    case 3:
    {
        Right_Out = Left_In;
        if (Max < Left_In) // adjust maximum at runtime
        {
            Max = Left_In;
        }

        Left_Out = delay_line_filter(Left_In) / Max;

        break;
    }
    }
}
```
