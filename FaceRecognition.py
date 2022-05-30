import cv2
import numpy as np

def FindFace(img):
    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml") #Use haarcaascade for recognition library
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Change image to grayscale
    faces = faceCascade.detectMultiScale(imgGray,1.2,8)

    myFaceListC = [] #Holds the x,y of where the face is detected
    myFaceListArea = [] #Holds the area information of the detected faces

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) #Make rectangle when detect a face
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        myFaceListC.append([cx,cy])
        myFaceListArea.append(area)

    #Return the nearest face to the camera(face with biggest area)
    #Else return nothing
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i],myFaceListArea[i]]
    else:
        return img, [[0,0],0]

#--Running the webcam--#
cap = cv2.VideoCapture(0) #0 is main webcam
while True:
    _, img = cap.read() #Get image
    img, info = FindFace(img)
    print("Center:",info[0],"Area:",info[1])
    cv2.imshow("Output", img) #Create window to output image
    cv2.waitKey(1) #Delay