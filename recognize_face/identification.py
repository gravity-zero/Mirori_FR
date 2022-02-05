from tkinter.ttk import Style

import face_recognition
import cv2
import numpy as np
import os
import time
from sty import fg, bg, ef, rs, Style, RgbFg


class identify:
    font = cv2.FONT_HERSHEY_DUPLEX
    color = (255, 255, 255)
    fg.orange = Style(RgbFg(255, 150, 50))

    def __init__(self, entree, embedding_file, name_file, width_max=320, tolerance=0.55):
        self.ratio = None
        self.face_distances = None
        self.frame = None
        self.face_names = None
        self.face_locations = None
        self.entree = entree
        self.width_max = width_max
        self.tolerance = tolerance

        if not os.path.exists(embedding_file):
            print("Fichier", embedding_file, "non trouvé")
            quit()
        if not os.path.exists(name_file):
            print("Fichier", name_file, "non trouvé")
            quit()
        self.known_face_encodings = np.load(embedding_file)
        self.known_face_names = np.load(name_file)
        print("Fichier Trouvé", embedding_file)

        if entree.split(':')[0] == "file":
            fichier = entree.split(':')[1]
            if not os.path.exists(fichier):
                print("Fichier", fichier, "non trouvé")
                quit()
            self.video_capture = cv2.VideoCapture(fichier)
        else:
            print("Entree inconnue")
            quit()

    def read(self):
        if self.video_capture is not None:
            ret, self.frame = self.video_capture.read()
        else:
            while True:
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                if not color_frame:
                    continue
                break
            self.frame = np.array(color_frame.get_data())

    def analyse(self):
        frame = self.frame
        if (frame is not None) and (frame.shape[1] > self.width_max):
            self.ratio = self.width_max / frame.shape[1]
            frame_to_analyse = cv2.resize(frame, (0, 0), fx=self.ratio, fy=self.ratio)
        else:
            self.ratio = 1
            frame_to_analyse = frame

        self.face_locations = face_recognition.face_locations(frame_to_analyse)
        face_encodings = face_recognition.face_encodings(frame_to_analyse, self.face_locations)
        self.face_names = []
        self.face_distances = []
        for face_encoding in face_encodings:
            distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            if np.min(distances) < self.tolerance:
                best_match_index = np.argmin(distances)
                name = self.known_face_names[best_match_index]
            else:
                name = "Inconnu"
            self.face_names.append(name)
            self.face_distances.append(np.min(distances))


mirror_snapshot = identify("file:images_to_test/den1.jpg", "face_encodings.npy", "face_names.npy")

while True:
    mirror_snapshot.read()
    mirror_snapshot.analyse()
    print("STARTING RECOGNIZE PROGRAM")
    i = 1
    for name, distance in zip(mirror_snapshot.face_names, mirror_snapshot.face_distances):
        if mirror_snapshot.face_names and len(mirror_snapshot.face_names) == 1:
            distance_color = fg.green + str(round(distance, 2)) + fg.rs if distance > 0.4 else (
                fg.yellow + str(round(distance, 2)) + fg.rs if distance > 0.3 else fg.orange + str(
                    round(distance, 2)) + fg.rs)
            print("RESULT-> ", fg.green + name + fg.rs)
            print('distance:', distance_color)
        else:
            if i == 1:
                print(fg.red + "ERROR MORE THAN ONE FACE TO COMPARE" + fg.rs)
            print("RESULT "+str(i)+":", fg.green + name + fg.rs if name != "Inconnu" else fg.red + name + fg.rs)
            i += 1
    print("ENDING RECOGNIZE PROGRAM")
    quit()
