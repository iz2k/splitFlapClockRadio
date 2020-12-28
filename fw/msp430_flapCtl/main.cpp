#include <msp430.h>
#include <board.hpp>
#include <smbus/smbusSlave.hpp>
#include <smbus/smbusRegMap.hpp>
#include <system/cs.hpp>
#include <system/sysTimer.hpp>
#include <stepper/stepper.hpp>

#define VAR_DECLS
#include <nvm/nvm.hpp>

extern bool flagSysTimer;

Stepper stepperHH;
Stepper stepperMM;
Stepper stepperWW;


int main(void)
{
    // Stop WDT
    WDTCTL = WDTPW | WDTHOLD;

    // Initialize system
    initCS();
    initSysTimer();

    // Create stepper objects
    stepperHH = Stepper(hhStepperDef, ClockWise);
    stepperMM = Stepper(mmStepperDef, AntiClockWise);
    stepperWW = Stepper(wwStepperDef, ClockWise);

    // Register SMBUS map
    defineSmbusRegisterMap(stepperHH, stepperMM, stepperWW);

    // Initialize SMBus slave
    initSmbusSlave();

    // Disable High-Z GPIOs
    PM5CTL0 &= ~LOCKLPM5;

    // Enable Global Interrupts
    __bis_SR_register(GIE);

    int tmp=0;
    // Endless loop
    while(true)
    {
        // Check sysTimer event
        if(flagSysTimer == true){
            // Deassert flag
            flagSysTimer = false;

            if(tmp++<0){
                stepperHH.move();
                stepperMM.move();
                stepperWW.move();
            }else if(tmp<2000){
                stepperHH.stop();
                stepperMM.stop();
                stepperWW.stop();

            }else{
                tmp=0;
            }
        }

    }

}
