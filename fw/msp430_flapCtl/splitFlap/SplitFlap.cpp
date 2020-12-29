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
    this->stepper = Stepper(&(*splitFlapDef).stepperDef);
    this->detector = Detector(&(*splitFlapDef).detectorDef, pAdc);
    this->pIrThreshold = (*splitFlapDef).pIrThreshold;
    this->pHallThreshold = (*splitFlapDef).pHallThreshold;
    this->pHallDigit = (*splitFlapDef).pHallDigit;
    this->currentDigit = 0;
    this->desiredDigit = 0;
    this->currentIR = 0;
    this->currentHall = 0;
    this->syncTrigger = 0;
    this->state = Idle;
}

SplitFlap::~SplitFlap()
{
    // TODO Auto-generated destructor stub
}

void SplitFlap::run()
{
    if (this->state != Idle){
        this->currentHall = this->detector.measHall();
        this->currentIR = this->detector.measIr();
    }
    this->detector.disable();

    switch (this->state)
    {
    case Idle:
        this->stepper.stop();
        if (this->currentDigit != this->desiredDigit){
            this->state = Move;
        }
        break;
    case Move:
        this->stepper.move();
        if (this->currentDigit == this->desiredDigit){
            this->state = Idle;
        }
        break;
    case Sync:
        break;
    }
}

void SplitFlap::enableDetectorIfNeeded()
{
    if (this->state != Idle){
        this->detector.enable();
    }
}

