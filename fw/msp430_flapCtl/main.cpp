#include <msp430.h>
#include <board.hpp>
#include <detector/adc.h>
#include <smbus/smbusSlave.hpp>
#include <smbus/smbusRegMap.hpp>
#include <system/cs.hpp>
#include <system/sysTimer.hpp>
#include <stepper/stepper.hpp>
#include <detector/sensor.h>

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

    // Create ADC controller
    Adc adc = Adc();

    // Create Sensor controller
    Sensor sensor = Sensor();

    // Create stepper objects
    stepperHH = Stepper(hhStepperDef, ClockWise,
                        &hh_ir_threshold, &hh_hall_threshold, &hh_hall_digit);
    stepperMM = Stepper(mmStepperDef, AntiClockWise,
                        &mm_ir_threshold, &mm_hall_threshold, &mm_hall_digit);
    stepperWW = Stepper(wwStepperDef, ClockWise,
                        &ww_ir_threshold, &ww_hall_threshold, &ww_hall_digit);

    // Register SMBUS map
    defineSmbusRegisterMap(&stepperHH, &stepperMM, &stepperWW);

    // Initialize SMBus slave
    initSmbusSlave();

    // Disable High-Z GPIOs
    PM5CTL0 &= ~LOCKLPM5;

    // Enable Global Interrupts
    __bis_SR_register(GIE);

    // Endless loop
    while(true)
    {
        // Check sysTimer event
        if(flagSysTimer == true){
            // Deassert flag
            flagSysTimer = false;

            // Update ADC
            sensor.enableSensorAll();
            __delay_cycles(10000);
            stepperHH.updateHall(adc.measChannel(4));
            stepperHH.updateIR(adc.measChannel(5));
            stepperMM.updateHall(adc.measChannel(6));
            stepperMM.updateIR(adc.measChannel(7));
            stepperWW.updateHall(adc.measChannel(0));
            stepperWW.updateIR(adc.measChannel(1));
            sensor.disableSensorAll();

            // Run steppers
            stepperHH.run();
            stepperMM.run();
            stepperWW.run();
        }

    }

}
