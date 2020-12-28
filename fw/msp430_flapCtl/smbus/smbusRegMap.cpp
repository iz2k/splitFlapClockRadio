/*
 * smbusRegMap.cpp
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */
#include <smbus/smbusRegMap.hpp>

#define MAX_SMB_REGS 32

SmbusRegister smbusRegisters[MAX_SMB_REGS];

const uint16_t  reg_fw_version = 1;
uint16_t  hh_hall_threshold = 20;
uint8_t  hh_hall_digit = 0;
uint16_t  hh_ir_threshold = 150;


void defineSmbusRegisterMap()
{
    addSmbusRegister({
        .smbusAddress=1,
        .mcuAddress=(void*) &reg_fw_version,
        .length=2});

    addSmbusRegister({
        .smbusAddress=2,
        .mcuAddress=(void*) &hh_hall_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=3,
        .mcuAddress=(void*) &hh_hall_digit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=4,
        .mcuAddress=(void*) &hh_ir_threshold,
        .length=2});
}

void addSmbusRegister(SmbusRegister smbReg)
{
    if (smbReg.smbusAddress < MAX_SMB_REGS)
    {
        smbusRegisters[smbReg.smbusAddress] = smbReg;
    }
}

uint8_t* getRegPointer(uint8_t smbAddress)
{
    if (smbAddress < MAX_SMB_REGS)
    {
        return (uint8_t*) smbusRegisters[smbAddress].mcuAddress;
    }else{
        return 0;
    }
}

uint8_t getRegLength(uint8_t smbAddress)
{
    if (smbAddress < MAX_SMB_REGS)
    {
        return smbusRegisters[smbAddress].length;
    }else{
        return 0;
    }
}

