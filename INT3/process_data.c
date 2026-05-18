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

#define kHz *1000.0f

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

    float t = (float)NumPoints / (float)SAMPLINGRATE; // rounding errors?; might get inlined anyway, but for high values of t might still get inaccurate
    /*********************************************************/
    /* place here code for control signals */
    switch (State)
    {
    case 0:
    {
        Right_Out = sinf(2.0f * PI * 1 kHz * t);
        Left_Out = sinf(2.0f * PI * 2 kHz * t);

        break;
    }
    case 1:
    {

        Right_Out = triangle_wave(1 kHz * t);
        Left_Out = triangle_wave(1 kHz * t + 0.25f);

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
        Left_Out = delay_line_filter(Left_In);

        break;
    }
    }
}
