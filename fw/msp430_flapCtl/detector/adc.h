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
    // Members
    uint16_t hh_flap;
    uint16_t hh_sync;
    uint16_t mm_flap;
    uint16_t mm_sync;
    uint16_t ww_flap;
    uint16_t ww_sync;

    // Methods
    Adc();
    virtual ~Adc();
    uint16_t measChannel(uint8_t channel);
private:
    void setupGpios();
    uint16_t trash;
};

#endif /* DETECTOR_ADC_H_ */
