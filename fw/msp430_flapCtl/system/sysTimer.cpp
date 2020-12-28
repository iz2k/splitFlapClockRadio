/*
 * sysTimer.cpp
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */

#include <msp430.h>
#include <system/sysTimer.hpp>

#define SYSTIMER_SRC_FREQ       32768
#define SYSTIMER_PERIOD_MS      3

bool flagSysTimer;

void initSysTimer(){
    flagSysTimer = false;
    TA0CCTL0 |= CCIE;
    TA0CCR0 = SYSTIMER_SRC_FREQ*SYSTIMER_PERIOD_MS/1000;
    TA0CTL |= TASSEL__ACLK | MC__UP;
}

// Timer A0 interrupt service routine
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector = TIMER0_A0_VECTOR
__interrupt void Timer_A (void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(TIMER0_A0_VECTOR))) Timer_A (void)
#else
#error Compiler not supported!
#endif
{
    flagSysTimer = true;
}




