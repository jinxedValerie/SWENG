/*********************************************************/
/* Praktikum Mikrorechentechnik II */
/* Student’s practice Microcomputing II */
/* */
/* Function generator and digital FIR filter */
/* */
/* by A. Schmidt, TNT, IfN, TU Dresden */
/* October 2013 */
/*********************************************************/

#include "ADDS_21161_EzKit.h"
#include <def21161.h>
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
const float PI = 3.14159;
const int SAMPLINGRATE = 50000;
extern int State;
extern float Left_In;
extern float Right_In;
extern float Left_Out;
extern float Right_Out;

/*** variables *******************************************/
int f = 0;           // control variable
int h = 0;           // control variable
int NumPoints = 0;   // control variable
int Degree = 20;     // degree of the filter, i.e. tap number
float DelayLine[20]; // delay line for filter of degree 20
int Index = 0;       // index for delay line
float Max = -10.0;   // to keep the maximum, initiated with a
                     // value well below any input signal

/*** do the processing ***********************************/
void Process_Data()
{
    NumPoints++;

    float t = (float)NumPoints / (float)SAMPLINGRATE; // rounding errors?; might get inlined anyway
    /*********************************************************/
    /* place here code for control signals */
    switch (State)
    {
    case 0:
    {
        Right_Out = sinf(2.0 * PI * 1000.0 * t);
        Left_Out = sinf(2.0 * PI * 2000.0 * t);

        break;
    }
    case 1:
    {
        float t1 = (float)NumPoints / (float)SAMPLINGRATE;
        float t2 = ((float)NumPoints + 12.5)/ (float)SAMPLINGRATE;

        Right_Out = 2.0* 1.0 *fabs(fmax(1.0 - fmod(2.0 * 1000 * t1, 2.0), -1.0)) - 1.0;
        Left_Out = 2.0* 1.0 * fabs(fmax(1.0 - fmod(2.0 * 1000 * t2, 2.0), -1.0)) - 1.0;
        break;
    }
    case 2:
    {
        Right_Out = Left_In;
        float phase = 0.0 if (Max < Left_In)
        {
            Max = Left_In;
        }
        float freq;
        if (Left_In < 0.8 * Max)
{
            freq = 1000.0;
        }
        else
{
            freq = 5000.0;
        }

        float step = 2.0 * PI * freq / SAMPLINGRATE;
        phase += step

        Left_OUT = sinf(phase)

        /*********************************************************/
        /* place here code for threshold signal */
        break;
        /*********************************************************/
    }
    case 3:
    {   

        /*********************************************************/
        /* place here code for digital filter */
        break;
        /*********************************************************/
    }
    }
}
