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

try:
    right.Drive(0,255)
    left.Drive(0,200)

#    for i in range(0,2):
    x = lidar.getPoints(ser, polar = True)
#        print(x)
    while ((x[0,0] > 1000 and x[0,0] <2000) == False):
        if x[0,0] > 1000 and x[0,0] <2000:
            break
        else:
            x = lidar.getPoints(ser, polar = True)
            print(x[0,0])

    right.Drive(0,0)
    left.Drive(0,0)

    sleep(.5)

    right.Drive(0,255)
    left.Drive(0,255)
    
    while(x[0,0] > 100):
        if(x[0,0]<= 100):
            right.Drive(0,0)
            left.Drive(0,0)
        else:
            x = lidar.getPoints(ser, polar = True)
            print(x[0,0])

    right.Drive(0,0)
    left.Drive(0,0)
    
except KeyboardInterrupt:
    print("Exiting")
    motor.Spin(0)
    right.Drive(0,0)
    left.Drive(0,0)
    left.Stop()
    right.Stop()
