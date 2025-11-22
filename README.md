# office_data_collector

## Summary

This is the repo to collect environmental data from my office using a Raspberry PI 3b+ and a handful of I2C/SPI sensors.  

### Bill of Materials

| Device | Notes | Specs |
| -------- | --------- | ----------------------------- |
| `Raspberry Pi 3 Model B Plus Rev 1.3` | What I had on hand | <https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/> |
| `Pmod HAT Adapter: Pmod Expansion for Raspberry Pi` | Bought to test existing PMODs | <https://digilent.com/shop/pmod-hat-adapter-pmod-expansion-for-raspberry-pi/> |
| `SparkFun Qwiic pHAT v2.0 for Raspberry Pi` | From another project | <https://www.sparkfun.com/products/15945> |
| `SparkFun Environmental Sensor Breakout - BME680 (Qwiic)` | From another project | <https://www.sparkfun.com/products/16466> |
| `SparkFun Ambient Light Sensor - VEML6030 (Qwiic)` | From another project | <https://www.sparkfun.com/products/15436> |
| `Pmod HYGRO: Digital Humidity and Temperature Sensor` | From another project | <https://digilent.com/shop/pmod-hygro-digital-humidity-and-temperature-sensor/> |
| `Pmod Cable Kit: 6-pin` | From another project |  <https://digilent.com/shop/pmod-cable-kit-6-pin/> |
| `SparkFun Qwiic Cable Kit` | From another project  | <https://www.sparkfun.com/products/15081> |

## Host Setup

Run `sudo raspi-config` and enable I2c, SPI, and Remote GPIO.
Read <os_tweaks\README.MD> for additional config.

## Rapsberry Pi Pico W

The data collector has been migrated to a Raspberry Pi Pico W.
See [picow/README.md](./picow/README.md)

## Prometheus and Grafana

Prometheus and Grafana
