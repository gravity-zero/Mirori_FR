import face_recognition

file_name = "romain feregotto"

known_image = face_recognition.load_image_file("../our_faces/romain feregotto.png")
unknown_image = face_recognition.load_image_file("images_to_test/image.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

if results:
    print("result=", file_name)