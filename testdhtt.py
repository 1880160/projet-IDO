import pigpio
import time
# Source DHTT: https://github.com/joan2937/pigpio/blob/master/EXAMPLES/Python/DHT11_SENSOR/dht11.py
from dhtt import DHT11 


pi = pigpio.pi()
 
dhttSensor = DHT11(pi,17)
temp = 0.0
hum  = 0.0

def lire():
	global temp
	global hum  

try:
	while True:
		data = next(dhttSensor)
		for i in dhttSensor:
			temp = data['temperature']
			hum = data['humidity']
			print(f"Temp: {temp}°C, Humid: {hum}%")
			break
		time.sleep(2)
finally :
	dhttSensor.close()
	pi.stop()