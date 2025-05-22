
import paho.mqtt.client as pmc
import pigpio
import time
from dhtt import DHT11 

#Source : https://cedalo.com/blog/configuring-paho-mqtt-python-client-with-examples/#Subscribe_to_topics_with_the_Paho_MQTT_client
#- Par Maindy

BROKER = "mqttbroker.lan"
PORT = 1883
HOTE = "pi"
TOPIC_T = f"final/{HOTE}/T"
TOPICRCP_T = "final/+/T"
TOPIC_H = f"final/{HOTE}/H"
TOPICRCP_H = "final/+/H"


DHTT = 17
R,G,B = 16,20,21



temp = None
hum = None
tempRecv = None
humRecv = None


pi = pigpio.pi()
dhttSensor = DHT11(pi,DHTT)
pi.set_mode(R,pigpio.OUTPUT)
pi.set_mode(G,pigpio.OUTPUT)
pi.set_mode(B,pigpio.OUTPUT)
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
        print(f" < Temp: {data}°C")
    elif "/H" in currentTopic:
        humRecv = data
        print(f" < Hum: {data}%")


    print (f" > {currentTopic}:{data}")
  


def publication_msg(sensor):
    global temp, hum
    data = next(sensor)
    temp = data['temperature']
    hum = data['humidity']
    
    


client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client.on_connect = connexion
client.connect(BROKER,PORT)
client.subscribe(TOPICRCP_T)
client.subscribe(TOPICRCP_H)
client.on_message = on_message
client.loop_start()




try:
    while True:
        publication_msg(dhttSensor)
        client.publish(TOPIC_T,temp)
        client.publish(TOPIC_H,hum)
        print(f" < Temp: {temp}°C | Hum: {hum}%")
        
        if tempRecv is not None and int(tempRecv) < temp:
            print("Ma temperature is higher")
            pi.write(R,0)
            pi.write(G,1)
            pi.write(B,1)
            time.sleep(1)
        elif humRecv is not None and int(humRecv) < hum:
            print("Mon humidité is higher")
            pi.write(R,1)
            pi.write(G,1)
            pi.write(B,0)
            time.sleep(1)
        else :
            print("Theirs is higher")
            pi.write(R,1)
            pi.write(G,0)
            pi.write(B,1)
            time.sleep(1)
        time.sleep(3)
        
        
except KeyboardInterrupt as e:
        dhttSensor.close()
        pi.stop()
        client.loop_stop()
        client.disconnect()
        print(f"Bye {e}")
