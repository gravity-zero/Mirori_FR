from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import system, getenv
import browser as bi
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv("../.env")
GPIO.setmode(GPIO.BCM)

browser = bi.chromium_instance() # We close all existents instance & start new one

def waiting_page(browser):
    browser.get('https://gravity-zero.fr')

def start_FR():
    user_id = system("curl -G http://127.0.0.1:5500/")
    if user_id:
        system("curl -G http://127.0.0.1:5500/user_experience")
        back_route = getenv("back_route")
        api_key = getenv("api_key")
        data = "id=" + user_id + "api_key=" + api_key
        composed_route = back_route + "/auth/login"
        jwt_token = system('curl -d '+data+' -H "Content-Type: application/x-www-form-urlencoded" -X POST '+composed_route)

def kill_FR():
    system("curl -G http://127.0.0.1:5500/user_finished")

waiting_page(browser)

## CAPTEUR DE PRESENCE

Trig = 23  # Entree Trig du HC-SR04 branchee au GPIO 23
Echo = 24  # Sortie Echo du HC-SR04 branchee au GPIO 24

GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)
GPIO.output(Trig, False)

first=True
count=0
timer = datetime.now() + timedelta(seconds=320)

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

    if distance < 150.00 and first:
        start_FR()
        first=False

    # if no one stay in front (<1m50) of mirori after 5min we count 20sec without close distance & we kill all the programm & came back to waiting mode
    if distance >= 200.00 and timer < now:
        count+=1
    else:
        count=0

    if count > 20:
        kill_FR()
        if bi.get_status(browser) != "Alive":
            browser = bi.chromium_instance()
        waiting_page(browser)
        first=True
        count=0
        timer = datetime.now() + timedelta(seconds=320)
    

#GPIO.cleanup() # inutile, la boucle n'a pas de condition de sortie




