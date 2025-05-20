import pigpio
import paho.mqtt.client as pmc
import time
from dhtt import DHT11
from flask import Flask, jsonify, request
pi = pigpio.pi


# -----------------CONSTANCE----------------------
HOTE = "pi"
TOPIC_T = "test/{HOTE}/T"
TOPIC_H = "test/{HOTE}/H"
BROKER = 11
PORT = 1883
TOPIC = 123
BUTTON = 123
DHTTSENSOR = DHT11(pi,17)
FLAG = True

# DONNE RECUPERER PAR DHTT11
TEMP = 0.0
HUM  = 0.0
# DONNE RECUPERER PAR REST
TOPIC_TEMP = 0
TOPIC_HUM = 0




# valeur a cree avec REST
def controleLedBlanche():
    while True:
        if envoieDonnees:
            # Allumer LED BLANCHE
            print("LED BLANCHE ALLUMER")
        else:
            # Eteindre LED BLANCHE
            print("LED BLANCHE ETEINDRE")