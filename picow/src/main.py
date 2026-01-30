"""
    Based on the GurgleApps Webserver example code.
    Project: GurgleApps Webserver
    File: main.py
    Author: GurgleApps.com
    Date: 2021-04-01
    Description: Demonstrates how to use the GurgleApps Webserver
"""

#  from platform import machine
from gurgleapps_webserver import GurgleAppsWebserver
import config
import utime as time
import ntptime
import uasyncio as asyncio
import machine
from machine import Pin, I2C, ADC
import ujson as json
import template
from usmbus import SMBus  # wrapper for smbus for bme680
from bme680 import BME680


led = Pin("LED", Pin.OUT)

# hardware config
I2C_BUS = 0
I2C_SDA_PIN = 8
I2C_SCL_PIN = 9
I2C_FREQ = 100000
BME680_I2C_ADDR = 0x77

# Pico CPU y temperature calibration
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

# Initialize I2C bus
i2c = I2C(
    I2C_BUS,
    scl=Pin(I2C_SCL_PIN),
    sda=Pin(I2C_SDA_PIN),
    freq=I2C_FREQ
    )

# psuedo SMbus for bme680
smbus = SMBus(
    id=I2C_BUS, 
    scl=Pin(I2C_SCL_PIN), 
    sda=Pin(I2C_SDA_PIN), 
    freq=I2C_FREQ
    )

devices = i2c.scan()
if devices is None:

    raise "No i2c devices found on bus!  Have you connected the correct pins?"
else:
    print("i2c devices: ")
    print(devices)

# Setup locks
data_lock = asyncio.Lock()

# Environment sensor status
sensor_data = dict()
sensor_data["location"]                = config.LOCATION
sensor_data["core_temp_c"]             = 0
sensor_data["core_temp_f"]             = 0
sensor_data["bme680_temp_c"]           = 0
sensor_data["bme680_temp_f"]           = 0
sensor_data["bme680_humidity"]         = 0
sensor_data["bme680_pressure_hpa"]     = 0
sensor_data["bme680_altitude_meters"]  = 0
sensor_data["bme680_gas_ohms"]         = 0

def c_to_f(c):
    """Convert Celsius to Fahrenheit."""
    return (c * 9/5) + 32

def f_to_c(f):
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5/9

async def read_sensors():
    print("Starting read_sensors task")
    global sensor_data
    global data_lock

    await data_lock.acquire()
    # Initialize BME680 sensor
    bme680 = BME680(i2c_device=smbus, i2c_addr=BME680_I2C_ADDR)
    asyncio.sleep(0.5)  # Introduce a delay to allow the bme680 to heat up
    data_lock.release()
    while True:
        await data_lock.acquire()
        try:
            # Read data from BME680 sensor
            # Update sensor_data dictionary with the new values
            sensor_data["bme680_temp_c"] = bme680.data.temperature
            sensor_data["bme680_humidity"] = bme680.data.humidity
            sensor_data["bme680_pressure_hpa"] = bme680.data.pressure
            sensor_data["bme680_gas_ohms"] = bme680.data.gas_resistance
            sensor_data["bme680_temp_f"] = c_to_f(sensor_data["bme680_temp_c"])
            raw_cpu_temp = sensor_temp.read_u16() * conversion_factor
             # Convert voltage to temperature (Celsius)
            sensor_data["cpu_temp_c"] = 27 - (raw_cpu_temp - 0.706)/0.001721
            sensor_data["cpu_temp_f"] = c_to_f(sensor_data["cpu_temp_c"])
        finally:
            data_lock.release()
        await asyncio.sleep(10)  # Read sensors every 10 seconds


async def metrics(request, response):
    global sensor_data
    global data_lock
    await data_lock.acquire()
    try:
        data = json.loads(json.dumps(sensor_data))
    finally:
        data_lock.release()
    metrics_data = template.generate_metrics(data)
    await response.send(metrics_data, content_type="text/plain")
    
# async def get_time(request, response):
#     if not server.wlan_sta.isconnected():
#         response_string = json.dumps({"error": True, "message": "Not connected to wifi", "time": time.localtime()})
#         await response.send_json(response_string, 200)
#         return
#     try:
#         ntptime.host = "pool.ntp.org"
#         ntptime.settime()
#         response_string = json.dumps({"error": False, "time": time.localtime()})
#         await response.send_json(response_string, 200)
#     except Exception as e:
#         response_string = json.dumps({"error": True, "message": str(e), "time": time.localtime()})
#         await response.send_json(response_string, 200)


# async def stop_server(request, response):
#     global shutdown
#     await response.send_html("Server stopping")
#     await server.stop_server()
#     shutdown = True

async def connnect_to_wifi():
    wifi_ssid = config.WIFI_SSID.strip()
    if wifi_ssid:
        wifi_password = config.WIFI_PASSWORD.strip()
        print("Connecting to wifi")
        success = await server.connect_wifi(wifi_ssid, wifi_password)
        if success:
            print("Connected to wifi")
        else:
            print("Failed to connect to wifi")
        return success
    else:
        print("No wifi ssid set")
        return False


# async def run_as_access_point(request, response):
#     print("Running as access point")
#     success = server.start_access_point('gurgleapps', 'gurgleapps')
#     if success:
#         await response.send_html("Running as access point")
#     else:
#         await response.send_html("Failed to run as access point")


async def main():
    await connnect_to_wifi()
    # print("Past Wifi")
    # print("Setup done, starting tasks")
    asyncio.create_task(read_sensors())
    # asyncio.create_task(blink_led())
    print("Read Sensors task started")

print("starting web server")
server = GurgleAppsWebserver(
    port=80,
    timeout=20,
    doc_root="/www",
    log_level=3      
     
)
server.default_index_pages = ['index.html']
server.add_function_route("/metrics", metrics)
print('metrics route added')
print("starting server with background task")
asyncio.run(server.start_server_with_background_task(main))

