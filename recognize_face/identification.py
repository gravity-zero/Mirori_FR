import face_recognition
import cv2
import numpy as np
import os
import time

class identify:
    font=cv2.FONT_HERSHEY_DUPLEX
    color=(255, 255, 255)

    def __init__(self, entree, embedding_file, name_file, width_max=320, tolerance=0.55):
        self.entree=entree
        self.width_max=width_max
        self.tolerance=tolerance

        if not os.path.exists(embedding_file):
            print("Fichier", embedding_file, "non trouvé")
            quit()
        if not os.path.exists(name_file):
            print("Fichier", name_file, "non trouvé")
            quit()
        self.known_face_encodings=np.load(embedding_file)
        self.known_face_names=np.load(name_file)
        print("Fichier Trouvé", embedding_file)

        if entree.split(':')[0]=="file":
            fichier=entree.split(':')[1]
            if not os.path.exists(fichier):
                print("Fichier", fichier, "non trouvé")
                quit()
            self.video_capture=cv2.VideoCapture(fichier)
        else:
            print("Entree inconnue")
            quit()

    def read(self):
        if self.video_capture is not None:
            ret, self.frame=self.video_capture.read()
        else:
            while True:
                frames=self.pipeline.wait_for_frames()
                color_frame=frames.get_color_frame()
                if not color_frame:
                    continue
                break
            self.frame=np.array(color_frame.get_data())

    def analyse(self):
        frame=self.frame
        if frame is not None:
            frame.shape[1]>self.width_max
            self.ratio=self.width_max/frame.shape[1]
            
            frame_to_analyse=cv2.resize(frame, (0, 0), fx=self.ratio, fy=self.ratio)
        else:
            self.ratio=1
            frame_to_analyse=frame
            
        self.face_locations=face_recognition.face_locations(frame_to_analyse)
        face_encodings=face_recognition.face_encodings(frame_to_analyse, self.face_locations)
        self.face_names=[]
        self.face_distances=[]
        for face_encoding in face_encodings:
            
            distances=face_recognition.face_distance(self.known_face_encodings, face_encoding)
            if np.min(distances)<self.tolerance:
                best_match_index=np.argmin(distances)
                name=self.known_face_names[best_match_index]
            else:
                name="Inconnu"
            self.face_names.append(name)
            self.face_distances.append(np.min(distances))
        
    def render(self):
        self.frame_render=self.frame
        for (top, right, bottom, left), name, distance in zip(self.face_locations, self.face_names, self.face_distances):
            top   =int(top    /self.ratio)
            right =int(right  /self.ratio)
            bottom=int(bottom /self.ratio)
            left  =int(left   /self.ratio)
            cv2.rectangle(self.frame_render, (left, top), (right, bottom), self.color, 2)
            msg="[{:4.2f}] {}".format(distance, name)
            cv2.putText(self.frame_render, msg, (left, int(bottom+(bottom-top)*0.2)), self.font, 0.8, self.color, 1)
        
#miror_snapshot=identify("realsense", "face_encodings.npy", "face_names.npy")
#miror_snapshot=identify("https://www.youtube.com/watch?v=m_xWEofOqHI", "face_encodings.npy", "face_names.npy")
#miror_snapshot=identify("csi", "face_encodings.npy", "face_names.npy")
miror_snapshot=identify("file:images_to_test/tm.jpg", "face_encodings.npy", "face_names.npy")

while True:
    miror_snapshot.read()
    miror_snapshot.analyse()
    print("START TEST")
    for name, distance in zip(miror_snapshot.face_names, miror_snapshot.face_distances):
        print("RESULT ->   ", name, distance)
    miror_snapshot.render()
    cv2.imshow("Frame render", miror_snapshot.frame_render)

    key=cv2.waitKey(1)&0xFF
    if key == ord('q'):
        break
    if key==ord('a'):
        for i in range(100):
            miror_snapshot.read()
    if key==ord('z'):
        for i in range(2000):
            miror_snapshot.read()
    print("END TEST")

#cv2.destroyAllWindows()