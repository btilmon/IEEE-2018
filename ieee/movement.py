
import scan
import Motor
import pigpio
import numpy as np
import time
import os
import LidarPrint as lp
import serial
import math
from time import sleep
import threading
from LidarPrint import *



port = "/dev/ttyUSB0"
ser = serial.Serial(port, 115200, timeout = 5)
ser.setDTR(False)
print (ser.name)
lidar = Lidar(ser) 

left = Motor.Motor(scan.m1DIR,scan.m1PWM)
right = Motor.Motor(scan.m2DIR,scan.m2PWM)
left.Inverse()

########### motor speeds#######
# straight
L_straight = 255
R_straight = 246


###############################

############ methods #########
def data(lidar_data):
    x = lidar_data
    x[np.where(x[:,0] == 0),0] = 3000
    return x

def angle_calc(lidar_data, angle):
    x = lidar_data[:,1] - angle
    x = np.abs(x)
    minim = np.where(x == np.min(x))[0][0]
    return minim
###################################

try:
    ########
    # Move out of corner and approach center
    #######
    
    right.Drive(0,255)
    left.Drive(0,200)
    x = data(lidar.getPoints(ser, polar = True))

    print(x[0,0])
    while ((x[0,0] > 1000 and x[0,0] <2000) == False):
        if x[0,0] > 1000 and x[0,0] <2000:
            break
        else:
            x = data(lidar.getPoints(ser, polar = True))

            print(x[0,0])
            
    print('turned to center')
    right.Drive(0,0)
    left.Drive(0,0)

    sleep(.5)

    
    print(x[0,0])
    while(x[0,0] > 500):
        right.Drive(0,R_straight)
        left.Drive(0,L_straight)
        x = data(lidar.getPoints(ser, polar = True))

        print(x[0,0])
        
    right.Drive(0,0)
    left.Drive(0,0)
    print('reached center!')
##    
    x = data(lidar.getPoints(ser, polar = True))
    angle = angle_calc(x,270)
    while(x[angle,1] > 275):
        x = data(lidar.getPoints(ser, polar = True))
        angle = angle_calc(x,270)


    right.Drive(0,0)
    left.Drive(0,L_straight)
    
    while(x[angle, 0] > 700):
        x = data(lidar.getPoints(ser, polar = True))
        angle = angle_calc(x,270)
        while(x[angle,1] > 275):
            x = data(lidar.getPoints(ser, polar = True))
            angle = angle_calc(x,270)
        print('distance in loop',x[angle,0])
        print('angle in loop',x[angle,1])

    ########
    # Begin circling center
    #######
    print('circling center')
    while True:
        
        right.Drive(0,R_straight)
        left.Drive(0,180)

        while(x[angle, 0] < 750):
            x = data(lidar.getPoints(ser, polar = True))
            angle = angle_calc(x,270)
            print('I see the center!')
            
            
            while(x[angle,1] > 275):
                x = data(lidar.getPoints(ser, polar = True))
                angle = angle_calc(x,270)
        print('turning towards center')        
        right.Drive(0,255)
        left.Drive(0,0)
        x = data(lidar.getPoints(ser, polar = True))
        angle = angle_calc(x,270)
        while(x[angle,1] > 275):
            x = data(lidar.getPoints(ser, polar = True))
            angle = angle_calc(x,270)

##        while(x[angle, 0] > 500 and x[angle, 0] < 700 ):
##            right.Drive(0,255)
##            left.Drive(0,0)
            
            

    
except KeyboardInterrupt:
    print("Exiting")

    right.Drive(0,0)
    left.Drive(0,0)
    left.Stop()
    right.Stop()
