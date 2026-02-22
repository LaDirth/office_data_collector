from microdot import Microdot
import config
import machine
from machine import Pin, I2C, ADC
import network
import asyncio
from usmbus import SMBus  # wrapper for smbus for bme680
from bme680 import BME680
import template

# hardware config
I2C_BUS = 0
I2C_SDA_PIN = 8
I2C_SCL_PIN = 9
I2C_FREQ = 100000
BME680_I2C_ADDR = 0x77

# Pico CPU temperature calibration
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
if not devices:
    raise RuntimeError("No i2c devices found on bus!  Have you connected the correct pins?")
else:
    print("Found i2c devices: " + str({hex(n) for n in devices}))

# Setup locks
data_lock = asyncio.Lock()

prometheus_string = 'BME680 not yet initialized'

def c_to_f(c):
    """Convert Celsius to Fahrenheit."""
    return (c * 9/5) + 32

def f_to_c(f):
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5/9

async def read_sensors():
    print("Starting read_sensors task")
    global prometheus_string
    
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
    
    # Initialize BME680 sensor
    bme680 = BME680(i2c_device=smbus, i2c_addr=BME680_I2C_ADDR)
    asyncio.sleep(10)  # Introduce a delay to allow the bme680 to heat up
    while True:
        # Read data from BME680 sensor
        # Update sensor_data dictionary with the new values
        sensor_data["bme680_temp_c"] = bme680.data.temperature
        sensor_data["bme680_humidity"] = bme680.data.humidity
        sensor_data["bme680_pressure_hpa"] = bme680.data.pressure
        sensor_data["bme680_gas_ohms"] = bme680.data.gas_resistance
        sensor_data["bme680_temp_f"] = c_to_f(sensor_data["bme680_temp_c"])
        raw_cpu_temp = sensor_temp.read_u16() * conversion_factor
        # Convert voltage to temperature (Celsius)
        sensor_data["core_temp_c"] = 27 - (raw_cpu_temp - 0.706)/0.001721
        sensor_data["core_temp_f"] = c_to_f(sensor_data["core_temp_c"])
        async with data_lock:  # Automatically acquire & release
            prometheus_string = template.generate_metrics(sensor_data)
        await asyncio.sleep(10)  # Read sensors every 10 seconds

def connect_wifi(ssid, key):
    print("Trying to connect to network")
    wlan = network.WLAN()
    mac_bytes = wlan.config('mac')
    print('mac address: ' + ':'.join('{:02x}'.format(b) for b in mac_bytes))
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            machine.idle()
    print('network config:', wlan.ipconfig('addr4'))

connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
asyncio.create_task(read_sensors())
app = Microdot()

print("Adding Routes")
@app.route('/')
async def index(request):
    return 'Unauthorized', 401

@app.route('/metrics')
async def metrics(request):
    global prometheus_string
    async with data_lock:  # Automatically acquire & release
        return prometheus_string
print("Starting Microdot")
app.run(
    port=80,
    debug=True
    )