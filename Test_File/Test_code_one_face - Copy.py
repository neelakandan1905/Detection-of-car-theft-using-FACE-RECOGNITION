import cv2
import face_recognition
import numpy as np
import os
#Encoding Neelakandan Face
img_neela= face_recognition.load_image_file('D:/PROJECT/Car_theft/Face_Reco_HOG/Test_File/Neelakandan.jpg')
img_neela= cv2.cvtColor(img_neela,cv2.COLOR_BGR2RGB)
face_loc_neela = face_recognition.face_locations(img_neela)[0]
encode_neela= face_recognition.face_encodings(img_neela)[0]
#Rectangle in Neelakandan Face
# startPoint = (face_loc_neela[3], face_loc_neela[0])
# endPoint = (face_loc_neela[1], face_loc_neela[2])
# color =  (255, 0, 0)
# thickness = 2
# cv2.rectangle(face_loc_neela, startPoint, endPoint, color, thickness)
# cv2.imshow('Unit_Testing', face_loc_neela)

# Path defined
path= 'D:/PROJECT/Car_theft/Face_Reco_HOG/Test_File/Test_image/'
images = []
test_names = []
test = os.listdir('D:/PROJECT/Car_theft/Face_Reco_HOG/Test_File/Test_image/')
#print(test)

#Take images from folder and loop
for tst in test:
    curimg = cv2.imread(f"{path}{tst}")
    images.append(curimg)
    #Removes Extension
    test_names.append(os.path.splitext(tst)[0])
#print(test_names)

def findEncodings(images):
    # encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_loc = face_recognition.face_locations(img)
        encodes = face_recognition.face_encodings(img)
        #To find Multiple Faces(Array)
        for index, encode in enumerate(encodes):
            results = face_recognition.compare_faces([encode_neela], encode)
            face_dist = face_recognition.face_distance([encode_neela], encode)
            #Draw rectangle
            # startPoint = (face_loc[index][3], face_loc[index][0])
            # endPoint = (face_loc[index][1], face_loc[index][2])
            # color =  (255, 0, 0)
            # thickness = 2
            # #For loop for finding image
            # cv2.rectangle(img, startPoint, endPoint, color, thickness)
            print(results, face_dist)
            # cv2.imshow('Unit_Testing', img)
        # encodeList.append(encode)
    # return encodeList

findEncodings(images)
cv2.waitKey(0)
