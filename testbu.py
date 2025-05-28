
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





count = 0


def isPressed():
    while True:
            
        if pi.read(2) == 0 and count == 100000:
            return True
        else:
            return False

while True:
    print(count)
    print(pi.read(2))
    try:    
        if isPressed == True:
            print("true")
            count +=1
            # envoieDonnees = not envoieDonnees
        elif isPressed == False:
            print("false")
 
            # client.publish(TOPIC_TEMP, str(currentTemp))
            # client.publish(TOPIC_HUMID, str(currentHumid))
            flag = True
    except KeyboardInterrupt:
        pi.stop()
        
                