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



# def on_btn_click(client,TOPIC_TEMP,TOPIC_HUMID):
#     global envoieDonnees
#     global currentTemp
#     global currentHumid


compte = 0
while True:
    try:
        if pi.read(2) == 0:
            # temps initiale enregistrer
            start_time = time.time()
            #  si bouton appuyer et (temps actuel - temps appuyer superieur) a 2 = contraire de letat de la variable/fonction envoieDonnes
            temps = time.time() - start_time
            compte += 1
            print(compte)
            if pi.read(2) == 0 and compte > 10000:
                print("temps: " + str(temps))
                # envoieDonnees = not envoieDonnees
                pi.write(R,1)
                pi.write(G,0)
                pi.write(B,1)
                print("if")
            else:
                # client.publish(TOPIC_TEMP, str(currentTemp))
                # client.publish(TOPIC_HUMID, str(currentHumid))
                pi.write(R,1)
                pi.write(G,0)
                pi.write(B,1)
                print("else")
    except KeyboardInterrupt:
        pi.stop()
        
                