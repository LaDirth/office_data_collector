"""
    Project: GurgleApps Webserver
    File: main.py
    Author: GurgleApps.com
    Date: 2021-04-01
    Description: Demonstrates how to use the GurgleApps Webserver
"""
from gurgleapps_webserver import GurgleAppsWebserver
import config
import utime as time
import ntptime
import uasyncio as asyncio
from machine import Pin
import ujson as json
from board import Board
from machine import I2C
# import sensor libaries
from veml6030 import Veml6030
import bme680
import sgp40


BOARD_TYPE = Board().type
print("Board type: " + BOARD_TYPE)
INVERT_LED = False
if BOARD_TYPE == Board.BoardType.PICO_W:
    led = Pin("LED", Pin.OUT)
elif BOARD_TYPE == Board.BoardType.PICO:
    led = Pin(25, Pin.OUT)
elif BOARD_TYPE == Board.BoardType.ESP8266:
    led = Pin(2, Pin.OUT)
    INVERT_LED = True
elif BOARD_TYPE == Board.BoardType.ESP32:
    led = Pin(2, Pin.OUT)
    INVERT_LED = True
elif BOARD_TYPE == Board.BoardType.ESP32_C3:
    led = Pin(8, Pin.OUT)
    INVERT_LED = True
else:
    led = Pin(2, Pin.OUT)

# hardware config
I2C_BUS = 0
I2C_SDA_PIN = 8
I2C_SCL_PIN = 9



blink_off_time = 0.5
blink_on_time = 0.5

status = False
shutdown = False

async def get_sensor_data(request, response):
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
    await response.send_json(json.dumps(office_environment_data), 200)

async def say_hello(request, response, name):
    await response.send_html("Hello " + name + " hope you are well")

async def send_status(request, response):
    # send boolean status and number frequency
    response_string = json.dumps({"status": status, "delay": (blink_off_time + blink_on_time) *0.5, "blink_on_time": blink_on_time, "blink_off_time": blink_off_time})
    await response.send_json(response_string, 200)

async def set_blink_pattern(request, response, on, off):
    print("on: " + on)
    print("off: " + off)
    global blink_off_time, blink_on_time
    blink_off_time = float(off)
    blink_on_time = float(on)
    await send_status(request, response)

async def set_delay(request, response, new_delay):
    print("new delay: " + new_delay)
    global blink_off_time, blink_on_time
    blink_off_time = float(new_delay)
    blink_on_time = float(new_delay) 
    await send_status(request, response)

async def stop_flashing(request, response):
    global status
    status = False
    await send_status(request, response)

async def start_flashing(request, response):
    global status
    status = True
    await send_status(request, response)

async def get_time(request, response):
    if not server.wlan_sta.isconnected():
        response_string = json.dumps({"error": True, "message": "Not connected to wifi", "time": time.localtime()})
        await response.send_json(response_string, 200)
        return
    try:
        ntptime.host = "pool.ntp.org"
        #ntptime.host = "time.nist.gov"
        ntptime.settime()
        response_string = json.dumps({"error": False, "time": time.localtime()})
        await response.send_json(response_string, 200)
    except Exception as e:
        response_string = json.dumps({"error": True, "message": str(e), "time": time.localtime()})
        await response.send_json(response_string, 200)

async def stop_server(request, response):
    global shutdown
    await response.send_html("Server stopping")
    await server.stop_server()
    shutdown = True

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


async def run_as_access_point(request, response):
    print("Running as access point")
    success = server.start_access_point('gurgleapps', 'gurgleapps')
    if success:
        await response.send_html("Running as access point")
    else:
        await response.send_html("Failed to run as access point")


async def main():
    global shutdown
    await connnect_to_wifi()
    print("Past Wifi")
    if config.BLINK_IP:
        await(server.blink_ip(led_pin = led, last_only = config.BLINK_LAST_ONLY))
    while not shutdown:
        if status:
            led.value(not INVERT_LED)
            await asyncio.sleep(blink_on_time)
            led.value(INVERT_LED)
            await asyncio.sleep(blink_off_time)
        else:
            led.value(not INVERT_LED)
            await asyncio.sleep(0.2)

print("starting web server")
server = GurgleAppsWebserver(
    port=80,
    timeout=20,
    doc_root="/www",
    log_level=3      
     
)
server.default_index_pages = ['index.html']
print("pre function adds")
server.add_function_route("/set-delay/<delay>", set_delay)
server.add_function_route(
    "/set-blink-pattern/<on_time>/<off_time>",
    set_blink_pattern
)
#server.add_function_route("/stop", stop_flashing)
#server.add_function_route("/start", start_flashing)
#server.add_function_route("/status", send_status)
#server.add_function_route("/example/func/<param1>/<param2>", example_func)
#server.add_function_route("/hello/<name>", say_hello)
#server.add_function_route("/stop-server", stop_server)
#server.add_function_route("/run-as-access-point", run_as_access_point)
#server.add_function_route("/get-time", get_time)
server.add_function_route("/data", get_sensor_data)
print('post function adds')
asyncio.run(server.start_server_with_background_task(main))
print('DONE')
