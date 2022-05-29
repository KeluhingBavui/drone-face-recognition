from djitellopy import tello
import cv2
 
me = tello.Tello()
me.connect() #Establish connection to drone
print(me.get_battery()) #Get the battery percentage

me.streamon() #Will give us all frames 1 by 1 to be processed

while True:
    img = me.get_frame_read().frame #Gives individual image coming from the drone
    img = cv2.resize(img, (360,240)) #Resize the image(smaller the faster)
    cv2.imshow("Image",img) #Creates a window to display the image
    cv2.waitKey(1) #Give delay so frame does not close on us
    