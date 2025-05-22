import paho.mqtt.client as pmc
import pigpio
import time
import socket
from dhtt import DHT11
 
# MQTT configuration
BROKER = "mqttbroker.lan"
PORT = 1883
 
# Utilise le nom de l'appareil comme identifiant
HOTE = socket.gethostname()
 
# Topics
TOPIC_T = f"final/{HOTE}/T"
TOPIC_H = f"final/{HOTE}/H"
TOPICRCP_T = "final/+/T"
TOPICRCP_H = "final/+/H"
 
# DHT11 GPIO
DHTT = 17
 
# Variables globales
temp = None
hum = None
tempRecv = None
humRecv = None
 
# Initialisation capteur et MQTT
pi = pigpio.pi()
dhttSensor = DHT11(pi, DHTT)
 
def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("✅ Connecté au broker MQTT")
    else:
        print(f"❌ Erreur de connexion : {code}")
 
def on_message(client, userdata, message, properties=None):
    global tempRecv, humRecv
    topic = message.topic
    payload = message.payload.decode()
 
    # Ignorer ses propres messages
    if HOTE in topic:
        return
 
    if "/T" in topic:
        tempRecv = payload
    elif "/H" in topic:
        humRecv = payload
 
    print(f"[REÇU AUTRE PI] {topic} : {payload}")
 
# Client MQTT
client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client.on_connect = connexion
client.on_message = on_message
 
client.connect(BROKER, PORT)
client.subscribe(TOPICRCP_T)
client.subscribe(TOPICRCP_H)
client.loop_start()
 
# Lecture DHT11
def publication_msg(sensor):
    global temp, hum
    data = next(sensor)
    temp = data['temperature']
    hum = data['humidity']
 
try:
    while True:
        publication_msg(dhttSensor)
 
        # Publier les données locales
        client.publish(TOPIC_T, str(temp))
        client.publish(TOPIC_H, str(hum))
 
        # Afficher
        print(f"[MOI] Temp: {temp}°C | Hum: {hum}%")
 
        # Comparer avec les données reçues
        if tempRecv is not None and int(tempRecv) < temp:
            print("🔥 Ma température est la plus haute")
        if humRecv is not None and int(humRecv) < hum:
            print("💧 Mon humidité est la plus élevée")
 
        time.sleep(3)
 
except KeyboardInterrupt:
    print("⛔ Arrêt manuel")
    dhttSensor.cancel()
    pi.stop()
    client.loop_stop()
    client.disconnect()
    print("🛑 Fini proprement.")