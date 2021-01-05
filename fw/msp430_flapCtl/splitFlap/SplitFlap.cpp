/*
 * SplitFlap.cpp
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */

#include <splitFlap/SplitFlap.h>

SplitFlap::SplitFlap()
{
    // TODO Auto-generated constructor stub

}

SplitFlap::SplitFlap(const SplitFlapDef *splitFlapDef, Adc *pAdc)
{
    this->stepper = Stepper(&splitFlapDef->stepperDef);
    this->detector = Detector(&splitFlapDef->detectorDef, pAdc);
    this->pIrThreshold = splitFlapDef->pIrThreshold;
    this->pHallThreshold = splitFlapDef->pHallThreshold;
    this->pHallDigit = splitFlapDef->pHallDigit;
    this->pDebounce = splitFlapDef->pDebounce;
    this->maxDigit = splitFlapDef->maxDigit;
    this->currentDigit = 0;
    this->desiredDigit = 0;
    this->currentIR = 0;
    this->currentHall = 0;
    this->maxHall = 0;
    this->debounceInCurse = false;
    this->debounceCounter = 0;
    this->syncFound = true;
    this->syncDone = false;
    this->state = Idle;
    this->syncTrigger = 1;
}

SplitFlap::~SplitFlap()
{
    // TODO Auto-generated destructor stub
}

void SplitFlap::run()
{
    // Check sync trigger
    if (this->syncTrigger == 1)
    {
        this->syncTrigger = 2;
        this->state = Sync;
        this->syncDone = false;
        this->detector.enable();
        this->desiredDigit = *this->pHallDigit;
    }

    // Analyze sensor values
    if (this->state != Idle){
        this->currentHall = this->filter(this->currentHall, this->detector.measHall(), 0.1);
        this->currentIR = this->detector.measIr();

        // Check IR sensor to count falling flaps
        if(this->debounceInCurse == false)
        {
            if (this->currentIR > *this->pIrThreshold)
            {
                this->currentDigit++;
                if (this->currentDigit > this->maxDigit)
                {
                    this->currentDigit = 0;
                }
                this->debounceInCurse = true;
                this->debounceCounter = 0;
            }
        }else{
            if (++this->debounceCounter > *this->pDebounce)
            {
                this->debounceInCurse = false;
            }
        }


        // Check Hall sensor to check sync magnet
        if ((this->currentHall + *this->pHallThreshold) < this->maxHall)
        {
            if (this->syncFound == false)
            {
                this->syncFound = true;
                if (this->syncDone == false)
                {
                    this->syncDone = true;
                    this->currentDigit = *this->pHallDigit;
                }
            }
        }
        // Update maximum Hall value
        if(this->currentHall > this->maxHall)
        {
            this->maxHall = this->currentHall;
        }

        // Reset sync found flag when magnet far away
        if (this->currentHall == 0)
        {
            this->syncFound = false;
            this->syncDone = false;
            this->maxHall = 0;
        }

    }

    // Control stepper depending on state
    switch (this->state)
    {
    case Idle:
        this->stepper.stop();
        if (this->currentDigit != this->desiredDigit){
            this->state = Move;
            this->detector.enable();
        }
        break;
    case Move:
        if(this->debounceInCurse == false)
        {
            this->stepper.move();
        }
        if (this->currentDigit == this->desiredDigit){
            this->state = Idle;
            this->detector.disable();
        }
        break;
    case Sync:
        if (this->syncDone == false)
        {
            this->stepper.move();
        }else{
            this->state = Idle;
            this->syncTrigger = 0;
        }
        break;
    }
}

void SplitFlap::enableDetectorIfNeeded()
{
    if (this->state != Idle){
        this->detector.enable();
    }
}

uint16_t SplitFlap::filter(uint16_t oldval, uint16_t newval, float speed)
{
    return oldval*(1-speed)+ newval*speed;
}
