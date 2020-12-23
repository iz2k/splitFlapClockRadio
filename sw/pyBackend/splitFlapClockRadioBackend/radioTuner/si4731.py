import subprocess

import pigpio
import smbus2
import time
import logging
from enum import Enum
from .rds import RDS
from ..tools.osTools import start_service, stop_service


class Si4731:

    class HW(Enum):
        I2C_ADDRESS=0x63 # 0x63 (/SEN=1) or 0x11 (/SEN=0)
        RST_GPIO = 26
        SEN_GPIO = 16
        RECLK_GPIO = 4
        REFCLK_FREQ = 32768

    class CMDSET(Enum):
        POWER_UP=0x01
        GET_REV=0x10
        POWER_DOWN=0x11
        SET_PROPERTY=0x12
        GET_PROPERTY=0x13
        GET_INT_STATUS=0x14
        FM_TUNE_FREQ=0x20
        FM_SEEK_START=0x21
        FM_TUNE_STATUS=0x22
        FM_RSQ_STATUS=0x23
        GET_RDS_STATUS=0x24

    class PROPS(Enum):
        REFCLK_FREQ = 0x0201
        REFCLK_PRESCALE = 0x0202
        DIGITAL_OUTPUT_SAMPLE_RATE = 0x0104
        DIGITAL_OUTPUT_FORMAT = 0x0102
        RX_VOLUME = 0x4000
        FM_RDS_INT_SOURCE = 0x1500
        FM_RDS_INT_FIFO_COUNT = 0x1501
        FM_RDS_CONFIG = 0x1502

    class RFMODE(Enum):
        LW = 0
        AM = 1
        SW = 2
        FM = 3

    class OUTMODE(Enum):
        RDS=0x00  # RDS only
        ANALOG=0x05
        DIGITAL1=0x0B # DCLK, LOUT/DFS, ROUT/DIO
        DIGITAL2=0xB0 # DCLK, DFS, DIO
        BOTH=(ANALOG | DIGITAL2)
        BITWIDTH24 = 0x0002

    class SEEKMODE(Enum):
        UD_UP=8
        UD_DOWN=0
        WH_WRAP=4
        WH_HALT=0

    class FLAGS(Enum):
        CTS = 0x80
        ERR = 0x40
        STCINT = 0x01
        INTACK = 0x01
        RDSINT = 0x04

    class FM_RDS_FLAGS(Enum):
        RDSRECV = 0x0001
        NOERRORS = 0xAA01

    class STATION_INFO():
        Valid = False
        Frequency = None
        RSSI = None
        SNR = None
        Pilot = None
        Stblend = None
        Multipath = None
        Freq_offset = None

    def __init__(self):
        self.create_logger()
        self.init_hw()
        self.init_radio()
        self.turn(False)
        self.station = self.STATION_INFO()
        self.rds = RDS()

    # Deleting (Calling destructor)
    def __del__(self):
        self.turn(False)

    def create_logger(self):
        # create logger
        self.logger = logging.getLogger('Si4731')
        #self.logger.setLevel(logging.DEBUG)
        self.logger.setLevel(logging.NOTSET)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        self.logger.addHandler(ch)

    def init_hw(self):
        # Set HW clock to feed REFCLK
        self.pi = pigpio.pi()

        # Reset the device
        self.pi.set_mode(self.HW.RST_GPIO.value, pigpio.OUTPUT)
        self.pi.set_mode(self.HW.SEN_GPIO.value, pigpio.OUTPUT)
        self.pi.write(self.HW.RST_GPIO.value, 0)
        self.pi.write(self.HW.SEN_GPIO.value, 1)
        self.logger.debug("RST adn SEN GPIOs initialized.")

        self.pi.hardware_clock(self.HW.RECLK_GPIO.value, self.HW.REFCLK_FREQ.value)
        self.logger.debug("REFCLK enabled @" + str(self.HW.REFCLK_FREQ.value) + 'Hz')

        # Wait to ensure reset of device
        time.sleep(0.1)

        # Set /RST high
        self.pi.write(self.HW.RST_GPIO.value, 1)
        self.logger.debug("Device Reset!")

        # Wait to ensure reset of device
        time.sleep(0.1)

        # Initialize i2c communication
        self.i2c = smbus2.SMBus(1)
        self.logger.debug("I2C bus open")

    def write_cmd(self, cmd, args):
        try:
            # Wait Clear To Send flag
            self.wait_cts()
            # Write command and arguments to i2c bus
            self.i2c.write_i2c_block_data(self.HW.I2C_ADDRESS.value, cmd.value, args)
            #self.logger.debug("Command sent: " + cmd.name + ", arguments: " + str(args))
        except:
            pass

    def read_cmd(self, cmd, nbytes):
        try:
            # Wait Clear To Send flag
            self.wait_cts()
            # Write command and read data from i2c bus
            return self.i2c.read_i2c_block_data(self.HW.I2C_ADDRESS.value, cmd.value, nbytes)
        except:
            pass

    def write_read_cmd(self, cmd, write, nread):
        try:
            # Write command and ACK INT
            wr=[cmd.value]
            wr.extend(write)
            write = smbus2.i2c_msg.write(self.HW.I2C_ADDRESS.value, wr)
            # Read status
            read = smbus2.i2c_msg.read(self.HW.I2C_ADDRESS.value, nread)
            # Execute I2C operation
            self.i2c.i2c_rdwr(write, read)
            # Convert response to list
            return list(read)
        except:
            pass


    def get_status(self):
        try:
            return self.i2c.read_byte(self.HW.I2C_ADDRESS.value)
        except:
            pass

    def wait_cts(self):
        try:
            while not self.get_status() & self.FLAGS.CTS.value:
                time.sleep(0.01)
        except:
            pass

    def get_int_status(self, intFlag):
        try:
            self.write_cmd(self.CMDSET.GET_INT_STATUS, [])
            if self.get_status() & intFlag.value:
                return True
            else:
                return False
        except:
            pass

    def wait_int(self, interruptType):
        try:
            #self.logger.debug("Waiting for " + interruptType.name + " interrupt...")
            while not self.get_int_status(interruptType):
                time.sleep(0.001)
        except:
            pass

    def power_up(self, outmode):
        try:
            # Create POWER_UP command
            cmd = self.CMDSET.POWER_UP
            args = [0x00]
            args.extend(outmode.value.to_bytes(1, byteorder='big'))
            # Send command
            self.write_cmd(cmd, args)
            self.logger.debug("Command sent: " + cmd.name + " with OUTMODE: " + outmode.name + " | " + str(args))
        except:
            pass

    def get_revision(self):
        try:
            # Send command
            resp=self.read_cmd(self.CMDSET.GET_REV, 9)
            partnumber = 'Si47' + str(resp[1])
            firmware = chr(resp[2]) + '.' + chr(resp[3])
            compfirmware = chr(resp[6]) + '.' + chr(resp[7])
            chiprev = chr(resp[8])
            self.logger.debug('Part Number: ' + partnumber)
            self.logger.debug('Firmware Revision: ' + firmware)
            self.logger.debug('Component Firmware Revision: ' + compfirmware)
            self.logger.debug('Chip Revision: ' + chiprev)
        except:
            pass

    def write_property(self, prop, val):
        try:
            # Create SET_PROPERTY command
            cmd = self.CMDSET.SET_PROPERTY
            args = [0x00]
            args.extend(prop.value.to_bytes(2, byteorder='big'))
            args.extend(val.to_bytes(2, byteorder='big'))
            # Send command
            self.write_cmd(cmd, args)
            self.logger.debug("Command sent: " + cmd.name + " with PROPERTY: " + prop.name + " and VALUE: " + str(val) + " | " + str(args))
        except:
            pass

    def init_radio(self):
        try:
            # POWER ON
            self.power_up(self.OUTMODE.BOTH)
            # Get silicon revision
            self.get_revision()
            # REFCLK_FREQ
            self.write_property(self.PROPS.REFCLK_FREQ, self.HW.REFCLK_FREQ.value)
            # REFCLK_PRESCALE
            self.write_property(self.PROPS.REFCLK_PRESCALE, 1)
            # I2S output mode
            self.write_property(self.PROPS.DIGITAL_OUTPUT_FORMAT, self.OUTMODE.BITWIDTH24.value)
            # Sample rate 48000
            self.write_property(self.PROPS.DIGITAL_OUTPUT_SAMPLE_RATE, 48000)
            # Configure RDS interrupt source
            self.write_property(self.PROPS.FM_RDS_INT_SOURCE, self.FM_RDS_FLAGS.RDSRECV.value)
            # Set minimum RDS data for interrupt
            self.write_property(self.PROPS.FM_RDS_INT_FIFO_COUNT, 4)
            # Set accepted RDS data
            self.write_property(self.PROPS.FM_RDS_CONFIG, self.FM_RDS_FLAGS.NOERRORS.value)
        except:
            pass

    def set_volume(self, vol):
        try:
            # Volume value goes from 0 to 63
            if 0 <= vol <= 63:
                self.logger.debug("Setting volume to " + str(vol) + " ("+str(int(vol*100/63))+"%)")
                self.write_property(self.PROPS.RX_VOLUME, vol)
            else:
                self.logger.warning("Volume out of range. Please set a value between 0 and 63")
        except:
            pass

    def turn(self, onoff):
        try:
            self.on = onoff
            # Volume value goes from 0 to 63
            if onoff == True:
                self.set_volume(63)
            else:
                self.set_volume(0)
        except:
            pass

    def fm_tune(self, freq_MHz):
        try:
            # Create FM_TUNE_FREQ command
            cmd = self.CMDSET.FM_TUNE_FREQ
            args = [0x00]
            args.extend(int((freq_MHz*100)).to_bytes(2, byteorder='big'))
            args.extend([0x00, 0x00])
            # Send command
            self.write_cmd(cmd, args)
            self.logger.debug("Command sent: " + cmd.name + " with FREQUENCY: " + str(freq_MHz) + " | " + str(args))
            self.wait_tune_done()
        except:
            pass

    def fm_seek_up(self):
        try:
            # Create FM_TUNE_FREQ command
            cmd = self.CMDSET.FM_SEEK_START
            args = [self.SEEKMODE.UD_UP.value + self.SEEKMODE.WH_WRAP.value]
            # Send command
            self.write_cmd(cmd, args)
            self.logger.debug("Command sent: " + cmd.name + " | " + str(args))
            self.wait_tune_done()
        except:
            pass

    def fm_seek_down(self):
        try:
            # Create FM_TUNE_FREQ command
            cmd = self.CMDSET.FM_SEEK_START
            args = [self.SEEKMODE.UD_DOWN.value + self.SEEKMODE.WH_WRAP.value]
            # Send command
            self.write_cmd(cmd, args)
            self.logger.debug("Command sent: " + cmd.name + " | " + str(args))
            self.wait_tune_done()
        except:
            pass

    def wait_tune_done(self):
        try:
            # Reset RDS data
            self.rds.reset()
            # Wait TUNE DONE interrupt
            self.wait_int(self.FLAGS.INTACK)
            self.logger.debug("Tuning done!")
            # ACK Interrupt and read status
            self.get_tune_status()
        except:
            pass

    def get_tune_status(self):
        try:
            # Send FM_TUNE_STATUS command, ACK INT, and read 8 bytes
            resp=self.write_read_cmd(self.CMDSET.FM_TUNE_STATUS, [self.FLAGS.INTACK.value], 8)

            # Process response
            self.station.Valid = resp[1] & 0x01
            self.station.Frequency = ((resp[2]<<8) | resp[3])/100
            self.station.RSSI = resp[4]
            self.station.SNR = resp[5]
            self.station.Multipath = resp[6]

            # Print info
            self.logger.debug('Valid freq.: ' + str(self.station.Valid))
            self.logger.debug('Fequency: ' + str(self.station.Frequency))
            self.logger.debug('RSSI: ' + str(self.station.RSSI))
            self.logger.debug('SNR: ' + str(self.station.SNR))
            self.logger.debug('Multipath: ' + str(self.station.Multipath))
        except:
            pass


    def get_rsq_status(self):
        try:
            # Send FM_TUNE_STATUS command, ACK INT, and read 8 bytes
            resp=self.write_read_cmd(self.CMDSET.FM_RSQ_STATUS, [0], 8)

            # Process response
            self.station.Valid = resp[2] & 0x01
            self.station.Pilot = (resp[3] & 0x80) >> 7
            self.station.Stblend = resp[3] & 0x7F
            self.station.RSSI = resp[4]
            self.station.SNR = resp[5]
            self.station.Multipath = resp[6]
            self.station.Freq_offset = resp[7]

            # Print info
            self.logger.debug('Valid freq.: ' + str(self.station.Valid))
            self.logger.debug('Pilot: ' + str(self.station.Pilot))
            self.logger.debug('Stereo Blend: ' + str(self.station.Stblend))
            self.logger.debug('RSSI: ' + str(self.station.RSSI))
            self.logger.debug('SNR: ' + str(self.station.SNR))
            self.logger.debug('Multipath: ' + str(self.station.Multipath))
            self.logger.debug('Freq. offset: ' + str(self.station.Freq_offset))
        except:
            pass

    def wait_rds(self):
        try:
            self.wait_int(self.FLAGS.RDSINT)
        except:
            pass

    def check_rds(self):
        try:
            return self.get_int_status(self.FLAGS.RDSINT)
        except:
            pass

    def get_rds_status(self):
        try:
            # Send GET_RDS_STATUS command, ACK INT, and read 8 bytes
            resp=self.write_read_cmd(self.CMDSET.GET_RDS_STATUS, [self.FLAGS.INTACK.value], 13)
            fifoused=resp[3]
            blocka=resp[4]*256 + resp[5]
            blockb=resp[6]*256 + resp[7]
            blockc=resp[8]*256 + resp[9]
            blockd=resp[10]*256 + resp[11]
            self.rds.process_rds_blocks(blocka, blockb, blockc, blockd)
        except:
            pass
    def get_info_obj(self):
        obj = {
            'freq' : self.station.Frequency,
            'SNR' : self.station.SNR,
            'RSSI' : self.station.RSSI,
            'PS' : self.rds.PS.string,
            'RadioTextA' : self.rds.RadioTextA.string,
            'on' : self.on
        }
        return obj



