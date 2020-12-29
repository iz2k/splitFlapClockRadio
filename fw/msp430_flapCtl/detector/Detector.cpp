/*
 * Detector.cpp
 *
 *  Created on: 29 dic. 2020
 *      Author: IbonZalbide
 */

#include <detector/Detector.h>

Detector::Detector()
{
    // TODO Auto-generated constructor stub

}

Detector::Detector(const DetectorDef *detectorDef, Adc* pAdc)
{
    this->enableGpo = Gpo(&detectorDef->enableGpoDef);
    this->chHall = detectorDef->chHall;
    this->chIr = detectorDef->chIr;
    this->pAdc = pAdc;
}

Detector::~Detector()
{
    // TODO Auto-generated destructor stub
}


void Detector::enable()
{
    this->enableGpo.set();
}

void Detector::disable()
{
    this->enableGpo.clear();
}

uint16_t Detector::measHall()
{
    return this->pAdc->measChannel(chHall);
}

uint16_t Detector::measIr()
{
    return this->pAdc->measChannel(chIr);
}
