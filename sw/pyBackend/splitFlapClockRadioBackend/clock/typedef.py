
MSP430_REGS = {
    '1': {'name': 'FW_VERSION', 'type': 'msp43xFwVersion', 'len' : 2},
    '2': {'name': 'HH_HALL_THRESHOLD', 'type': int, 'len' : 2},
    '3': {'name': 'HH_HALL_DIGIT', 'type': int, 'len' : 1},
    '4': {'name': 'HH_IR_THRESHOLD', 'type': int, 'len' : 2}
}


SMBUS_OPS = {
    'SMB_OP_NONE': 0b00000000,
    'SMB_OP_READ': 0b01000000,
    'SMB_OP_WRITE': 0b10000000,
    'SMB_OP_MASK': 0b11000000
}
