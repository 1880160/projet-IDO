import paho.mqtt.client as pmc
import pigpio
import time
from dhtt import DHT11 


BROKER = "mqttbroker.lan"
PORT = 1883
HOTE = "pi"
TOPIC_T = "test/{HOTE}/T"
TOPIC_H = "test/{HOTE}/H"
DHTT = 17

pi = pigpio.pi()
dhttSensor = DHT11(pi,DHTT)




def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)




client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client.on_connect = connexion
client.connect(BROKER,PORT)

def publication_msg(sensor,client,topic_t,topic_h):
    data = next(dhttSensor)
    temp = data['temperature']
    hum = data['humidity']
    client.publish(topic_t,temp)
    client.publish(topic_h,hum)

try:
    while True:
        print
        publication_msg(dhttSensor,client,TOPIC_T,TOPIC_H)
        time.sleep(3)
except KeyboardInterrupt as e:
        dhttSensor.close()
        pi.stop()
        client.loop_stop()
        client.client.disconnect()
        print(f"Bye {e}")