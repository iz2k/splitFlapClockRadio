#include <msp430.h>
#include <board.h>
#include <system/cs.h>
#include <system/sysTimer.h>
#include <adc/Adc.h>
#include <smbus/smbusSlave.h>
#include <splitFlap/SplitFlap.h>


void defineSmbusRegisterMap(SplitFlap*, SplitFlap*, SplitFlap*);
extern bool flagSysTimer;

int main(void)
{
    // Stop WDT
    WDTCTL = WDTPW | WDTHOLD;

    // Initialize system
    initCS();
    initSysTimer();

    // Create ADC controller
    Adc adc = Adc();

    // Create stepper objects
    SplitFlap hhSplitFlap = SplitFlap(&hhSplitFlapDef, &adc);
    SplitFlap mmSplitFlap = SplitFlap(&mmSplitFlapDef, &adc);
    SplitFlap wwSplitFlap = SplitFlap(&wwSplitFlapDef, &adc);

    // Register SMBUS map
    defineSmbusRegisterMap(&hhSplitFlap, &mmSplitFlap, &wwSplitFlap);

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

            // Enable detectors if needed
            hhSplitFlap.enableDetectorIfNeeded();
            mmSplitFlap.enableDetectorIfNeeded();
            wwSplitFlap.enableDetectorIfNeeded();

            // Wait for detection signal stabilization
            __delay_cycles(15000);

            // Run steppers
            hhSplitFlap.run();
            mmSplitFlap.run();
            wwSplitFlap.run();
        }

    }

}

void defineSmbusRegisterMap(SplitFlap *sfHH, SplitFlap *sfMM, SplitFlap *sfWW)
{
    /* FW VERSION */
    addSmbusRegister({
        .smbusAddress=0,
        .mcuAddress=(void*) &fw_version,
        .length=2});

    /* HH */
    addSmbusRegister({
        .smbusAddress=1,
        .mcuAddress=(void*) &hh_ir_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=2,
        .mcuAddress=(void*) &hh_hall_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=3,
        .mcuAddress=(void*) &hh_hall_digit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=4,
        .mcuAddress=(void*) &(*sfHH).currentDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=5,
        .mcuAddress=(void*) &(*sfHH).desiredDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=6,
        .mcuAddress=(void*) &(*sfHH).currentIR,
        .length=2});

    addSmbusRegister({
        .smbusAddress=7,
        .mcuAddress=(void*) &(*sfHH).currentHall,
        .length=2});

    addSmbusRegister({
        .smbusAddress=8,
        .mcuAddress=(void*) &(*sfHH).syncTrigger,
        .length=1});

    /* MM */
    addSmbusRegister({
        .smbusAddress=11,
        .mcuAddress=(void*) &mm_ir_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=12,
        .mcuAddress=(void*) &mm_hall_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=13,
        .mcuAddress=(void*) &mm_hall_digit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=14,
        .mcuAddress=(void*) &(*sfMM).currentDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=15,
        .mcuAddress=(void*) &(*sfMM).desiredDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=16,
        .mcuAddress=(void*) &(*sfMM).currentIR,
        .length=2});

    addSmbusRegister({
        .smbusAddress=17,
        .mcuAddress=(void*) &(*sfMM).currentHall,
        .length=2});

    addSmbusRegister({
        .smbusAddress=18,
        .mcuAddress=(void*) &(*sfMM).syncTrigger,
        .length=1});

    /* WW */
    addSmbusRegister({
        .smbusAddress=21,
        .mcuAddress=(void*) &ww_ir_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=22,
        .mcuAddress=(void*) &ww_hall_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=23,
        .mcuAddress=(void*) &ww_hall_digit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=24,
        .mcuAddress=(void*) &(*sfWW).currentDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=25,
        .mcuAddress=(void*) &(*sfWW).desiredDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=26,
        .mcuAddress=(void*) &(*sfWW).currentIR,
        .length=2});

    addSmbusRegister({
        .smbusAddress=27,
        .mcuAddress=(void*) &(*sfWW).currentHall,
        .length=2});

    addSmbusRegister({
        .smbusAddress=28,
        .mcuAddress=(void*) &(*sfWW).syncTrigger,
        .length=1});
}
