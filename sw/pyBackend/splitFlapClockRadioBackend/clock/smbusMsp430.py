import time
from enum import Enum

import pigpio
import smbus
from termcolor import colored

from splitFlapClockRadioBackend.clock.typedef import SMBUS_OPS, MSP430_REGS
from splitFlapClockRadioBackend.tools.menuTools import getKeyFromDictionarySubitemName, select_value, doReturn, doMenu


class smbusMsp430:

    class HW(Enum):
        I2C_ADDRESS=0x16
        RST_GPIO = 12

    def __init__(self, SMBusChannel=1, i2cAddress=0x16):
        self.bus = smbus.SMBus(SMBusChannel)
        self.i2c_address = i2cAddress

        # Set HW clock to feed REFCLK
        self.pi = pigpio.pi()

        # Reset the device
        self.pi.set_mode(self.HW.RST_GPIO.value, pigpio.OUTPUT)
        self.pi.write(self.HW.RST_GPIO.value, 0)
        time.sleep(0.1)
        self.pi.write(self.HW.RST_GPIO.value, 1)
        time.sleep(0.1)
        self.pi.set_mode(self.HW.RST_GPIO.value, pigpio.INPUT)

    def read_register(self, key):
        data = self.bus.read_i2c_block_data(self.i2c_address, int(key) + SMBUS_OPS['SMB_OP_READ'], MSP430_REGS[key]['len'])
        return int.from_bytes(data, byteorder='little')

    def write_register(self, key, value):
        value_byte_array = value.to_bytes(MSP430_REGS[key]['len'], byteorder='little')
        self.bus.write_i2c_block_data(self.i2c_address, int(key) + SMBUS_OPS['SMB_OP_WRITE'], [b for b in value_byte_array])

    ####    MENU IMPLEMENTATION ####
    def menu(self, preTitle):

        menuItems = {
            'title': preTitle + ' >> MSP430',
            'options': {
                '1': {'descriptor': 'Read all registers', 'function': self.readAllRegisters},
                '2': {'descriptor': 'Write register', 'function': self.writeRegister},
                'r': {'descriptor': 'return', 'function': doReturn},
            }
        }

        # Loop on menu
        run = True
        while run:
            run = doMenu(menuItems)
        return True

    def readAllRegisters(self,preTitle):
        print(colored(preTitle + ' >> Reading all registers', 'magenta'))
        for reg in MSP430_REGS:
            print ('\t* ' + MSP430_REGS[reg]['name'] + ' = ' + self.show_reg(reg))
        return True

    def show_reg(self, reg):
        raw = self.read_register(reg)
        if MSP430_REGS[reg]['type'] is int:
            return str(raw)
        if MSP430_REGS[reg]['type'] is 'msp43xFwVersion':
            major = raw >> 8
            minor = raw & 0xFF
            return str(major) + '.' + str(minor)
        if isinstance(MSP430_REGS[reg]['type'],dict):
            return MSP430_REGS[reg]['type'][str(raw)]

    def writeRegister(self,preTitle):
        print(colored(preTitle + ' >> Writing specific register', 'magenta'))
        key = getKeyFromDictionarySubitemName(MSP430_REGS)
        if key == None:
            return True
        value = select_value(MSP430_REGS[key])
        if value == None:
            return True
        self.write_register(key, int(value))
        return True
