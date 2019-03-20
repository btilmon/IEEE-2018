
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
ser_lidar = serial.Serial(port, 115200, timeout = 0)
ser_color = serial.Serial("/dev/ttyACM0",9600)
#### Arduino ports #####

ser_lidar.setDTR(False)
print (ser_lidar.name)
lidar = Lidar(ser_lidar)

sensors = ser_color.readline().rstrip()
data = sensors.split('^')

left = Motor.Motor(scan.m1DIR,scan.m1PWM)
right = Motor.Motor(scan.m2DIR,scan.m2PWM)
left.Inverse()

########### motor speeds#######
# straight
L_straight = 230
R_straight = 223




###############################

############ methods #########
def data(lidar_data):
    '''
    filters any emtpy values from lidar to equal 3000
    '''
    x = lidar_data
    x[np.where(x[:,0] == 0),0] = 3000
    return x

def angle_calc(lidar_data, angle):
    '''
    ratio for determining which angle to look at *pretty sure distance slice is better than this*
    '''
    x = lidar_data[:,1] - angle
    x = np.abs(x)
    minim = np.where(x == np.min(x))[0][0]
    return minim
    
def distance_slice(lidar_data, angle, spread):
    '''
    gives an array of distances based on user defined angle and angle spread 
    '''
    x = lidar_data[:,1] - angle
    x = np.abs(x)
    minim = np.where(x == np.min(x))[0][0]
    low = minim-spread
    
    high = minim + spread
    dist = lidar_data[low:high,0]
    if dist.size:
        abc = 0
    else:
        dist = 3000 * np.ones((spread*2))
    return dist
    
def driveRight(x,increase):
    delta = x + increase
    return right.Drive(0,delta)
    
def driveLeft(x,increase):
    delta = x + increase
    return left.Drive(0,delta)

def stop():
    right.Drive(0,0)
    left.Drive(0,0)

def color(raw):
    '''
    reads color sensor data from arduino
    '''
    if raw[0] == 'c':
        return 2

    
    
'''
cases:
    case 0 = move out of corner and position orthogonally to center
    case 1 = orbit around center
    case 2 = move to corner, then enter case 0, enter case 3 if all objects collected
    case 3 = move to original corner and raise flag
'''

try:
    
    case = 0
    
##    case = color(data)
    print('case is',case)
    
    #case 0
    if case == 0:
        right.Drive(0,0)
        left.Drive(1,160)
        x = data(lidar.getPoints(ser_lidar, polar = True))

        print(x[0,0])
        while ((x[0,0] > 1000 and x[0,0] <2000) == False):
            
            
##            print('case is', color(ser_color, case))
            print('turning to center')
            if x[0,0] > 1000 and x[0,0] <2000:
                break
            else:
                x = data(lidar.getPoints(ser_lidar, polar = True))

                print(x[0,0])
                
        print('turned to center')
        stop()

        sleep(.5)

        print(x[0,0])
        while(x[0,0] > 800):
            right.Drive(0,R_straight)
            left.Drive(1,L_straight)
            x = data(lidar.getPoints(ser_lidar, polar = True))

            print(x[0,0])

        x = data(lidar.getPoints(ser_lidar, polar = True))
        angle = angle_calc(x,325)
        
        right.Drive(0,R_straight)
        left.Drive(0,L_straight)

        while(x[angle, 0] > 900):
            x = data(lidar.getPoints(ser_lidar, polar = True))
            angle = angle_calc(x,270)
            while(x[angle,1] > 275):
                x = data(lidar.getPoints(ser_lidar, polar = True))
                angle = angle_calc(x,270)
            print('distance in loop',x[angle,0])
            print('angle in loop',x[angle,1])
        case = 1

    # case 1
    if case == 1:
        
        print('circling center')
        start = time.time()
        end = time.time()
        while ((start-end)<30):
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

            x = data(lidar.getPoints(ser_lidar, polar = True))
            dist2 = distance_slice(x, slice_angle, slice_width)

##            case = color(ser_color,case)
            
            while np.min(dist2) < 900:
                
                x = data(lidar.getPoints(ser_lidar, polar = True))
                dist2 = distance_slice(x, slice_angle, slice_width)
                
##                case = color(ser_color, case)
                print('I see the center')
    
            while np.min(dist2) > 900:
                
                right.Drive(0,0)
                left.Drive(1,L_straight)
                x = data(lidar.getPoints(ser_lidar, polar = True))
                dist2 = distance_slice(x, slice_angle, slice_width)
                
##                case = color(ser_color, case)
                print('turning towards center')
            
            end = time.time()

    if case == 2:
        slice_width = 10

        x = data(lidar.getPoints(ser_lidar, polar = True))
        dist3 = distance_slice(x, 10, slice_width)

        i = 1
        while (dist3[i] > dist3[0])
            right.Drive(1,R_straight)
            left.Drive(0,L_straight)

            x = data(lidar.getPoints(ser_lidar, polar = True))
            dist3 = distance_slice(x, 10, slice_width)

        stop()

        x = data(lidar.getPoints(ser_lidar, polar = True))

        while(x[0,0] > 200)
            right.Drive(0,R_straight)
            left.Drive(0,L_straight)

        stop()    
    
except KeyboardInterrupt:
    print("Exiting")

    stop()
    left.Stop()
    right.Stop()
