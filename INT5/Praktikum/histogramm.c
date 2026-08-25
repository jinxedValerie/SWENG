/* Praktikum Software Engineering / Mikrorechentechnik II */
/* TU Dresden, Fakultaet Elektrotechnik */
/* Institut fuer Akustik und Sprachkommunikation */
/* Professur Sprachkommunikation */
/* Autor: Steffen Kuerbis, BAR S53 */
/* Weiterverbreitung nur mit Zustimmung des Autors! */


/* Berechnung der NDG - Histogramme eines Signalabschnittes */


#include <stdio.h>
#include <stdlib.h>

#include "erkenner.h"

const unsigned int SAMPLE_FREQ = 16000;

#define ANZ_HIST_KAN 4
const int HIST_CLASS_1 = 5;
const int HIST_CLASS_2 = 10;
const int HIST_CLASS_3 = 30;
const float HIST_CLASS_1_INC = 1.0f;
const float HIST_CLASS_2_INC = 1.0f;
const float HIST_CLASS_3_INC = 1.0f;
const float HIST_CLASS_4_INC = 1.0f;

extern void zero_crossings(short *samples, size_t length, short threshold, size_t *crossing_idxs, size_t *crossings_idxs_len);
extern void differentiate_array(short array[], size_t length, short *diff_buf);
extern const int NOISE_THRESHOLD;

typedef enum
{
    OK = 0,
    ERROR = -1,
    NOOP = 1,
} Status;


// hist_buf needs to be at least `ANZ_HIST_KAN * sizeof(int)` large
// hist buf needs to be zero-initialized or will add otherwise
void crossing_histogram(size_t *crossing_idxs, size_t crossings, float *hist_buf)
{
    if (crossings < 2)
        return;

    for (size_t i = 0; i < crossings - 1; i++)
    {
        int distance = crossing_idxs[i + 1] - crossing_idxs[i];

        if (distance < HIST_CLASS_1)
            hist_buf[0] += HIST_CLASS_1_INC;
        else if (distance < HIST_CLASS_2)
            hist_buf[1] += HIST_CLASS_2_INC;
        else if (distance < HIST_CLASS_3)
            hist_buf[2] += HIST_CLASS_3_INC;
        else
            hist_buf[3] += HIST_CLASS_4_INC;
    }
}

Status ndg_histogramm(short *feld_ptr, unsigned int anzahl_atw, float *hist_ori, float *hist_diff)
{
    if (feld_ptr == NULL || hist_ori == NULL || hist_diff == NULL)
        return ERROR;

    // SETUP
    size_t *crossings_buf = malloc(anzahl_atw * sizeof(size_t));
    if (crossings_buf == NULL)
        return ERROR;
    size_t crossings;

    // ZERO OUT IN-HIST-BUFS
    for (size_t i = 0; i < ANZ_HIST_KAN; i++)
    {
        hist_ori[i] = 0;
        hist_diff[i] = 0;
    }

    // CALC ORI
    zero_crossings(feld_ptr, anzahl_atw, NOISE_THRESHOLD, crossings_buf, &crossings);
    crossing_histogram(crossings_buf, crossings, hist_ori);

    // CALC DIFF
    size_t diff_buf_len = anzahl_atw - 1;
    short *diff_buf = malloc(diff_buf_len * sizeof(short));
    if (diff_buf == NULL)
    {
        free(crossings_buf);
        return ERROR;
    }

    differentiate_array(feld_ptr, anzahl_atw, diff_buf);
    zero_crossings(diff_buf, diff_buf_len, NOISE_THRESHOLD, crossings_buf, &crossings);
    crossing_histogram(crossings_buf, crossings, hist_diff);

    // CLEANUP
    free(crossings_buf);
    free(diff_buf);
    return OK;
}

//unsigned int ndg_histogramm(short *feld_ptr, unsigned int anzahl_atw, float *hist_ori, float *hist_diff)
//{
//
//int j;
//
///* -- Histogramme loeschen --------------------------- */
//
//  for(j=0;j<ANZ_HIST_KAN;j++)
//  {   hist_ori [j] = 0.;
//  		hist_diff[j] = 0.;
//  }
//
//
//  return (0);
//}
