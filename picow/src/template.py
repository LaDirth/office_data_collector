def generate_metrics(sensor_data):
    instance = f'instance="{sensor_data["location"]}",'
    template = ""
    template += "# HELP bme680_altitude_meters Altitude in meters calculated by BME680\n"
    template += "# TYPE bme680_altitude_meters untyped\n"
    template += 'bme680_altitude_meters{' + instance + 'sensor="bme680",unit="meters"} ' + str(sensor_data["bme680_altitude_meters"]) + '\n'
    template += "# HELP bme680_gas_ohms Gas resistance in ohms from BME680 sensor\n"
    template += "# TYPE bme680_gas_ohms untyped\n"
    template += 'bme680_gas_ohms{' + instance + 'sensor="bme680",unit="ohms"} ' + str(sensor_data["bme680_gas_ohms"]) + '\n'
    template += "# HELP bme680_humidity Humidity reading from BME680 sensor\n"
    template += "# TYPE bme680_humidity untyped\n"
    template += 'bme680_humidity{' + instance + 'sensor="bme680",unit="percent"} ' + str(sensor_data["bme680_humidity"]) + '\n'
    template += "# HELP bme680_pressure_hpa Pressure in hPa from BME680 sensor\n"
    template += "# TYPE bme680_pressure_hpa untyped\n"
    template += 'bme680_pressure_hpa{' + instance + 'sensor="bme680",unit="hpa"} ' + str(sensor_data["bme680_pressure_hpa"]) + '\n'
    template += "# HELP bme680_temp_c Temperature in Celsius from BME680 sensor\n"
    template += "# TYPE bme680_temp_c untyped\n"
    template += 'bme680_temp_c{' + instance + 'sensor="bme680",unit="celsius"} ' + str(sensor_data["bme680_temp_c"]) + '\n'
    template += "# HELP bme680_temp_f Temperature in Fahrenheit from BME680 sensor\n"
    template += "# TYPE bme680_temp_f untyped\n"
    template += 'bme680_temp_f{' + instance + 'sensor="bme680",unit="fahrenheit"} ' + str(sensor_data["bme680_temp_f"]) + '\n'
    template += "# HELP cpu_temp_c Temperature in Celsius from CPU sensor\n"
    template += "# TYPE cpu_temp_c untyped\n"
    template += 'cpu_temp_c{' + instance + 'sensor="cpu",unit="celsius"} ' + str(sensor_data["cpu_temp_c"]) + '\n'
    template += "# HELP cpu_temp_f Temperature in Fahrenheit from CPU sensor\n"
    template += "# TYPE cpu_temp_f untyped\n"
    template += 'cpu_temp_f{' + instance + 'sensor="cpu",unit="fahrenheit"} ' + str(sensor_data["cpu_temp_f"]) + '\n'
    return template