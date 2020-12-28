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


void defineSmbusRegisterMap(Stepper *stpHH, Stepper *stpMM, Stepper *stpWW)
{
    /* FW VERSION */
    addSmbusRegister({
        .smbusAddress=0,
        .mcuAddress=(void*) &fw_version,
        .length=2});

    /* HH */
    addSmbusRegister({
        .smbusAddress=1,
        .mcuAddress=(void*) &hh_ir_threshold,
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
        .mcuAddress=(void*) &(*stpHH).currentDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=5,
        .mcuAddress=(void*) &(*stpHH).desiredDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=6,
        .mcuAddress=(void*) &(*stpHH).currentIR,
        .length=2});

    addSmbusRegister({
        .smbusAddress=7,
        .mcuAddress=(void*) &(*stpHH).currentHall,
        .length=2});

    addSmbusRegister({
        .smbusAddress=8,
        .mcuAddress=(void*) &(*stpHH).syncTrigger,
        .length=1});

    /* MM */
    addSmbusRegister({
        .smbusAddress=11,
        .mcuAddress=(void*) &mm_ir_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=12,
        .mcuAddress=(void*) &mm_hall_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=13,
        .mcuAddress=(void*) &mm_hall_digit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=14,
        .mcuAddress=(void*) &(*stpMM).currentDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=15,
        .mcuAddress=(void*) &(*stpMM).desiredDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=16,
        .mcuAddress=(void*) &(*stpMM).currentIR,
        .length=2});

    addSmbusRegister({
        .smbusAddress=17,
        .mcuAddress=(void*) &(*stpMM).currentHall,
        .length=2});

    addSmbusRegister({
        .smbusAddress=18,
        .mcuAddress=(void*) &(*stpMM).syncTrigger,
        .length=1});

    /* WW */
    addSmbusRegister({
        .smbusAddress=21,
        .mcuAddress=(void*) &ww_ir_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=22,
        .mcuAddress=(void*) &ww_hall_threshold,
        .length=2});

    addSmbusRegister({
        .smbusAddress=23,
        .mcuAddress=(void*) &ww_hall_digit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=24,
        .mcuAddress=(void*) &(*stpWW).currentDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=25,
        .mcuAddress=(void*) &(*stpWW).desiredDigit,
        .length=1});

    addSmbusRegister({
        .smbusAddress=26,
        .mcuAddress=(void*) &(*stpWW).currentIR,
        .length=2});

    addSmbusRegister({
        .smbusAddress=27,
        .mcuAddress=(void*) &(*stpWW).currentHall,
        .length=2});

    addSmbusRegister({
        .smbusAddress=28,
        .mcuAddress=(void*) &(*stpWW).syncTrigger,
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

