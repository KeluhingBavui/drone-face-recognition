from djitellopy import tello
from time import sleep
 
me = tello.Tello()
me.connect() #Establish connection to drone
print(me.get_battery()) #Get the battery percentage

me.takeoff()
me.send_rc_control(0, 50, 0, 0) #Move forward 50cm

sleep(2)

me.send_rc_control(0, 0, 0, 30) #Rotate 30cm to the right

sleep(2)

me.send_rc_control(0, 0, 0, 0)
me.land() #Land