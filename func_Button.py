# faite par Rodney
import pigpio

BUTTON = 2
pi = pigpio.pi()
pi.set_mode(BUTTON,pigpio.INPUT)




# def on_btn_click():
while True:
    print(pi.read(BUTTON))

