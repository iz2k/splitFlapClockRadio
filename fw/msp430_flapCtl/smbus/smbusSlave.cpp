/*
 * i2c-slave.c
 *
 *  Created on: 24 abr. 2020
 *      Author: IbonZalbide
 */
#include <msp430.h>
#include <smbus/smbusSlave.hpp>
#include <smbus/smbusRegMap.hpp>


/* Used to track the state of the software state machine*/
i2cStateMachine slaveState = RX_REG_ADDRESS_MODE;
uint8_t  smbus_reg;
smbusOperation  smbus_op;

/* The Register Address/Command to use*/
uint8_t ReceiveRegAddr = 0;

/* ReceiveBuffer: Buffer used to receive data in the ISR
 * RXByteCtr: Number of bytes left to receive
 * ReceiveIndex: The index of the next byte to be received in ReceiveBuffer
 * TransmitBuffer: Buffer used to transmit data in the ISR
 * TXByteCtr: Number of bytes left to transfer
 * TransmitIndex: The index of the next byte to be transmitted in TransmitBuffer
 * */
uint8_t ReceiveBuffer[I2C_BUFFER_LENGTH] = {0};
uint8_t RXByteCtr = 0;
uint8_t ReceiveIndex = 0;
uint8_t *TransmitBuffer;
uint8_t TXByteCtr = 0;
uint8_t TransmitIndex = 0;

void initSmbusSlave()
{
    // Configure I2C GPIOs
    P1SEL0 |= BIT2 | BIT3;
    P1SEL1 &= ~(BIT2 | BIT3);

    // Configure USCI for I2C
    UCB0CTLW0 = UCSWRST;                      // Software reset enabled
    UCB0CTLW0 |= UCMODE_3 | UCSYNC;           // I2C mode, sync mode
    UCB0I2COA0 = I2C_SLAVE_ADDR | UCOAEN;         // Own Address and enable
    UCB0CTLW0 &= ~UCSWRST;                    // clear reset register
    UCB0IE |= UCRXIE + UCSTPIE;
}

/* Initialized the software state machine according to the received cmd
 *
 * cmd: The command/register address received
 * */
void I2C_Slave_ProcessCMD(uint8_t cmd)
{
    ReceiveIndex = 0;
    TransmitIndex = 0;
    RXByteCtr = 0;
    TXByteCtr = 0;

    // Extract operation from cmd
    smbusOperation op = (smbusOperation) (cmd & SMB_OP_MASK);

    // Extract addess from cmd
    uint8_t address = (cmd & ~SMB_OP_MASK);

    switch(op)
    {
    case SMB_OP_READ:
        slaveState = TX_DATA_MODE;
        TXByteCtr = getRegLength(address);
        // Fill out the TransmitBuffer
        TransmitBuffer = getRegPointer(address);
        // Switch to TX
        UCB0IE &= ~UCRXIE;
        UCB0IE |= UCTXIE;
        break;
    case SMB_OP_WRITE:
        slaveState = RX_DATA_MODE;
        RXByteCtr = getRegLength(address);
        // Switch to RX
        UCB0IE &= ~UCTXIE;
        UCB0IE |= UCRXIE;
        break;
    default:
        break;
    }

}


/* The transaction between the slave and master is completed. Uses cmd
 * to do post transaction operations. (Place data from ReceiveBuffer
 * to the corresponding buffer based in the last received cmd)
 *
 * cmd: The command/register address corresponding to the completed
 * transaction
 */
void I2C_Slave_TransactionDone(uint8_t cmd)
{
    // Extract operation from cmd
    smbusOperation op = (smbusOperation) (cmd & SMB_OP_MASK);

    // Extract addess from cmd
    uint8_t address = (cmd & ~SMB_OP_MASK);

    switch(op)
    {
    case SMB_OP_READ: // DO NOTHING FOR NOW
        break;
    case SMB_OP_WRITE: // UPDATE REGISTER
        CopyArray(ReceiveBuffer, getRegPointer(address) , getRegLength(address));
        break;
    }

    // Set SMBUS flags for main
    smbus_op=op;
    smbus_reg=address;
}

