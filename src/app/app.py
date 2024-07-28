# App to get office environmental data

import json
import datetime
import os
import logging
import time

# import sensor data
from veml6030 import Veml6030 
from pmodhygro import PmodHygro
from pprint import pprint
import board
import adafruit_bme680

from fastapi import FastAPI

app = FastAPI()

# Init Veml6030
veml6030 = Veml6030()
veml6030.init_device()
# Init PmodHygro
pmodhygro_sensor = PmodHygro()
pmodhygro_sensor.begin_i2c()
# Init bme680
# Create sensor object, communicating over the board's default I2C bus
bme680_i2c = board.I2C()  # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(bme680_i2c, debug=False)
# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25
# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
bme680_temperature_offset = 0

@app.get("/")
def main():
    '''
    Processes the various sensor data.
    '''
    office_environment_data = dict()

    # pmodhygro data
    pmodhygro_temp                                     = pmodhygro_sensor.get_temperature()
    pmodhygro_temp_f                                   = pmodhygro_sensor.get_temperature_f()
    pmodhygro_humidity                                 = pmodhygro_sensor.get_humidity()

    office_environment_data["brightness"]              = veml6030.measure_light()
    office_environment_data["pmodhygro_temp_c"]        = pmodhygro_temp
    office_environment_data["pmodhygro_temp_f"]        = pmodhygro_temp_f
    office_environment_data["pmodhygro_humidity"]      = pmodhygro_humidity
    office_environment_data["bme680_temp_c"]           = bme680.temperature + bme680_temperature_offset
    office_environment_data["bme680_humidity"]         = bme680.relative_humidity
    office_environment_data["bme680_pressure_hpa"]     = bme680.pressure
    office_environment_data["bme680_altitude_meters"]  = bme680.altitude
    office_environment_data["bme680_gas_ohms"]         = bme680.gas
    
    pprint(office_environment_data)
    return json.dumps(office_environment_data)

if __name__ == "__main__":
    main()