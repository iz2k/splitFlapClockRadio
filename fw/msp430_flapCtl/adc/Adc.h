/*
 * adc.h
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */

#ifndef DETECTOR_ADC_H_
#define DETECTOR_ADC_H_
#include <stdint.h>

class Adc
{
public:
    // Methods
    Adc();
    virtual ~Adc();
    uint16_t measChannel(uint8_t channel);
};

#endif /* DETECTOR_ADC_H_ */
