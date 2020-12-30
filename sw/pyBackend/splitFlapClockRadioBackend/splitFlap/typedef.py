
MSP430_REGS = {
    '0': {'name': 'fw_version', 'type': 'msp43xFwVersion', 'len' : 2},
    '1': {'name': 'hh_ir_threshold', 'type': int, 'len' : 2},
    '2': {'name': 'hh_hall_threshold', 'type': int, 'len' : 2},
    '3': {'name': 'hh_hall_digit', 'type': int, 'len' : 1},
    '4': {'name': 'hh_current_digit', 'type': int, 'len' : 1},
    '5': {'name': 'hh_desired_digit', 'type': int, 'len' : 1},
    '6': {'name': 'hh_current_ir', 'type': int, 'len' : 2},
    '7': {'name': 'hh_current_hall', 'type': int, 'len' : 2},
    '8': {'name': 'hh_sync_trigger', 'type': int, 'len' : 1},
    '11': {'name': 'mm_ir_threshold', 'type': int, 'len' : 2},
    '12': {'name': 'mm_hall_threshold', 'type': int, 'len' : 2},
    '13': {'name': 'mm_hall_digit', 'type': int, 'len' : 1},
    '14': {'name': 'mm_current_digit', 'type': int, 'len' : 1},
    '15': {'name': 'mm_desired_digit', 'type': int, 'len' : 1},
    '16': {'name': 'mm_current_ir', 'type': int, 'len' : 2},
    '17': {'name': 'mm_current_hall', 'type': int, 'len' : 2},
    '18': {'name': 'mm_sync_trigger', 'type': int, 'len' : 1},
    '21': {'name': 'ww_ir_threshold', 'type': int, 'len' : 2},
    '22': {'name': 'ww_hall_threshold', 'type': int, 'len' : 2},
    '23': {'name': 'ww_hall_digit', 'type': int, 'len' : 1},
    '24': {'name': 'ww_current_digit', 'type': int, 'len' : 1},
    '25': {'name': 'ww_desired_digit', 'type': int, 'len' : 1},
    '26': {'name': 'ww_current_ir', 'type': int, 'len' : 2},
    '27': {'name': 'ww_current_hall', 'type': int, 'len' : 2},
    '28': {'name': 'ww_sync_trigger', 'type': int, 'len' : 1}
}


SMBUS_OPS = {
    'SMB_OP_NONE': 0b00000000,
    'SMB_OP_READ': 0b01000000,
    'SMB_OP_WRITE': 0b10000000,
    'SMB_OP_MASK': 0b11000000
}
