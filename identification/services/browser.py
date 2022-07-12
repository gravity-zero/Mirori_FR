from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.chrome.options import Options
import http.client as httplib
import socket
from os import system 
import subprocess

def launch_chromium():
    chrome_options = Options()
    chrome_options.add_argument("--kiosk")
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
    #system("while pgrep chrome ; do pkill chrome ; done")
    #subprocess.run("while pgrep chrome ; do pkill chrome ; done", capture_output=False, shell=False)
    system("killall chrome")
    return True


def chromium_instance():
    cmd = "ps aux | pgrep chrome | wc -l"
    exec_cmd = subprocess.run(cmd, capture_output=True, shell=True)
    nb_instance= int(exec_cmd.stdout.decode())
    
    print("NB instance =", nb_instance, flush=True)
    if nb_instance >= 21:
        print("Kill Chromium", flush=True)
        kill_Chromium_process()
    
    return launch_chromium()
    
    