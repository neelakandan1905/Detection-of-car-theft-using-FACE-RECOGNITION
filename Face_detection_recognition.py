import cv2
import numpy as np
import pyrebase
import face_recognition
import os
import requests
import datetime
import Constants

while True:
    unknown_face_count = 0
    unknown_count = 5  # Assigning number of seconds that the system should detect unknown face to send message
    known_count = 3

    path = 'Images'
    images = []
    classNames = []
    myList = os.listdir(path)
    # print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])


    # print(classNames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    encodeListKnown = findEncodings(images)
    # print('Encoding Complete', encodeListKnown)

    cap = cv2.VideoCapture(0)
    c = 0
    flag = True

    chat_id = str(Constants.check_list[0][1])

    while flag:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            print(matchIndex)
            print(faceDis[matchIndex])

            if faceDis[matchIndex] < 0.50:
                name = classNames[matchIndex].upper()
                print(classNames[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                if known_count == 5:
                    x = datetime.datetime.now()
                    Day, meridiem, time, date = x.strftime("%A"), x.strftime("%p"), x.strftime("%X"), x.strftime(
                        "%x").lstrip()
                    time = list(time.split(':'))
                    time.pop()
                    exact_time = ':'.join(time)
                    d = datetime.datetime.strptime(exact_time, "%H:%M")
                    exact_time = d.strftime("%I:%M %p")
                    string = "Welcome {}!\nLogin details - \n".format(classNames[matchIndex])
                    total = string + date + ' ' + Day + ' ' + exact_time

                    requests.post(
                        "https://api.telegram.org/[YOUR_BOT_TOKEN]"
                        "/sendMessage?chat_id={}&text={}".format(chat_id, total))

                known_count += 1

            else:
                name = 'UNKNOWN'
                unknown_face_count += 1
                print(name, unknown_face_count)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                # if the driver's face identified as unknown for 5 seconds then
                # it will send the message to telegram
                if 5 < unknown_face_count < 11:
                    c += 1
                    unknown_img = "Unknown/UnknownPerson-{}.jpg".format(c)
                    cv2.imwrite(unknown_img, img)

                    # Here Total number of images that will be send to the owner is 5
                    if c == unknown_count:
                        cap.release()
                        cv2.destroyAllWindows()

                        requests.post(
                            "https://api.telegram.org/[YOUR_BOT_TOKEN]"
                            "/sendMessage?chat_id={}&text=Alert your car is not safe>>>".format(chat_id))

                        for i in range(1, c + 1):
                            folder = "Unknown/UnknownPerson-{}.jpg".format(i)
                            files = {'photo': open(folder, 'rb')}
                            requests.post(
                                "https://api.telegram.org/[YOUR_BOT_TOKEN]"
                                "/sendphoto?chat_id={}".format(chat_id),
                                files=files)

            if c == unknown_count:
                flag = False
                break
        if c != unknown_count:
            cv2.imshow('Webcam', img)
            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27 or cv2.waitKey(1) == ord('q'):
                break

    if c == unknown_count:
        print("\n [INFO] Exiting Program and cleanup stuff")
        cap.release()
        cv2.destroyAllWindows()
        break

