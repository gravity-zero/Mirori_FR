import cv2
import face_recognition
import sys 
import os

sys.path.append('../')

#from services import ssh
from services import ssh_scp as conn

############### UPLOAD ##################

#conn.scp_upload('./face_encodings.npy')
#conn.scp_upload('./face_names.npy')

############### DOWNLOAD ##################

#conn.scp_download('mirori_faces/*', "./")
#print(conn.ssh_command("ls -l mirori_faces/"))

##################################################################

video_capture = cv2.VideoCapture(0)

face_locations = []

id=1 #API CALL 
print("SPACE BAR FOR TAKING A REFERENCE FACE IMAGE")
print("ESC FOR EXIT")
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()  # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]  # Find all the faces in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)  # Display the results
    for top, right, bottom, left in face_locations:
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Display the resulting image
        cv2.imshow('Video', frame)
        
    key = cv2.waitKey(1)
    
    if key & key % 256 == 27:
        # ESC pressed for Quit
        video_capture.release()
        cv2.destroyAllWindows()
        break
    elif key & key % 256 == 32:
        # SPACE pressed for Screenshot
        img_name = "identity.png"
        parent_folder = "../identified/"
        folder = str(id) + "/"
        path = os.path.join(parent_folder, folder)
        filename = path + img_name
        if not os.path.exists(filename):
            os.mkdir(path, 0o755)
        cv2.imwrite(path + img_name, frame)
        video_capture.release()
        cv2.destroyAllWindows()

        if os.path.exists(filename):
            import prepare_embedding as pe

            pe.encoding_image(parent_folder)
            print("REFERENCE IMAGE TAKEN for", id)
            id+=1
        else:
            print("IMAGE DOESN'T EXISTS, SOMETHING WENT WRONG")
        break
    