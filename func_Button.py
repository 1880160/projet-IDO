# faite par Rodney
# REFERENCE : https://stackoverflow.com/questions/61713551/how-to-properly-use-time-time
import pigpio
import time


BUTTON = 2
pi = pigpio.pi()
pi.set_mode(BUTTON,pigpio.INPUT)
R,G,B = 20,16,21
pi.set_mode(R,pigpio.OUTPUT)
pi.set_mode(G,pigpio.OUTPUT)
pi.set_mode(B,pigpio.OUTPUT)



def on_btn_click(client,TOPIC_TEMP,TOPIC_HUMID):
    global envoieDonnees
    global currentTemp
    global currentHumid

start_time = 0
count = 0

while True:
    print(pi.read(2))
    try:    
        if pi.read(2) == 0  :
            count +=1
        if pi.read(2) == 0 and count < 10 : 
            # temps initiale enregistrer
            start_time = time.time()
            print(start_time)
        #  si bouton appuyer et (temps actuel - temps appuyer superieur) a 2 = contraire de letat de la variable/fonction envoieDonnes
        temps = time.time() - start_time
        print(temps)
        time.sleep(1)
        if pi.read(2) == 0 and temps > 2:
            print("temps: " + str(temps))
            # envoieDonnees = not envoieDonnees
        else:
            # client.publish(TOPIC_TEMP, str(currentTemp))
            # client.publish(TOPIC_HUMID, str(currentHumid))
            flag = True
    except KeyboardInterrupt:
        pi.stop()
        
                