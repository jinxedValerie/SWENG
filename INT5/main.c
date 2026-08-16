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

void zero_crossings(short *samples, size_t length, short threshold, size_t *crossing_idxs, size_t *crossings_idxs_len)
{
    int current_state = 0; // 1: above threshold, -1: below threshold
    size_t crossings = 0;

    for (size_t i = 0; i < length; i++)
    {
        if (samples[i] > threshold)
        {
            if (current_state == -1)
            {
                crossing_idxs[crossings] = i;
                crossings++;
            }
            current_state = 1;
        }
        else if (samples[i] < -threshold)
        {
            if (current_state == 1)
            {
                crossing_idxs[crossings] = i;
                crossings++;
            }
            current_state = -1;
        }
    }
    *crossings_idxs_len = crossings;
}

// diff_buf needs to be at least (length - 1) * sizeof(short) large
void differentiate_array(short array[], size_t length, short *diff_buf)
{
    for (size_t i = 0; i < length - 1; i++)
    {
        diff_buf[i] = array[i + 1] - array[i];
    }
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

const int NOISE_THRESHOLD = 50; // UNSURE WHAT TO USE
Status ndg_dichte(short *feld_ptr, unsigned int anzahl_atw, float *dichte_ori, float *dichte_diff)
{
    // SETUP
    size_t *crossings_buf = malloc(anzahl_atw * sizeof(size_t));
    if (crossings_buf == nullptr)
        return ERROR;
    size_t crossings;

    // CALC ORIGINAL
    zero_crossings(feld_ptr, anzahl_atw, NOISE_THRESHOLD, crossings_buf, &crossings);

    *dichte_ori = (float)crossings / (float)anzahl_atw;

    // CALC DIFFERNTIATED

    size_t diff_buf_len = anzahl_atw - 1;
    short *diff_buf = malloc(diff_buf_len * sizeof(short));
    if (diff_buf == nullptr)
    {
        free(crossings_buf);
        return ERROR;
    }
    differentiate_array(feld_ptr, anzahl_atw, diff_buf);

    zero_crossings(diff_buf, diff_buf_len, NOISE_THRESHOLD, crossings_buf, &crossings);

    *dichte_diff = (float)crossings / (float)diff_buf_len;

    free(diff_buf);
    free(crossings_buf);

    return OK;
}

int main()
{
    return 0;
}

// Status ndg_histogramm(short *feld_ptr, unsigned int anzahl_atw, float *hist_ori, float *hist_diff)
// {
// }