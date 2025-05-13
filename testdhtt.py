import pigpio
import time
# Source DHTT: https://github.com/joan2937/pigpio/blob/master/EXAMPLES/Python/DHT11_SENSOR/dht11.py
from dhtt import DHT11 


pi = pigpio.pi()
 
dhttSensor = DHT11(pi,17)
 
try:
	while True:
		data = next(dhttSensor)
		for i in dhttSensor:
			print(f"Temp: {data['temperature']}°C, Humid: {data['humidity']}%")
			break
		time.sleep(2)
finally :
	dhttSensor.close()
	pi.stop()