
		
	
	

import Motor
import pigpio
import numpy as np
import time
import os

import serial
import math
from time import sleep
import threading

ser = serial.Serial('/dev/ttyACM0',57600)

left = Motor.Motor(scan.m1DIR,scan.m1PWM)
right = Motor.Motor(scan.m2DIR,scan.m2PWM)
left.Inverse()

########### motor speeds#######
# straight
L_straight = 230
R_straight = 230

############ methods #########
def read():
	ser = serial.Serial('/dev/ttyACM0',57600)
	data = ser.readline().rstrip()

	sensors = data.split('^')
	sensors = map(int, sensors)
	
print(sensors)

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

def zeroSlice(x,slice_width):
    '''
    gives a range of values on the zero degree, distanceSLice doesnt work on zero degree 
    '''
    slice_angle = 358
    dist1 = distance_slice(x, slice_angle, slice_width)
    
    slice_angle = 2
    dist2 = distance_slice(x, slice_angle, slice_width)
    
    dist = np.append(dist1, dist2)
    return dist

    
    
    
'''
cases:
    case 0 = move out of corner and position orthogonally to center
    case 1 = orbit around center
    case 2 = move to corner, then enter case 0, enter case 3 if all objects collected
    case 3 = move to original corner and raise flag
'''

try:
    
    case = 0
    while True:
    ##    case = color(data)
        
        
        #case 0
        if case == 0:
            print('case = ', case)
            
            angle = 358
            width = 1
            right.Drive(0,0)
            left.Drive(1,160)
            x = read()
            #~ dist = zeroSlice(x, 2)
            dist = distance_slice(x,angle, width)
            
            while ((np.min(dist) > 1000 and np.min(dist) <2000) == False):
                
                
    ##            print('case is', color(ser_color, case))
                print('turning to center')
                if np.min(dist) > 1000 and np.min(dist) < 2000:
                    break
                else:
                    x = read()
                    dist = distance_slice(x,angle, width)
                    print(dist)
                    
            print('turned to center')
            stop()

            sleep(.5)

            x = read()
            dist = zeroSlice(x, 1)
            while(np.average(dist) > 800):
                right.Drive(0,R_straight)
                left.Drive(1,L_straight)
                x = read()
                dist = zeroSlice(x, 1)

                print(x[0,0])
