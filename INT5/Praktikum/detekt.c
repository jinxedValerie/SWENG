/* Praktikum Software Engineering / Mikrorechentechnik II */
/* TU Dresden, Fakultaet Elektrotechnik */
/* Institut fuer Akustik und Sprachkommunikation */
/* Professur Sprachkommunikation */
/* Autor: Steffen Kuerbis, BAR S53 */
/* Weiterverbreitung nur mit Zustimmung des Autors! */


/* Detektion des Nutzsignals */


#include <stdio.h>
#include <stdlib.h>

#define FENSTER         320    /* Fensterlaenge=20 ms fuer Energieberechnung */
#define MIN_FENSTER_ANZ  10    /* Minimal 10 Fenster Signal */
#define SCHWELLWERT      10    /* Abstand Effektivwertquadrat Signal-Pause */


int mean(short array[], size_t length)
{
    long sum = 0;

    for (size_t i = 0; i < length; i++)
    {
        sum += array[i];
    }

    return sum / length;
}

int mean_square(short array[], size_t length)
{
    long long squared_sum = 0;

    for (size_t i = 0; i < length; i++)
    {
        squared_sum += (long long)array[i] * array[i];
    }

    return squared_sum / length;
}

int array_max(int array[], size_t length)
{
    int max = 0;
    for (size_t i = 0; i < length; i++)
    {
        if (array[i] > max)
        {
            max = array[i];
        }
    }
    return max;
}

//const unsigned int ENERGY_BLUR = SAMPLE_FREQ / 100;              // UNSURE WHAT TO USE
//const float ENERGY_RELATIVE_THRESHOLD = 0.25f;                   // UNSURE WHAT TO USE
//const unsigned int ENERGY_DURATION_THRESHOLD = SAMPLE_FREQ / 10; // UNSURE WHAT TO USE
int signal_detekt(short **sample_anfang, unsigned int *sample_anzahl)
{
    if (sample_anfang == NULL || sample_anzahl == NULL)
        return -1;

    // SETUP
    short *full_samples = *sample_anfang;
    size_t full_sample_length = *sample_anzahl;

    short *signal_samples = full_samples;
    size_t signal_length = 0;

    // ZERO LENGTH GUARD
    if (full_sample_length == 0)
        return 1;

    // CALCULATE ENERGY
    int *energy = malloc(full_sample_length * sizeof(int));
    if (energy == NULL)
        return -1;

    for (size_t i = 0; i < full_sample_length; i++)
    {
        size_t start_idx = (i < FENSTER) ? 0 : (i - FENSTER);
        size_t window_len = (i < FENSTER) ? (i + 1) : FENSTER;
        energy[i] = mean_square(&full_samples[start_idx], window_len);
    }

    int max = array_max(energy, full_sample_length);
    int energy_threshold = (int)((float)max * ((float)SCHWELLWERT / 100.0f));

    // SIGNAL DETECTION
    for (size_t i = 0; i < full_sample_length; i++)
    {
        // FIND SIGNAL BEGINNING
        if (energy[i] > energy_threshold)
        {
            signal_samples = &full_samples[i];
            signal_length = full_sample_length - i;

            // FIND SIGNAL LENGTH
            for (size_t offset = 1; offset < full_sample_length - i; offset++)
            {
                if (energy[i + offset] < energy_threshold)
                {
                    signal_length = offset;
                    break;
                }
            }
        }
        if (signal_length > MIN_FENSTER_ANZ)
            break;
    }
    free(energy);

    if (signal_length < MIN_FENSTER_ANZ)
        return 1;

    // REMOVE DC PART
    int DC_level = mean(signal_samples, signal_length);
    for (size_t i = 0; i < signal_length; i++)
    {
        signal_samples[i] -= DC_level;
    }

    // ESTABLISH RETURN STATE
    *sample_anfang = signal_samples;
    *sample_anzahl = signal_length;
    printf("Signal length: %d\n", signal_length);

    return 0;
}
