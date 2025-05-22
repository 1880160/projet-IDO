import paho.mqtt.client as pmc
import pigpio
import time
from dhtt import DHT11 

#Source : https://cedalo.com/blog/configuring-paho-mqtt-python-client-with-examples/#Subscribe_to_topics_with_the_Paho_MQTT_client


BROKER = "mqttbroker.lan"
PORT = 1883
HOTE = "pi"
TOPIC_T = f"test/{HOTE}/T"
TOPICRCP_T = "test/+/T"
TOPIC_H = f"test/{HOTE}/H"
TOPICRCP_H = "test/+/H"


DHTT = 17

temp = None
hum = None
tempRecv = None
humRecv = None


pi = pigpio.pi()
dhttSensor = DHT11(pi,DHTT)
def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)


def on_message(client, userdata, message, properties=None):
    global tempRecv, humRecv
    data = message.payload.decode()
    currentTopic = message.topic
 
 
    if "/T" in currentTopic:
        tempRecv = data
    elif "/H" in currentTopic:
        humRecv = data

    print (f"{currentTopic}:{message}")


def publication_msg(sensor):
    global temp, hum
    data = next(sensor)
    temp = data['temperature']
    hum = data['humidity']
    
    


client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client.on_connect = connexion
client.connect(BROKER,PORT)
client.on_message = on_message
client.subscribe(TOPICRCP_T)
client.subscribe(TOPICRCP_H)
client.loop_start()




try:
    while True:
        publication_msg(dhttSensor)
        client.publish(TOPIC_T,temp)
        client.publish(TOPIC_H,hum)
        
        print(f" < Temp: {temp}°C | Hum: {hum}%")
        if tempRecv is not None and int(tempRecv) < temp:
            print("My temp is higher")
        elif humRecv is not None and int(humRecv) < hum:
            print("My humidity is higher")
        time.sleep(3)
        
        
except KeyboardInterrupt as e:
        dhttSensor.close()
        pi.stop()
        client.loop_stop()
        client.disconnect()
        print(f"Bye {e}")