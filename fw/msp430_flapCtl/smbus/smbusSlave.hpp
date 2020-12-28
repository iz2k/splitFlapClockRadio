/*
 * i2c-slave.h
 *
 *  Created on: 24 abr. 2020
 *      Author: IbonZalbide
 */

#ifndef DRIVERS_SMBUS_SLAVE_H_
#define DRIVERS_SMBUS_SLAVE_H_

#include <stdint.h>

#define I2C_BUFFER_LENGTH 6
#define I2C_SLAVE_ADDR 0x16

typedef enum {
    SMB_NONE                = 0,
    SMB_FW_VERSION          = 1,
    SMB_HH_HALL_THRESHOLD   = 2,
    SMB_HH_HALL_DIGIT       = 3,
    SMB_HH_IR_THRESHOLD     = 4
} smbusRegMap;

typedef enum{
    SMB_OP_NONE     = 0b00000000,
    SMB_OP_READ     = 0b01000000,
    SMB_OP_WRITE    = 0b10000000,
    SMB_OP_MASK     = 0b11000000
} smbusOperation;

typedef enum i2cStateMachine{
    IDLE_MODE,
    NACK_MODE,
    TX_REG_ADDRESS_MODE,
    RX_REG_ADDRESS_MODE,
    TX_DATA_MODE,
    RX_DATA_MODE,
    SWITCH_TO_RX_MODE,
    SWITHC_TO_TX_MODE,
    TIMEOUT_MODE
} i2cStateMachine;

void initSmbusSlave();

void I2C_Slave_ProcessCMD(uint8_t cmd);
void I2C_Slave_TransactionDone(uint8_t cmd);
void CopyArray(uint8_t *source, uint8_t *dest, uint8_t count);

uint8_t *get_reg_pointer(smbusRegMap address);
uint8_t get_reg_len(smbusRegMap address);



#endif /* DRIVERS_SMBUS_SLAVE_H_ */
