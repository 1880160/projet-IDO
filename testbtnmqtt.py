import pigpio
import time
# import paho.mqtt.client as pmc
import pigpio

BROKER = "mqttbroker.lan"
PORT = 1883
TOPIC = "exercice2"
btn = 2
pi = pigpio.pi()
pi.set_mode(btn,pigpio.INPUT)
pi.set_pull_up_down(btn, pigpio.PUD_UP)
def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)





buttonTime = 0.0
autoSend = False

def codeloop():
	while True:
		print("clic")
		time.sleep(5)
		if (pi.read(btn)) == 0:
			break

def code():
	print("clic")
	time.sleep(2)
    

try:
	print ("Hello Wrld")
	while True :
		if (pi.read(btn)) == 0:
			if buttonTime == 0:
				buttonTime = time.time()
				code()
			elif time.time() - buttonTime > 2:
				while True :
						codeloop()
						
						
		else :
			buttonTime = 0.0
 
 
except KeyboardInterrupt:
	pi.stop()		
	pass


# To Resolve : Arret de l'envoi

    