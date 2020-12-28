/*
 * Sensor.cpp
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */

#include <msp430.h>
#include <detector/sensor.h>

Sensor::Sensor()
{
    P2DIR |= BIT0 + BIT4;
    P3DIR |= BIT0;
}

Sensor::~Sensor()
{
    // TODO Auto-generated destructor stub
}

void Sensor::enableSensorAll()
{
    this->enableSensorHH();
    this->enableSensorMM();
    this->enableSensorWW();
}

void Sensor::disableSensorAll()
{
    this->disableSensorHH();
    this->disableSensorMM();
    this->disableSensorWW();
}

void Sensor::enableSensorHH()
{
    P2OUT |= BIT0;
}

void Sensor::disableSensorHH()
{
    P2OUT &= ~BIT0;
}

void Sensor::enableSensorMM()
{
    P2OUT |= BIT4;
}

void Sensor::disableSensorMM()
{
    P2OUT &= ~BIT4;
}

void Sensor::enableSensorWW()
{
    P3OUT |= BIT0;
}

void Sensor::disableSensorWW()
{
    P3OUT &= ~BIT0;
}

