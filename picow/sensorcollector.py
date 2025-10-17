# App to get office environmental data, pico wh edition.
import machine
from machine import I2C
from machine import Pin

import json 
# import sensor libaries
from veml6030 import Veml6030
import bme680
import sgp40

# hardware config
I2C_BUS = 0
I2C_SDA_PIN = 8
I2C_SCL_PIN = 9




def main():
    i2c = I2C(I2C_BUS, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400_000)
    devices = i2c.scan()
    if devices is None:
        raise "No i2c devices found on bus!  Have you connected the correct pins?"
    else:
        print(devices)
    
    office_environment_data = dict()

    # Init Veml6030
    veml6030 = Veml6030(i2c)
    #light_in_lux = veml6030.measure_light()
    #print("light lux: ", light_in_lux)
    office_environment_data["brightness"]              = veml6030.measure_light()
    # Init bme680
    bme680_sensor = bme680.BME680_I2C(i2c)
    # You will usually have to add an offset to account for the temperature of
    # the sensor. This is usually around 5 degrees but varies by use. Use a
    # separate temperature sensor to calibrate this one.
    bme680_temperature_offset = 0
    # change this to match the location's pressure (hPa) at sea level
    bme680.sea_level_pressure = 1013.25
    #print(dir(bme680_sensor))
    office_environment_data["bme680_temp_c"]           = bme680_sensor.temperature + bme680_temperature_offset
    office_environment_data["bme680_humidity"]         = bme680_sensor.humidity
    office_environment_data["bme680_pressure_hpa"]     = bme680_sensor.pressure
    office_environment_data["bme680_altitude_meters"]  = bme680_sensor.altitude
    office_environment_data["bme680_gas_ohms"]         = bme680_sensor.gas
    sgp40_sensor = sgp40.SGP40(i2c)
    office_environment_data["sgp40_raw"]               = sgp40_sensor.measure_raw(humidity=office_environment_data["bme680_humidity"],temperature=office_environment_data["bme680_temp_c"])
    office_environment_data["sgp40_compensated"]       = 0 #sgp40_sensor.measure_raw(humidity=office_environment_data["bme680_humidity"],temperature=office_environment_data["bme680_temp_c"])
    
    print("brightness: ", office_environment_data["brightness"])
    print("bme680_temp_c: ", office_environment_data["bme680_temp_c"])
    print("bme680_humidity: ", office_environment_data["bme680_humidity"])
    print("bme680_pressure_hpa: ", office_environment_data["bme680_pressure_hpa"])
    print("bme680_altitude_meters: ", office_environment_data["bme680_altitude_meters"])
    print("bme680_gas_ohms: ", office_environment_data["bme680_gas_ohms"])
    print("sgp40_raw: ", office_environment_data["sgp40_raw"])
    print("sgp40_compensated: ", office_environment_data["sgp40_compensated"])
    return(json.dumps(office_environment_data))

if __name__ == "__main__":
    # Init i2c bus

    main()
