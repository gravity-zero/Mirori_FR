import identification as ident
import auto_screenshot as ascreen
from sty import fg, bg, ef, rs, Style, RgbFg

import sys
sys.path.append('../')
from services import ssh_scp as conn

def launch(test=0):
    if test < 3:
        #We take a screenshot
        result = ascreen.screenshot()
        if result is not None:
            #We need to init this program from the program where we take de screenshot sample
            conn.scp_download('mirori_faces/*', "../npy_files/")
            mirror_snapshot = ident.identify("file_location:./images_to_test/identity.png", "../npy_files/face_encodings.npy", "../npy_files/face_names.npy")

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

launch()