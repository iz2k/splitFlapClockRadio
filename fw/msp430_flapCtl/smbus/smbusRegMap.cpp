/*
 * smbusRegMap.cpp
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */
#include <smbus/smbusRegMap.hpp>
#include <stepper/stepper.hpp>
#include <nvm/nvm.hpp>

#define MAX_SMB_REGS 32

SmbusRegister smbusRegisters[MAX_SMB_REGS];


void defineSmbusRegisterMap(Stepper stpHH, Stepper stpMM, Stepper stpWW)
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

    addSmbusRegister({
        .smbusAddress=5,
        .mcuAddress=(void*) &stpHH.currentDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=6,
        .mcuAddress=(void*) &stpHH.desiredDigit,
        .length=1});
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

