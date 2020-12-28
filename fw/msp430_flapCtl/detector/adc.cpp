/*
 * adc.cpp
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */

#include <detector/adc.h>
#include <msp430.h>

Adc::Adc()
{
    this->setupGpios();
}

Adc::~Adc()
{
    // TODO Auto-generated destructor stub
}

void Adc::setupGpios()
{
    // Setup GPIOs
    P1SEL0 |= BIT0 + BIT1 + BIT4 + BIT5 + BIT6 + BIT7;
    P1SEL1 |= BIT0 + BIT1 + BIT4 + BIT5 + BIT6 + BIT7;
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
/*
    // Update CH7
    this->mm_flap = ADCMEM0;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update CH6
    this->mm_sync = ADCMEM0;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update CH5
    this->hh_flap = ADCMEM0;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update CH4
    this->hh_sync = ADCMEM0;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update CH3
    this->trash = ADCMEM0;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update CH2
    this->trash = ADCMEM0;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update CH1
    this->ww_flap = ADCMEM0;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update CH0
    this->ww_sync = ADCMEM0;
}
*/
