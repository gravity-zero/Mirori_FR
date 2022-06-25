import face_recognition
from cv2 import VideoCapture, FONT_HERSHEY_DUPLEX, resize, destroyAllWindows
import numpy as np
import os
from sty import fg, RgbFg, Style


class identify:
    font = FONT_HERSHEY_DUPLEX
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
        print("Fichiers Trouvés", embedding_file, name_file)

        if entree.split(':')[0] == "file_location":
            fichier = entree.split(':')[1]
            print(os.curdir)
            if not os.path.exists(fichier):
                print("Fichier", fichier, "non trouvé")
                quit()
            self.video_capture = VideoCapture(fichier)
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

    def stop(self):
        self.video_capture.release()
        destroyAllWindows()

    def analyse(self):
        frame = self.frame
        if (frame is not None) and (frame.shape[1] > self.width_max):
            self.ratio = self.width_max / frame.shape[1]
            frame_to_analyse = resize(frame, (0, 0), fx=self.ratio, fy=self.ratio)
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


