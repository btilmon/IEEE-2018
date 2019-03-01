
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
L_straight = 255
R_straight = 243


def data(lidar_data):
    x = lidar_data
    x[np.where(x[:,0] == 0),0] = 3000
    return x

def angle_calc(lidar_data, angle):
    x = lidar_data[:,1] - angle
    x = np.abs(x)
    minim = np.where(x == np.min(x))[0][0]
    return minim


try:
    
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
            
    print('turned to kabba amen')
    right.Drive(0,0)
    left.Drive(0,0)

    sleep(.5)

    
    print(x[0,0])
    while(x[0,0] > 300):
        right.Drive(0,R_straight)
        left.Drive(0,L_straight)
        x = data(lidar.getPoints(ser, polar = True))

        print(x[0,0])
        
    right.Drive(0,0)
    left.Drive(0,0)
    print('reached kabba!')
    
    x = data(lidar.getPoints(ser, polar = True))

    angle = angle_calc(x,270)
  
    print('distance',x[angle,0])
    print('angle',x[angle,1])
    
    while(x[angle, 0] > 300):

        left.Drive(0,255)
        x = data(lidar.getPoints(ser, polar = True))
        angle = angle_calc(x,270)
        print('distance in loop',x[angle,0])
        print('angle in loop',x[angle,1])

    while(0==0):
        left.Drive(0,255)
        right.Drive(0,255)
    
    right.Drive(0,0)
    left.Drive(0,0)
    left.Stop()
    right.Stop()
    
except KeyboardInterrupt:
    print("Exiting")

    right.Drive(0,0)
    left.Drive(0,0)
    left.Stop()
    right.Stop()
