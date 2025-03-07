import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
from PIL import Image

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('mouth.xml')
nose_cascade = cv2.CascadeClassifier('nariz.xml')
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture('Sample_video.mov')
anterior = 0

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # sub_face = frame[y:y+h, x:x+w]
        # FaceFileName = "unknownfaces/face_" + str(y) + ".jpg"
        # cv2.imwrite(FaceFileName, sub_face)
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        mouth = mouth_cascade.detectMultiScale(roi_gray)
        nose = nose_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(22,255,0),2)
            for (mx,my,mw,mh) in mouth:
                cv2.rectangle(frame,(mx,my),(mx+mw,my+mh),(122,255,0),2)
                for (nx,ny,nw,nh) in nose:
                    cv2.rectangle(frame,(nx,ny),(nx+nw,ny+nh),(0,255,111),2)
                    sub_face = frame[y:y+h, x:x+w]
                    FaceFileName = "unknownfaces/face_" + str(y) + ".jpg"
                    cv2.imwrite(FaceFileName, sub_face)

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
