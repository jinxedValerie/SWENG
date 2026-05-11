/*********************************************************/
/* Praktikum Mikrorechentechnik II */
/* Student’s practice Microcomputing II */
/* */
/* Function generator and digital FIR filter */
/* */
/* by A. Schmidt, TNT, IfN, TU Dresden */
/* April/May 2012 */
/* */
/* based on the CTalkThru example given for the EZ-Kit */
/* ADSP-21161N by Analog Devices */
/*********************************************************/
#include "ADDS_21161_EzKit.h"
#include <def21161.h>
#include <math.h>
#include <signal.h>
asm("#include <def21161.h>");
/*** variables *******************************************/
int a = 0;       // for simple timer test
int State = 0;   // to control application
bool Run = true; // run program, as long as run = true
void main()
{
    /* Setup Interrupt edges, I/O directions and SPORTs */
    Setup_ADSP21161N();
    Program_SPORT02_TDM_Registers();
    Program_SPORT02_DMA_Channels();
    *(int *)SP02MCTL |= MCE;
    /* Setup audio codec, SPORT0 and SPORT2*/
    Setup_AD1836();
    18
        /* execute a simple timer test */
        a = 0;
    Init_Timer(10000000);
    interrupt(SIG_TMZ0, Timer_Test_Function);
    while (a < 10)
        asm("idle;");
    Stop_Timer();
    /* Init LEDs */
    Init_LED_Flags();
    /* disable all interrupts except used ones */
    Disable_IRQs();
    Enable_IRQ1_IRQ2_SP0I();
    /* set function for IRQ2, i.e. "SW7 pressed", to change state */
    interruptf(SIG_IRQ2, Switch_State);
    /* set function for IRQ1, i.e. "SW6 pressed", to stop program */
    interruptf(SIG_IRQ1, Stop_Execution);
    /* set function for SP01 to transfer signals */
    interruptf(SIG_SP0I, Transfer_Samples);
    while (Run)
    {
        Process_Data();
        asm("idle;");
    }
}