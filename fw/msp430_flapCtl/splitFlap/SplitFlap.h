/*
 * SplitFlap.h
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */

#ifndef SPLITFLAP_SPLITFLAP_H_
#define SPLITFLAP_SPLITFLAP_H_
#include <adc/Adc.h>
#include <stepper/Stepper.h>
#include <gpo/Gpo.h>
#include <detector/Detector.h>

struct SplitFlapDef
{
    StepperDef stepperDef;
    DetectorDef detectorDef;
    uint16_t *pIrThreshold;
    uint16_t *pHallThreshold;
    uint8_t *pHallDigit;
    uint16_t *pDebounce;
    uint8_t maxDigit;
};

typedef enum {
    Idle,
    Move,
    Sync
} SplitFlapState;

class SplitFlap
{
public:
    // Properties
    uint16_t *pIrThreshold;
    uint16_t *pHallThreshold;
    uint8_t *pHallDigit;
    uint16_t *pDebounce;
    uint8_t currentDigit;
    uint8_t desiredDigit;
    uint16_t currentIR;
    uint16_t currentHall;
    uint16_t maxHall;
    uint8_t syncTrigger;

    // Methods
    SplitFlap();
    SplitFlap(const SplitFlapDef*, Adc*);
    virtual ~SplitFlap();
    void run();
    void enableDetectorIfNeeded();

private:
    Stepper stepper;
    Detector detector;
    SplitFlapState state;
    uint8_t maxDigit;
    bool debounceInCurse;
    uint16_t debounceCounter;
    bool syncDone;
    bool syncFound;

    uint16_t filter(uint16_t, uint16_t, float);
};

#endif /* SPLITFLAP_SPLITFLAP_H_ */