void CopyArray(uint8_t *source, uint8_t *dest, uint8_t count)
{
    uint8_t copyIndex = 0;

    // Program FRAM write enable
    SYSCFG0 = FRWPPW;
    for (copyIndex = 0; copyIndex < count; copyIndex++)
    {
        dest[copyIndex] = source[copyIndex];
    }
    // Program FRAM write protected (not writable)
    SYSCFG0 = FRWPPW | PFWP;
}

//******************************************************************************
// I2C Interrupt ***************************************************************
//******************************************************************************

#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector = USCI_B0_VECTOR
__interrupt void USCI_B0_ISR(void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(USCI_B0_VECTOR))) USCI_B0_ISR (void)
#else
#error Compiler not supported!
#endif
{
  //Must read from UCB0RXBUF
  uint8_t rx_val = 0;
  switch(__even_in_range(UCB0IV, USCI_I2C_UCBIT9IFG))
  {
    case USCI_NONE:          break;         // Vector 0: No interrupts
    case USCI_I2C_UCALIFG:   break;         // Vector 2: ALIFG
    case USCI_I2C_UCNACKIFG:                // Vector 4: NACKIFG
      break;
    case USCI_I2C_UCSTTIFG:  break;         // Vector 6: STTIFG
    case USCI_I2C_UCSTPIFG:
        UCB0IFG &= ~(UCTXIFG0);
        break;         // Vector 8: STPIFG
    case USCI_I2C_UCRXIFG3:  break;         // Vector 10: RXIFG3
    case USCI_I2C_UCTXIFG3:  break;         // Vector 12: TXIFG3
    case USCI_I2C_UCRXIFG2:  break;         // Vector 14: RXIFG2
    case USCI_I2C_UCTXIFG2:  break;         // Vector 16: TXIFG2
    case USCI_I2C_UCRXIFG1:  break;         // Vector 18: RXIFG1
    case USCI_I2C_UCTXIFG1:  break;         // Vector 20: TXIFG1
    case USCI_I2C_UCRXIFG0:                 // Vector 22: RXIFG0
        rx_val = UCB0RXBUF;
        switch (slaveState)
        {
          case (RX_REG_ADDRESS_MODE):
              ReceiveRegAddr = rx_val;
              I2C_Slave_ProcessCMD(ReceiveRegAddr);
              break;
          case (RX_DATA_MODE):
              ReceiveBuffer[ReceiveIndex++] = rx_val;
              RXByteCtr--;
              if (RXByteCtr == 0)
              {
                  //Done Receiving MSG
                  slaveState = RX_REG_ADDRESS_MODE;
                  // Switch to RX
                  UCB0IE &= ~(UCTXIE);
                  UCB0IE |= UCRXIE;
                  I2C_Slave_TransactionDone(ReceiveRegAddr);
              }
              break;
          default:
              __no_operation();
              break;
        }
        break;
    case USCI_I2C_UCTXIFG0:                 // Vector 24: TXIFG0
        switch (slaveState)
        {
          case (TX_DATA_MODE):
              UCB0TXBUF = TransmitBuffer[TransmitIndex++];
              TXByteCtr--;
              if (TXByteCtr == 0)
              {
                  //Done Transmitting MSG
                  slaveState = RX_REG_ADDRESS_MODE;
                  // Switch to RX
                  UCB0IE &= ~(UCTXIE);
                  UCB0IE |= UCRXIE;
                  I2C_Slave_TransactionDone(ReceiveRegAddr);
              }
              break;
          default:
              __no_operation();
              break;
        }
        break;                      // Interrupt Vector: I2C Mode: UCTXIFG
    default: break;
  }
}
