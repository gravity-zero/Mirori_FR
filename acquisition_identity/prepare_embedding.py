import face_recognition
import numpy as np
import os
import glob
import sys
sys.path.append('../')
from services import ssh_scp as conn

def encoding_image(dir_identites):

    face_encodings=[]
    face_names=[]

    #Comment next line : scp_download for test
    #conn.scp_download('mirori_faces/*', "../npy_files/")

    is_npy_file = os.path.isfile('../npy_files/face_names.npy')

    if is_npy_file:
        npyFaceName = np.load('../npy_files/face_names.npy')
        npyFaceEncode = np.load('../npy_files/face_encodings.npy')


    id=1
    for dir_identite in os.listdir(dir_identites):
        print("ID", id)
        id+=1

        fichiers=[]
        for ext in ["*.jpg", "*.jpeg", "*.png"]:
            fichiers.extend(glob.glob(dir_identites+dir_identite+"/"+ext))
        if len(fichiers)==0:
            print("Empty Folder", dir_identite)
            continue
        for fichier in fichiers:
            filename = dir_identite.replace('_', ' ')
            print(fichier)
            if is_npy_file and filename not in npyFaceName or not is_npy_file:
                image=face_recognition.load_image_file(fichier)
                embedding=face_recognition.face_encodings(image)[0]
                face_encodings.append(embedding)
                face_names.append(filename)

    
    
    if is_npy_file and len(face_names) > 0 :
        for faceEncoding in face_encodings:            
            np.save("../npy_files/face_encodings", np.array(np.append(npyFaceEncode, faceEncoding)))
            print('Append encoding new face')
        print(face_names)
        for faceName in face_names: 
            np.save("../npy_files/face_names", np.array(np.append(npyFaceName, faceName)))
            print('Append new face', faceName, '\n')
        print('New array', np.load('face_names.npy'))
            
    elif len(face_names) > 0 :
        np.save("../npy_files/face_encodings", np.array(face_encodings))
        print('encoding all faces', embedding)
        np.save("../npy_files/face_names", np.array(face_names))
        print('Add all face names', face_names) 
    conn.scp_upload('../npy_files/face_encodings.npy')
    conn.scp_upload('../npy_files/face_names.npy')