/*
 * smbusRegMap.hpp
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */

#ifndef SMBUS_SMBUSREGMAP_HPP_
#define SMBUS_SMBUSREGMAP_HPP_

#include <stdint.h>
#include <stepper/stepper.hpp>

struct SmbusRegister
{
    uint8_t smbusAddress;
    void * mcuAddress;
    uint8_t length;
};


void defineSmbusRegisterMap(Stepper*, Stepper*, Stepper*);

void addSmbusRegister(SmbusRegister);

uint8_t* getRegPointer(uint8_t);
uint8_t getRegLength(uint8_t);


#endif /* SMBUS_SMBUSREGMAP_HPP_ */
