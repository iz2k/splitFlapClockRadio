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
}

SplitFlap::~SplitFlap()
{
    // TODO Auto-generated destructor stub
}

void SplitFlap::run()
{
    //this->stepper.move();
    this->currentHall = this->detector.measHall();
    this->currentIR = this->detector.measIr();
    this->detector.disable();
}

void SplitFlap::enableDetectorIfNeeded()
{
    this->detector.enable();
}

