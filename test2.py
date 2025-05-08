
import time
import adafruit_dht
import board

# Initialize sensor connected to GPIO 4
sensor = adafruit_dht.DHT11(17)

while True:
    try:
        # Read temperature and humidity
        temperature_c = sensor.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity
        
        # Print readings
        print(f"Temp: {temperature_c:.1f}°C / {temperature_f:.1f}°F    Humidity: {humidity:.1f}%")
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
        
    time.sleep(2.0)