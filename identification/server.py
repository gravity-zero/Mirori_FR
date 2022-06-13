from flask import Flask
import identification as ident
import auto_screenshot as ascreen
from sty import fg
import requests

from os import path, system

import sys
#sys.path.append('../')
from services import ssh_scp as conn, virtualmouse as virtual

def launch(test=0):
    if test < 3:
        #We take a screenshot
        
        result = ascreen.screenshot()
        
        if result is not None:
            #We need to init this program from the program where we take the screenshot sample
            conn.scp_download('mirori_faces/*', path.abspath("/home/grav/Bureau/Mirori_FR/npy_files")+"/")
            mirror_snapshot = ident.identify("file_location:/home/grav/Bureau/Mirori_FR/identification/images_to_test/identity.png", "/home/grav/Bureau/Mirori_FR/npy_files/face_encodings.npy", "/home/grav/Bureau/Mirori_FR/npy_files/face_names.npy")

            mirror_snapshot.read()
            mirror_snapshot.analyse()
            print("STARTING RECOGNIZE PROGRAM")
            i = 1
            for name, distance in zip(mirror_snapshot.face_names, mirror_snapshot.face_distances):
                if name != "Inconnu":
                    #Check if we have more than one face
                    if mirror_snapshot.face_names and len(mirror_snapshot.face_names) == 1:
                        distance_color = fg.orange + str(round(distance, 2)) + fg.rs if distance > 0.5 else (
                            fg.yellow + str(round(distance, 2)) + fg.rs if distance > 0.4 else fg.green + str(
                                round(distance, 2)) + fg.rs)
                        print("RESULT-> ", fg.green + name + fg.rs)
                        print('distance:', distance_color)
                        #Release video capture from identify class
                        mirror_snapshot.video_capture.release()
                        return name
                    else:
                        #We have more than one face to compare, we need to take a new screenshot
                        if i == 1:
                            print(fg.red + "ERROR MORE THAN ONE FACE TO COMPARE" + fg.rs)
                        print("RESULT "+str(i)+":", fg.green + name + fg.rs if name != "Inconnu" else fg.red + name + fg.rs)
                        i += 1
                        launch(test+1)
                else:
                    distance_color = fg.orange + str(round(distance, 2)) + fg.rs if distance > 0.5 else (
                            fg.yellow + str(round(distance, 2)) + fg.rs if distance > 0.4 else fg.green + str(
                                round(distance, 2)) + fg.rs)
                    print("RESULT-> ", fg.green + name + fg.rs)
                    print('distance:', distance_color)
                    launch(test+1)

            print("ENDING RECOGNIZE PROGRAM")
            quit()
        else:
            print("SCREENSHOT ERROR")
    else:
        print("MESSAGE QR Code")


app = Flask(__name__)
@app.route("/", methods=['GET'])
def index():
 #déclencheur
    name = launch()
    print(name)
    if name:
        print("Launch Chromium & virtual mouse")
        VirtualM = virtual.Mouse()
        VirtualM.main()
        print("CLOSE PROGRAM")
        return "OK"
    
if __name__ == "__main__":
 app.run(host="127.0.0.1", port=5500, debug=True)

system("curl -G http://127.0.0.1:5500")

