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
int NumPoints = 1;   // control variable
int Degree = 20;     // degree of the filter, i.e. tap number
float DelayLine[20]; // delay line for filter of degree 20
int Index = 0;       // index for delay line
float Max = -10.0;   // to keep the maximum, initiated with a
                     // value well below any input signal

/*** do the processing ***********************************/
void Process_Data()
{
    /*********************************************************/
    /* place here code for control signals */
    switch (State)
    {
    case 0:
    {
        /*********************************************************/
        /* place here code for sinusoidal signals */
        break;
        /*********************************************************/
    }
    case 1:
    {
        /*********************************************************/
        /* place here code for triangle / sawtooth signals */
        break;
        /*********************************************************/
    }
    case 2:
    {
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