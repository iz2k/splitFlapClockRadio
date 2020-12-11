#include <msp430.h>
#include <stepper/stepper.hpp>
#include "board.hpp"

Stepper stepperHH;
Stepper stepperMM;
Stepper stepperWW;

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;                     // Stop WDT

    stepperHH = Stepper(hhStepperDef);
    stepperMM = Stepper(mmStepperDef);
    stepperWW = Stepper(wwStepperDef);

    //  ACLK = n/a, MCLK = SMCLK = TACLK = default DCO = ~1MHz
    // Disable the GPIO power-on default high-impedance mode to activate
    // previously configured port settings
    PM5CTL0 &= ~LOCKLPM5;

    TA0CCTL0 |= CCIE;                             // TACCR0 interrupt enabled
    TA0CCR0 = 50000;
    TA0CTL |= TASSEL__SMCLK | MC__CONTINUOUS;     // SMCLK, continuous mode

    __bis_SR_register(LPM0_bits | GIE);           // Enter LPM0 w/ interrupts
    __no_operation();                             // For debug
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
    stepperHH.test();
    stepperMM.test();
    stepperWW.test();
    TA0CCR0 = 50000;                             // Add Offset to TACCR0
}
