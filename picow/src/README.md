Created to work on a Raspberry Pi Pico W microcontroller using MicroPython.

Reads i2c sensors, and creates HTTP endpoint with JSON payload with sensor information to be scraped by Prometheus.  This is a limited set of sensors due only using the QWIIC based sensors, not the PMOD based sensors listed in the root bill of materials (BOM).

This uses a modified `GurgleApps Web Server` from <https://github.com/gurgleapps/pico-web-server-control>.
