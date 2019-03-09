
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
L_straight = 160
R_straight = 167




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
    
def distance_slice(lidar_data, angle, spread):
    x = lidar_data[:,1] - angle
    x = np.abs(x)
    minim = np.where(x == np.min(x))[0][0]
    low = minim-spread
    
    high = minim + spread
    dist = lidar_data[low:high,0]

    if dist == []:
        distance_slice(lidar_data, angle, spread)
    
    return dist
    
def driveRight(x,increase):
    delta = x + increase
    return right.Drive(0,delta)
    
def driveLeft(x,increase):
    delta = x + increase
    return left.Drive(0,delta)
    
###################################

try:
    ########
    # Move out of corner and approach center
    #######
    
    right.Drive(0,0)
    left.Drive(1,160)
    x = data(lidar.getPoints(ser, polar = True))

    print(x[0,0])
    while ((x[0,0] > 1000 and x[0,0] <2000) == False):
        print('turning to center')
        if x[0,0] > 1000 and x[0,0] <2000:
            break
        else:
            x = data(lidar.getPoints(ser, polar = True))

            print(x[0,0])
            
    print('turned to center')
    right.Drive(0,0)
    left.Drive(1,0)

    sleep(.5)

    
    print(x[0,0])
    while(x[0,0] > 600):
        right.Drive(0,R_straight)
        left.Drive(1,L_straight)
        x = data(lidar.getPoints(ser, polar = True))

        print(x[0,0])

        
    #zero point turn    
##    right.Drive(0,0)
##    left.Drive(1,L_straight)
    
    x = data(lidar.getPoints(ser, polar = True))
    angle = angle_calc(x,325)
    
##    while(x[angle,1] > 275):
##        x = data(lidar.getPoints(ser, polar = True))
##        angle = angle_calc(x,270)


    right.Drive(0,R_straight)
    left.Drive(0,L_straight)

    while(x[angle, 0] > 1000):
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

        
##        x = data(lidar.getPoints(ser, polar = True))
##        deg_225 = angle_calc(x,265)
##        deg_325 = angle_calc(x,275)
##        
##        right.Drive(0,R_straight)
##        left.Drive(1,L_straight)
##
##        while x[deg_225,0] < 1000:
##            print('i see the center')
##            x = data(lidar.getPoints(ser, polar = True))
##            deg_225 = angle_calc(x,225)
##
##        
##        right.Drive(0,0)
##        left.Drive(1,L_straight)
##        x = data(lidar.getPoints(ser, polar = True))
##        deg_325 = angle_calc(x,325)
        
##        while x[deg_225,0] > 1000:
##            print('turning towards center')
##            x = data(lidar.getPoints(ser, polar = True))
##            deg_225 = angle_calc(x,325)
        
        
        
############################################################################ 
        dist_low = 200
        dist_high = 1000
        slice_width = 1
        slice_angle = 290
        turn_modify = 0
        orbit_corr = 0
        R_turn = 0
        L_turn = 0
        
        right.Drive(0,R_straight)
        left.Drive(1,L_straight + orbit_corr)

        x = data(lidar.getPoints(ser, polar = True))
        dist2 = distance_slice(x, slice_angle, slice_width)
##        dist1 = distance_slice(x, slice_angle, slice_width)

##        while(np.min(dist2) > dist_low and np.average(dist2) < dist_high):
        while np.min(dist2) < 900:
            x = data(lidar.getPoints(ser, polar = True))
            dist2 = distance_slice(x, slice_angle, slice_width)
            print('I see the center')
##
        while np.min(dist2) > 900:
            right.Drive(0,0)
            left.Drive(1,L_straight)
            x = data(lidar.getPoints(ser, polar = True))
            dist2 = distance_slice(x, slice_angle, slice_width)
            print('turning towards center')
        
        
##        if np.min(dist2) < dist_low:
####            driveRight(R_straight,turn_modify)
##            right.Drive(0,R_straight + turn_modify)
##            left.Drive(0,L_straight)
##            print('too close')
##        elif np.min(dist2) > dist_high:
####            driveLeft(L_straight,turn_modify)
##            right.Drive(0,R_straight)
##            left.Drive(0,L_straight + turn_modify)
##            print('too far')


########################################################################################
            
    
    
except KeyboardInterrupt:
    print("Exiting")

    right.Drive(0,0)
    left.Drive(0,0)
    left.Stop()
    right.Stop()
