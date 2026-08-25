/* Praktikum Software Engineering / Mikrorechentechnik II */
/* TU Dresden, Fakultaet Elektrotechnik */
/* Institut fuer Akustik und Sprachkommunikation */
/* Professur Sprachkommunikation */
/* Autor: Steffen Kuerbis, BAR S53 */
/* Weiterverbreitung nur mit Zustimmung des Autors! */


/* Berechnung der NDG - Dichte eines Signalabschnittes */


#include <stdio.h>
#include <stdlib.h>

// diff_buf needs to be at least `(length - 1) * sizeof(short)` large
void differentiate_array(short array[], size_t length, short *diff_buf)
{
    for (size_t i = 0; i < length - 1; i++)
    {
        diff_buf[i] = array[i + 1] - array[i];
    }
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


const int NOISE_THRESHOLD = 50; // UNSURE WHAT TO USE
unsigned int ndg_dichte(short *feld_ptr, unsigned int anzahl_atw, float *dichte_ori, float *dichte_diff)
{
    if (feld_ptr == NULL || dichte_ori == NULL || dichte_diff == NULL)
        return -1;

    // SETUP
    size_t *crossings_buf = malloc(anzahl_atw * sizeof(size_t));
    if (crossings_buf == NULL)
        return -1;
    size_t crossings;

    // CALC ORIGINAL
    zero_crossings(feld_ptr, anzahl_atw, NOISE_THRESHOLD, crossings_buf, &crossings);

    *dichte_ori = (float)crossings / (float)anzahl_atw;

    // CALC DIFFERNTIATED

    size_t diff_buf_len = anzahl_atw - 1;
    short *diff_buf = malloc(diff_buf_len * sizeof(short));
    if (diff_buf == NULL)
    {
        free(crossings_buf);
        return -1;
    }
    differentiate_array(feld_ptr, anzahl_atw, diff_buf);

    zero_crossings(diff_buf, diff_buf_len, NOISE_THRESHOLD, crossings_buf, &crossings);

    *dichte_diff = (float)crossings / (float)diff_buf_len;

    free(diff_buf);
    free(crossings_buf);

    return 0;
}

