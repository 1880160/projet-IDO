
import paho.mqtt.client as pmc
import pigpio
import time
from dhtt import DHT11
from flask import Flask, jsonify, request
import threading

# Source : https://cedalo.com/blog/configuring-paho-mqtt-python-client-with-examples/#Subscribe_to_topics_with_the_Paho_MQTT_client
#- Maindy Goue et Rodney 
# voir autre fichier pour voir qui a fait quoi | MQTT, DHTT : Maindy | Bouton et REST : Rodney 


# -­> Initialisation des varaibles de MQTT
BROKER = "mqttbroker.lan"
PORT = 1883
HOTE = "pirm"
TOPIC_T = f"final/{HOTE}/T"
TOPICRCP_T = "final/+/T"
TOPIC_H = f"final/{HOTE}/H"
TOPICRCP_H = "final/+/H"

# -­> Initialisation des pins du rasberry pi
DHTT = 17
R,G,B = 16,20,21


# -­> Initialisation (vide) des varibles recues et envoyés
temp = None
hum = None
tempRecu = None
humRecu = None
pi = pigpio.pi()
dhttSensor = DHT11(pi,DHTT)
pi.set_mode(R,pigpio.OUTPUT)
pi.set_mode(G,pigpio.OUTPUT)
pi.set_mode(B,pigpio.OUTPUT)
envoiDonnees = True


# -> Connection MQTT [MG]
def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)


# -> Formule de reception de message [MG]
def on_message(client, userdata, message, properties=None):

    # Variables à remplir
    global tempRecu, humRecu

    # Stockage et decodage du message recu
    data = message.payload.decode()

    # Stockage de la provenance du message (soit du T pour temperature ou du H pour humidité)
    currentTopic = message.topic

    
    # Si la valeur provient du topic T, je stocke la variable dans tempRecu et je l'Affiche
    if "/T" in currentTopic:
        tempRecu = data
        print(f" Recu > Temp: {data}°C")

    # Si la valeur provient du topic H, je stocke la variable dans humRecu et je l'Affiche
    elif "/H" in currentTopic:
        humRecu = data
        print(f" Recu > Hum: {data}%")




# -> Stockage des valeurs que j'ai [MG]
def publication_msg(sensor):

    # Variables à remplir
    global temp, hum

    # Stockage des valeurs ressenties
    data = next(sensor)
    temp = data['temperature']
    hum = data['humidity']
    
    

# -> Configuration mqtt (connexion, subscription aux topics et debut du loop) [MG]
client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client.on_connect = connexion
client.connect(BROKER,PORT)
client.subscribe(TOPICRCP_T)
client.subscribe(TOPICRCP_H)
client.on_message = on_message
client.loop_start()




def controleLedBlanche():
        if envoieDonnees: # nom fonction qui va e
            # Allumer LED BLANCHE
            print("LED BLANCHE ALLUMER")
        else:
            # Eteindre LED BLANCHE
            print("LED BLANCHE ETEINDRE")

# # Declaration threads

thread_l =ledBlanche = threading.Thread(target=controleLedBlanche, daemon=True)
thread_l.start()

while True:

    
    # valeur a cree avec REST
    try:


        #Appel de la fonction et appelle du senseur branché au pi 
        publication_msg(dhttSensor)
        #Publier la temperature au topic de temperature
        # if envoiDonnees:
        client.publish(TOPIC_T,temp)
        #Publier l'humidité au topic d'humidité
        client.publish(TOPIC_H,hum)
        #Affichage de mes valeurs 
        print(f" Envoyé < Temp: {temp}°C | Hum: {hum}%")
        
        #Si la temperature recue n'est pas nulle et elle n'est pas plus haute que la mienne,
        if tempRecu is not None and int(tempRecu) < temp:
            # Affichage un message et allume la lumiere rouge
            print("Ma temperature est plus haute")
            pi.write(R,0)
            pi.write(G,1)
            pi.write(B,1)
            time.sleep(1)

        #Si l'humidité recue n'est pas nulle et elle n'est pas plus haute que la mienne,
        elif humRecu is not None and int(humRecu) < hum:
            # Affichage un message et allume la lumiere blue
            print("Mon humidité est plus haute")
            pi.write(R,1)
            pi.write(G,1)
            pi.write(B,0)
            time.sleep(1)
        #Si aucune de mes valeurs sont plus élévées j'allume une lumiere verte 
        else :
            print("Leurs valeurs sont plus haute")
            pi.write(R,1)
            pi.write(G,0)
            pi.write(B,1)
            time.sleep(1)
        time.sleep(3)
            
    # -> Fermeture de tout les services


        # app = Flask(__name__)

        # @app.route('/donnees',methods=['GET'])
        # def info_donnees():
        #     return jsonify(
        #         {
        #             "t": int(temp), 
        #             "h": int(hum)
        #         }
        #     )

        # @app.route('/etat', methods=['POST'])
        # def set_etat():
        #     if request.method == "POST":
        #         json = request.get_json()
        #         if "etat" in json:
        #             if json["etat"] == 0:
        # # 0 désactive l’envoi de données, 1 active l’envoi de données
        #                 envoiDonnees = False
        #                 return jsonify(
        #                     {
        #                         "etat": 0
        #                     })
        #             elif json["etat"] == 1:
        #                 envoiDonnees = True
        #                 return jsonify(
        #                     {
        #                         "etat": 1
        #                     })

        #             return jsonify({'Etat': json["etat"]}),200
        #     else:
        #         return jsonify({'Erreur': 'Requetes POST seulement'}),500

        # if __name__ == '__main__':
        #     app.run(host='0.0.0.0',port=3000)

    except KeyboardInterrupt as e:
            dhttSensor.close()
            pi.stop()
            client.loop_stop()
            client.disconnect()
            print(f"Bye {e}")


