/*
 * adc.cpp
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */

#include <adc/Adc.h>
#include <msp430.h>

Adc::Adc()
{

}

Adc::~Adc()
{
    // TODO Auto-generated destructor stub
}


uint16_t Adc::measChannel(uint8_t channel)
{
    // Configure ADC12
    ADCCTL0 &= ~ADCENC;          // Reset configuration
    ADCCTL0 = ADCSHT_2 | ADCON;  // 16ADCclks, ADC ON
    ADCCTL1 = ADCSHP;            // ADCCLK = MODOSC; sampling timer
    ADCCTL2 &= ~ADCRES;          // clear ADCRES in ADCCTL
    ADCCTL2 |= ADCRES_2;         // 12-bit conversion results
    ADCMCTL0 = channel;          // (channel) ADC input select; Vref=DVCC

    // Wait if ADC core is active
    while(ADCCTL1 & ADCBUSY);
    // Sampling and conversion start
    ADCCTL0 |= ADCENC | ADCSC;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    return ADCMEM0;
}
