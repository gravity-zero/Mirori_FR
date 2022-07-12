from os import system
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import requests
#import screen_brightness_control as sbc


GPIO.setmode(GPIO.BCM)
print("START detector")
 
def start_FR():
    return requests.get("http://127.0.0.1:5500/", stream=True) # return "OK" or "QRCODE" 
     
def start_VM():
    system("curl -G http://127.0.0.1:5500/virtual_mouse >/dev/null 2>&1 &")

def waiting_mode():
    system("curl -G http://127.0.0.1:5500/waiting_mode >/dev/null 2>&1 &")

def qrcode():
    system("curl -G http://127.0.0.1:5500/default_qr_code >/dev/null 2>&1 &")
    
def kill_VM():
    system("curl -G http://127.0.0.1:5500/user_finished")

#waiting_mode()

## CAPTEUR DE PRESENCE

Trig = 23  # Entree Trig du HC-SR04 branchee au GPIO 23
Echo = 24  # Sortie Echo du HC-SR04 branchee au GPIO 24

GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)
GPIO.output(Trig, False)

#sbc.set_brightness(1000)

stop_count=0
start_count=0
started=False

timer = datetime.now() + timedelta(seconds=36000)

while (True):
    
    now = datetime.now()
    time.sleep(1)       # On la prend toute les 1 seconde

    GPIO.output(Trig, True)
    time.sleep(0.00001)
    GPIO.output(Trig, False)

    while GPIO.input(Echo)==0:  ## Emission de l'ultrason
      debutImpulsion = time.time()

    while GPIO.input(Echo)==1:   ## Retour de l'Echo
      finImpulsion = time.time()

    distance = round((finImpulsion - debutImpulsion) * 340 * 100 / 2, 1)  ## Vitesse du son = 340 m/s
    print("distance est de :", distance, "cm", flush=True)

    #Si la distance est inférieur à 1m50 
    if distance < 150.00 and not started:
        start_count+=1
    else:
        start_count=0

    if distance < 150.00 and start_count > 1 and not started:
        print("START FR", flush=True)
        #sbc.fade_brightness(100, increment=20, interval=0.5)
        value = start_FR()

        if value.text == "OK":
            started=True
            start_VM()
        else:
            qrcode()
        timer = datetime.now() + timedelta(seconds=10) #320

    print(started, flush=True)

    # if no one stay in front (<1m50) of mirori after 5min we count 20sec without close distance & we kill all the programm & came back to waiting mode
    if distance >= 200.00 and timer < now and started:
        stop_count+=1
    else:
        stop_count=0

    if stop_count > 10:
        print("STOP VM", flush=True)
        kill_VM()
        waiting_mode
        stop_count=0
        start_count=0
        started=False
        #sbc.set_brightness(0)
        time.sleep(10)
        timer = datetime.now() + timedelta(seconds=36000)

    

GPIO.cleanup() # inutile, la boucle n'a pas de condition de sortie




