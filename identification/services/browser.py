from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.chrome.options import Options
import http.client as httplib
import socket
from os import system 

def launch_chromium():
    chrome_options = Options()
    #chrome_options.add_argument("--kiosk")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) #Disable banner message 
    browser = webdriver.Chrome(options=chrome_options)
    return browser

def get_status(browser):
    try:
        browser.execute(Command.STATUS)
        return "alive"
    except (socket.error, httplib.CannotSendRequest):
        return "dead"

def get_current_url(browser):
    return browser.current_url

def kill_Chromium_process():
    system("while pgrep chrome ; do pkill chrome ; done")

def chromium_instance():
    nb_instance = system("ps aux | grep chrome | wc -l")
    if nb_instance == 1:
        return launch_chromium()
    if nb_instance >= 12:
        kill_Chromium_process()
        return chromium_instance()
    