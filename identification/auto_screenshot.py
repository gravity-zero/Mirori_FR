
from cv2 import VideoCapture, imwrite, destroyAllWindows, CAP_V4L2
import time
import face_recognition
import os


def screenshot():
    #print(cv2.getBuildInformation())
    video_capture = VideoCapture(CAP_V4L2)

    face_locations = []

    while True:
        # Grab a single frame of video
        
        ret, frame = video_capture.read()  # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        
        #time.sleep(0.100)
        rgb_frame = frame[:, :, ::-1]  # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)  # Display the results
        print(face_locations)
        
        #Wait before taking face screenshot
        img_name = "identity.png"
        parent_folder = "images_to_test/"
        
        filename = parent_folder + img_name
        
        if os.path.exists(filename):
            os.remove(filename)
        imwrite(filename, frame)
        video_capture.release()
        destroyAllWindows()
        return "SCREENSHOT TAKEN"
        
