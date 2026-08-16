#include <stdlib.h>

const unsigned int SAMPLE_FREQ = 16000;

typedef enum
{
    OK = 0,
    ERROR = -1,
    NOOP = 1,
} Status;

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

const unsigned int ENERGY_BLUR = SAMPLE_FREQ / 100;              // UNSURE WHAT TO USE
const float ENERGY_RELATIVE_THRESHOLD = 0.25f;                   // UNSURE WHAT TO USE
const unsigned int ENERGY_DURATION_THRESHOLD = SAMPLE_FREQ / 10; // UNSURE WHAT TO USE
Status signal_detekt(short **sample_anfang, unsigned int *sample_anzahl)
{
    // SETUP
    short *full_samples = *sample_anfang;
    size_t full_sample_length = *sample_anzahl;
    if (full_sample_length < ENERGY_BLUR || full_sample_length < ENERGY_DURATION_THRESHOLD)
        return NOOP;

    short *signal_samples = full_samples;
    size_t signal_length = 0;

    // ZERO LENGTH GUARD
    if (full_sample_length == 0)
        return NOOP;

    // CALCULATE ENERGY
    int *energy = calloc(full_sample_length, sizeof(int));
    if (energy == nullptr)
        return ERROR;

    for (size_t i = ENERGY_BLUR; i < full_sample_length; i++)
    {
        energy[i] = mean_square(&full_samples[i - ENERGY_BLUR], ENERGY_BLUR);
    }

    int max = array_max(energy, full_sample_length);
    int energy_threshold = (int)((float)max * ENERGY_RELATIVE_THRESHOLD);

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
        if (signal_length > ENERGY_DURATION_THRESHOLD)
            break;
    }
    free(energy);

    if (signal_length < ENERGY_DURATION_THRESHOLD)
        return NOOP;

    // REMOVE DC PART
    int DC_level = mean(signal_samples, signal_length);
    for (size_t i = 0; i < signal_length; i++)
    {
        signal_samples[i] = signal_samples[i] - DC_level;
    }

    // ESTABLISH RETURN STATE
    *sample_anfang = signal_samples;
    *sample_anzahl = signal_length;
    return OK;
}

int main()
{
    return 0;
}

// Status ndg_dichte(short *feld_ptr, unsigned int anzahl_atw, float *dichte_ori, float *dichte_diff)
// {
// }

// Status ndg_histogramm(short *feld_ptr, unsigned int anzahl_atw, float *hist_ori, float *hist_diff)
// {
// }