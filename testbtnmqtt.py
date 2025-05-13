import pigpio
import time
import paho.mqtt.client as pmc
import pigpio

BROKER = "mqttbroker.lan"
PORT = 1883
TOPIC = "exercice2"


def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)

pi = pigpio.pi()
pi.set_mode(BTN,pigpio.INPUT)

client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client.on_connect = connexion
client.connect(BROKER,PORT)
client.loop_start()

btn = 2
pi = pigpio.pi()
pi.set_mode(btn,pigpio.INPUT)
pi.set_pull_up_down(btn, pigpio.PUD_UP)

buttonTime = 0.0
autoSend = False

def code():
	while True:
		client.publish(TOPIC,"clic")
		time.sleep(5)
    

try:
	print ("Hello Wrld")
	while True :
		if (pi.read(btn)) == 0:
			if buttonTime == 0:
				buttonTime = time.time()
				client.publish(TOPIC,"clic")
			elif time.time() - buttonTime > 2:
				autoSend = True
				while autoSend :
						code()
						if time.time() - buttonTime > 2:
							autoSend = False
						
		else :
			print ("Attente : Appuyez sur le bouton")
			buttonTime = 0.0
 
 
except KeyboardInterrupt:
	pi.stop()		
	pass


# To Resolve : Arret de l'envoi

    