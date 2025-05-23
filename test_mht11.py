# www.youtube.com/watch?v=WUoCCQmxxEk

import RPi.GPIO as GPIO
import time
import LA_DHT as DHT
DHTPin = 17     #define the pin of DHT11

def loop():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    sumCnt = 0              #number of reading times 
    while(True):
        sumCnt += 1         #counting number of reading times
        chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        print ("The sumCnt is : %d, \t chk    : %d"%(sumCnt,chk))
        if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            print("DHT11,OK!")
        elif(chk is dht.DHTLIB_ERROR_CHECKSUM): #data check has errors
            print("DHTLIB_ERROR_CHECKSUM!!")
        elif(chk is dht.DHTLIB_ERROR_TIMEOUT):  #reading DHT times out
            print("DHTLIB_ERROR_TIMEOUT!")
        else:               #other errors
            print("Other error!")
            
        print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
        time.sleep(2)       
        
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()