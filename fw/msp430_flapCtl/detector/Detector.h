/*
 * Detector.h
 *
 *  Created on: 29 dic. 2020
 *      Author: IbonZalbide
 */

#ifndef DETECTOR_DETECTOR_H_
#define DETECTOR_DETECTOR_H_

#include <gpo/Gpo.h>
#include <adc/Adc.h>

struct DetectorDef
{
    GpoDef enableGpoDef;
    uint8_t chHall;
    uint8_t chIr;
};

class Detector
{
public:
    Detector();
    Detector(const DetectorDef*, Adc*);
    virtual ~Detector();
    void enable();
    void disable();
    uint16_t measHall();
    uint16_t measIr();
private:
    Adc *pAdc;
    Gpo enableGpo;
    uint8_t chHall;
    uint8_t chIr;
};

#endif /* DETECTOR_DETECTOR_H_ */
