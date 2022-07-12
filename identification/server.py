from flask import Flask
import identification as ident
import auto_screenshot as ascreen
from sty import fg
from os import getenv
from services import ssh_scp as conn, virtualmouse as virtual, browser as bi
from dotenv import load_dotenv
import requests

load_dotenv("/home/grav/Bureau/Mirori_FR/.env")

def waiting_route():
    return getenv("front_route") + "visitors/standbyMode"

def fr_in_progress():
    return getenv("front_route") + "visitors/facialRecognitionLoading"

def fr_failed_qr_code():
    return getenv("front_route") + "visitors/facialRecognitionFailed"

def api_call(user_id):
    back_route = getenv("back_route")
    api_key = getenv("api_key")
    data = {"id": user_id, "api_key": api_key}
    composed_route = back_route + "auth/login"
    response = requests.post(composed_route, data=data)

    if response.status_code != 200:
        print("Erreur avec l'API, email inconnue ?", response, flush=True)
        return False

    res = response.json()

    if not res["token"]:
        print("API DON'T RETURN Token, response: ", res, flush=True)
        return False

    jwt_token = res["token"]
    print(jwt_token, flush=True)
    return jwt_token

print("Start chromium_instance")
global browser
browser = bi.chromium_instance() # We close all existents instance & start new one
browser.get(waiting_route())

def open_cms(jwt):
    browser.get(getenv("front_route")+"visitors/authFacialRecognition/"+jwt)

def launch(test=0):
    if test < 3:
        #We take a screenshot
        
        result = ascreen.screenshot()
        
        if result is not None:
            #We need to init this program from the program where we take the screenshot sample
            conn.scp_download('mirori_faces/*', "/home/grav/Bureau/Mirori_FR/identification/npy_files/")
            mirror_snapshot = ident.identify("file_location:/home/grav/Bureau/Mirori_FR/identification/images_to_test/identity.jpeg", "/home/grav/Bureau/Mirori_FR/identification/npy_files/face_encodings.npy", "/home/grav/Bureau/Mirori_FR/identification/npy_files/face_names.npy")
           
            mirror_snapshot.read()
            mirror_snapshot.analyse()
            print("STARTING RECOGNIZE PROGRAM", flush=True)
            i = 1
            for name, distance in zip(mirror_snapshot.face_names, mirror_snapshot.face_distances):
                if name != "Inconnu":
                    #Check if we have more than one face
                    if mirror_snapshot.face_names and len(mirror_snapshot.face_names) == 1:
                        distance_color = fg.orange + str(round(distance, 2)) + fg.rs if distance > 0.5 else (
                            fg.yellow + str(round(distance, 2)) + fg.rs if distance > 0.4 else fg.green + str(
                                round(distance, 2)) + fg.rs)
                        print("RESULT-> ", fg.green + name + fg.rs, flush=True)
                        print('distance:', distance_color, flush=True)
                        #Release video capture from identify class
                        mirror_snapshot.stop()
                        print("SUCCESS", flush=True)
                        return name
                    else:
                        #We have more than one face to compare, we need to take a new screenshot
                        if i == 1:
                            print(fg.red + "ERROR MORE THAN ONE FACE TO COMPARE" + fg.rs, flush=True)
                        print("RESULT "+str(i)+":", fg.green + name + fg.rs if name != "Inconnu" else fg.red + name + fg.rs, flush=True)
                        i += 1
                        launch(test+1)
                else:
                    distance_color = fg.orange + str(round(distance, 2)) + fg.rs if distance > 0.5 else (
                            fg.yellow + str(round(distance, 2)) + fg.rs if distance > 0.4 else fg.green + str(
                                round(distance, 2)) + fg.rs)
                    print("RESULT-> ", fg.green + name + fg.rs, flush=True)
                    print('distance:', distance_color, flush=True)
                    launch(test+1)
            quit()
        else:
            print("SCREENSHOT ERROR", flush=True)
            launch(test+1)
    else:
        print("MESSAGE QR Code", flush=True)
        browser.get(fr_failed_qr_code())
        return False
        

app = Flask(__name__)
@app.route("/", methods=['GET'])
def index():
    #
    #chome fr in progress
    browser.get(fr_in_progress())
    #déclencheur
    id = launch()
    print(id, flush=True)
    if not id:
        return "QRCODE"
    jwt = api_call(id) #if fail return QRCODE
    if not jwt:
        return "QRCODE"
    open_cms(jwt)
    return "OK"

    

@app.route("/virtual_mouse", methods=['GET'])
def vm_start():
    print("Virtual mouse", flush=True)
    global VirtualM
    VirtualM = virtual.Mouse()
    VirtualM.main()

@app.route("/waiting_mode", methods=['GET'])
def waiting_page():
    browser.get(waiting_route())
    return "WAITING PAGE"

@app.route("/default_qr_code", methods=['GET'])
def def_qr_code():
    browser.get(fr_failed_qr_code())
    return "QR CODE LAUNCHED"

@app.route("/user_finished", methods=['GET'])
def stop_user_experience():
    global VirtualM # we use global for get instance of virtual mouse
    VirtualM.stop() # kill process get error
    del VirtualM
    #sbc.set_brightness(0)
    return "STOP"
    
if __name__ == "__main__":
 app.run(host="127.0.0.1", port=5500, debug=True)

