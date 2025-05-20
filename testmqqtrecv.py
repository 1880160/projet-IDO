import paho.mqtt.client as pmc
import subprocess
import threading
import os
import random
 
  # Reaction 2 : Reaction de la reception du message MQTT et lancement de la vidéo
 
# ==> Initialisation du MQTT ==
BROKER = "mqttbroker.lan"
PORT = 1883
TOPIC_T = "test/{HOTE}/T"
TOPIC_H = "test/{HOTE}/H"
 
# ==> Fonction qui demarre la vidéo en "Full Screen"
# def startVideo():
#     os.environ["DISPLAY"] = ":0"
#     os.system(f"vlc {video} --fullscreen")
#     print("test")
 
 
 # ==> Connexion MQTT 
def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)
 

 # ==> Reception du message transmis via le topic et lancement de la video
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    if msg.topic.endswith("/T"):
            temp = message
    elif msg.topic.endswith("/H"):
            hum = message
 
    print(f"Température: {temp}°C | Humidité: {hum}%")
   
client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client.on_connect = connexion
client.on_message = on_message
 
try:
    while True:
        client.connect(BROKER,PORT)
        client.subscribe(TOPIC_H)
        client.subscribe(TOPIC_T)
        client.loop_forever()
except KeyboardInterrupt as e:
    print(f"Bye {e}")