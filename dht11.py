import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11
pin = 4


def read_dht11_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        # If the readings are valid, return humidity and temperature
        return humidity, temperature
    else:
        # If readings are not valid, return None for both
        return None, None


# Example usage
humidity, temperature = read_dht11_sensor_data()
if humidity is not None and temperature is not None:
    print(f'Readings - Humidity: {humidity}% Temperature: {temperature}°C')
else:
    print('Failed to read data from DHT11 sensor')
