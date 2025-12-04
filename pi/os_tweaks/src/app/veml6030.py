# veml6030.py
#from typing import Any
from smbus2 import SMBus
import time
import logging
from pprint import pprint

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Veml6030:
    """
    Gets data from the veml6030 light sensor over i2c
    https://www.vishay.com/docs/84366/veml6030.pdf
    """
    # manual tests with i2c tools on the cli
    # i2cset -y 1 0x48 0x02 0x00
    # i2cget -y 1 0x48 0x02
    # i2cset -y 1 0x48 0x02 0x3E80
    # i2cset -y 1 0x48 0x02 0x3E80 w
    # i2cget -y 1 0x48 0x04 w
    __author__ = "Dan Ackerman"
    __version__ = "0.1.0"
    __license__ = "MIT"

    # I2C address of the VEML6030 sensor
    #I2C_ADDR = 0x10  # could be either.
    I2C_ADDR = 0x48
    I2C_BUS = 1

    # Register addresses
    # See: https://learn.sparkfun.com/tutorials/qwiic-ambient-light-sensor-veml6030-hookup-guide/all#hardware-overview
    # https://www.vishay.com/docs/84366/veml6030.pdf

    ALS_CONF = 0x00
    ALS_WH = 0x01
    ALS_WL = 0x02
    POWER_SAVE_MODE = 0x03
    ALS = 0x04
    # TABLE 1 - CONFIGURATION REGISTER #0
    # | REGISTER_NAME | BIT     | FUNCTION / DESCRIPTION                 | R / W |
    # | Reserved      | 15:13   | Set 000b                               | R / W |
    # | ALS_GAIN      | 12 : 11 | Gain selection                         | R / W |
    #                             00 = ALS gain x 1
    #                             01 = ALS gain x 2
    #                             10 = ALS gain x (1/8)
    #                             11 = ALS gain x (1/4)
    # | reserved      | 10      | Set 0b                                 | R / W |
    # | ALS_IT        | 9 : 6   | ALS integration time setting           | R / W |
    #                             1100 = 25 ms
    #                             1000 = 50 ms
    #                             0000 = 100 ms
    #                             0001 = 200 ms
    #                             0010 = 400 ms
    #                             0011 = 800 ms
    # | ALS_PERS      | 5 : 4   | ALS persistence protect number setting | R / W |
    #                             00 = 1
    #                             01 = 2
    #                             10 = 4
    #                             11 = 8
    # | Reserved      | 3 : 2   | Set 00b                                | R / W |
    # | ALS_INT_EN    | 1       | ALS interrupt enable setting           | R / W |
    #                             0 = ALS INT disable
    #                             1 = ALS INT enable
    # | ALS_SD        | 0       | ALS shut down setting                  | R / W |
    #                             0 = ALS power on
    #                             1 = ALS shut down
    CONFIG = 0b0001100000000000
    LUX_TO_BIT_MULTIPLIER = 0.2304 #https://learn.sparkfun.com/tutorials/qwiic-ambient-light-sensor-veml6030-hookup-guide#example-2-and-3-ambient-light-interrupt

    
    def __init__(self):
        """initialize variables of sensor data"""
        logging.debug("Init VEML6030 Module")
        # print("Init VEML6030 Module")
        self.i2cbus_address = self.I2C_BUS
        self.veml6030_address = self.I2C_ADDR
        self.i2cbus = SMBus(self.i2cbus_address) # create a new I2C bus
        time.sleep(0.020)       # Wait 20ms for i2c bus
        self.init_device()
        
    def init_device(self):
        logging.debug("Init VEML6030 device")
        self.i2cbus.write_byte_data(self.veml6030_address,self.ALS_CONF,0x00)
        self.i2cbus.write_word_data(self.veml6030_address,self.ALS_WL,self.CONFIG)
        time.sleep(0.020)       # Wait 20ms for i2c bus

    def measure_light(self):
        """Outputs the brighness in lumens"""
        logging.debug("Measuring Light")
        raw_bits = self.i2cbus.read_word_data(self.I2C_ADDR, self.ALS)
        logging.debug(f"raw_bits: {raw_bits}")
        return raw_bits * self.LUX_TO_BIT_MULTIPLIER

if __name__ == "__main__":
    sensor = Veml6030()
    sensor.init_device()
    lux_from_sensor = sensor.measure_light()
    print("{:0.2f} lux".format(lux_from_sensor))
