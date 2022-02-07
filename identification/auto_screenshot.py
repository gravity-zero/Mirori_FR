import cv2
import face_recognition
import os
import time

def screenshot():
    video_capture = cv2.VideoCapture(0)

    face_locations = []

    while video_capture:
        # Grab a single frame of video
        ret, frame = video_capture.read()  # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]  # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)  # Display the results
        print(face_locations)
        time.sleep(0.500)

        #Wait before taking face screenshot
        img_name = "identity.png"
        parent_folder = "images_to_test/"
        
        filename = parent_folder + img_name
        
        if os.path.exists(filename):
            os.remove(filename)
        cv2.imwrite(filename, frame)
        video_capture.release()
        cv2.destroyAllWindows()
        return "SCREENSHOT TAKEN"
        
