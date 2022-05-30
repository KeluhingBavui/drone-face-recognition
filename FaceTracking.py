import cv2
import numpy as np
from djitellopy import tello
from time import sleep

me = tello.Tello()
me.connect() #Establish connection to drone
print(me.get_battery()) #Get the battery percentage

me.streamon() #Will give us all frames 1 by 1 to be processed
me.takeoff()

#--Uncomment these lines if drone didnt take off high enough from the floor--#
#me.send_rc_control(0, 0, 25, 0) #Go up at speed of 25
#sleep(2.2) #Go up at 2.2 seconds

w, h = 360, 240
fbRange = [6200, 6800] #Forward and backward range
pid = [0.4, 0.4, 0]
pError = 0 #Previous error

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
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i],myFaceListArea[i]]
    else:
        return img, [[0,0],0]

#--Function for drone to track/follow the face--#
def trackFace(info, w, pid, pError):
    area = info[1]
    x,y = info[0]
    fb = 0

    error = x - w // 2 #Find the deviation of the image from the center
    speed = pid[0] * error + pid[1] * (error-pError)
    speed = int(np.clip(speed,-100,100))

    if area > fbRange[0] and area < fbRange[1]: #To remain stationary
        fb = 0
    elif area>fbRange[1]: #If too far go forwards
        fb = -20
    elif area < fbRange[0] and area != 0: #If too near go backwards
        fb = 20

    if x == 0:
        speed = 0
        error = 0
    me.send_rc_control(0, fb, 0, speed) #Send control to drone
    
    return error

#--Driver code--#
while True:
    img = me.get_frame_read().frame #Gives individual image coming from the drone
    img = cv2.resize(img,(w,h))
    img, info = FindFace(img)
    pError = trackFace(info, w, pid, pError)
    cv2.imshow("Output", img) #Create window to output image

    #This code is for safety, if we press the q button, it will land
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break