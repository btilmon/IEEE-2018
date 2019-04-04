
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
import socket
#~ import cv_pipeline
import os
import subprocess
from subprocess import Popen, PIPE
#~ from optparse import OptionParser
import shlex
import ctypes


ser_color = serial.Serial("/dev/serial0",115200)




#############Motion#######################
#Motor A
m1in1= 26
m1in2= 19
m1PWM = 13
#Motor A
m2in1 = 21
m2in2 = 20
m2PWM = 16
#Lidar
ldr = 17

ldrM = Motor.Motor(ldr)
ldrM.Drive(255)

left = Motor.Motor(m1PWM,m1in1,m1in2)
right = Motor.Motor(m2PWM,m2in1,m2in2)
left.Inverse()

########### motor speeds#######
# straight
L_straight = 230
R_straight = 230

# quadrant count
i = 0

#~ dist_group1 = 
##################Lidar#################################

port = "/dev/ttyUSB0"
ser_lidar = serial.Serial(port, 115200, timeout = 5)


ser_lidar.setDTR(False)
print (ser_lidar.name)
lidar = Lidar(ser_lidar)

'''sensors = ser_color.readline().rstrip()'''
'''data = sensors.split('^')'''

pipe_in, pipe_out = os.pipe()

###############################

############ methods #########
def data(lidar_data):
    '''
    filters any emtpy values from lidar to equal 3000
    '''
    x = lidar_data
    x[np.where(x[:,0] == 0),0] = 3000
    return x

    
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
    
    dist = np.asarray(dist)
    
    return dist
    


def stop():
    right.Stop()
    left.Stop()

def read():
    x = data(lidar.getPoints(ser_lidar, polar = True))
    while (x.size < 100):
        x = data(lidar.getPoints(ser_lidar, polar = True))
    return x




def straight():
    right.Drive(230,0)
    left.Drive(230,1)

def reverse():
    right.Drive(230,1)
    left.Drive(230,0)    
    
def rightZP():
    right.Drive(150,0)
    left.Drive(150,0)
    
def leftZP():
    right.Drive(150,1)
    left.Drive(150,1)    
    
#~ def colorFile():
    
    #~ color = np.loadtxt('file.out')
    
    #~ while os.stat('file.out').st_size == 0:
        #~ color = np.loadtxt('file.out')  
              
    #~ return color

def color():
    msg = ser_color.read(3)
    #~ time.sleep()
    front = int(msg[0])
    back = int(msg[2])
    
    final = np.array([front, back])
    return final

def colorCorner(colorData):
    if colorData[0] == colorData[1]:
        return 1
    else:
        return 0





    
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
        
        if case == 0:
            #~ print('case = ', case)

            x = read()
            
            angle = 180
            width = 5
            
            dist = distance_slice(x, angle, width)
            
            straight()
            
            while np.min(dist) < 800:  
                x = read()
                dist = distance_slice(x, angle, width)

########################################################
#######  THIS CODE WORKED WELL ##########################
            rightZP()

            x = read()
            angle = 295
            dist = distance_slice(x, angle, 5)
            
            while(np.min(dist) < 800):
                x = read()
                dist = distance_slice(x, angle, 5)
                
            while(np.min(dist) > 800):
                x = read()
                dist = distance_slice(x, angle, 5)

            case = 1
############################################################

        #case 1
        if case == 1:
            #~ print('case = ', case)
            
            slice_width = 10
            slice_angle = 290
            


            x = read()
            dist2 = distance_slice(x, slice_angle, slice_width)
            dist3 = distance_slice(x, 90,5)
            
            
            col = color()
            req = colorCorner(col)
            if req == 1:
                case = 2
        
            #~ #begin orbiting
            while np.min(dist2) < 900:## and (color[0] != color[1]): #900 worked well
                
                straight()
                x = read()
                dist2 = distance_slice(x, slice_angle, slice_width)
                dist3 = distance_slice(x, 90,5)
                
                #~ if any(dist3) < 840:
                    #~ print('crossed tape')
                    #~ col = color()
                    #~ req = colorCorner(col)
                    #~ if req == 1:
                        #~ case = 2

            col = color()
            req = colorCorner(col)
            if req == 1:
                case = 2
            
            while np.min(dist2) > 900:## and (color[0] != color[1]): #900 worked well
                                    
                right.Stop()
                left.Drive(180, 1)
                x = read()
                dist2 = distance_slice(x, slice_angle, slice_width)
                
                if x[0,0] < 900:
                    case = 'turnCorrect'

            col = color()
            req = colorCorner(col)
            if req == 1:
                case = 2
            
        if case == 'turnCorrect':

            x = read()
            angle = 295
            dist = distance_slice(x, angle, 5)

            rightZP()

            while(np.min(dist) < 900):
                x = read()
                dist = distance_slice(x, angle, 5)
                
            while(np.min(dist) > 900):
                x = read()
                dist = distance_slice(x, angle, 5)
                
            case = 1
        
#############################################################################################################


        #case 2
        if case == 2:
            #~ print('case = ', case)
            
            x = read()
            
            c_angle1 = 24
            c_angle2 = 14
            c_width = 4
            
            c_dist1 = distance_slice(x,c_angle1,c_width)
            #~ deriv = np.asarray([dist1[i+1] - dist1[i] for i in range(len(dist1) - 1)])
            c_dist2 = distance_slice(x,c_angle2, c_width)
            
            right.Drive(180,0)
            left.Stop()
            
            #detect corner
            while any(c_dist2 > c_dist1) == True:
                #~ print('detecting corner')
                x = read()
                c_dist1 = distance_slice(x,c_angle1,c_width)
                c_dist2 = distance_slice(x,c_angle2, c_width)
                
            while any(c_dist2 < c_dist1) == True:
                #~ print('detecting corner')
                x = read()
                c_dist1 = distance_slice(x,c_angle1, c_width)
                c_dist2 = distance_slice(x, c_angle2, c_width)
                
            #move towards corner
            x = read()
            
            angle1 = 10
            width1 = angle1 - 1
            angle2 = 360 - angle1
            
            dist1 = distance_slice(x, angle1, width1)
            dist2 = distance_slice(x, angle2, width1) 
            dist = np.concatenate(dist1,dist2)
            print('dist is',dist)

            straight()
            
            #~ while((np.min(dist1) > 300) and (np.min(dist2) > 300)):
            while np.min(dist) > 300:

                #~ print('moving towards corner')
                x = read()
                dist1 = distance_slice(x, angle1, width1)
                dist2 = distance_slice(x, angle2, width1) 
                dist = np.concatenate(dist1,dist2)
                
            reverse()
            
            #reverse out of corner
            while x[0,0] < 900 or x[0,0] == 3000 :
                x = read()
                
            leftZP()

            x = read()
            angle = 295
            dist = distance_slice(x, angle, 5)
            
            while(np.min(dist) < 900):
                x = read()
                dist = distance_slice(x, angle, 5)
                
            while(np.min(dist) > 900):
                x = read()
                dist = distance_slice(x, angle, 5)

            
                #~ print('reversing out of corner')
        
            #~ x = read()
            #~ dist = np.concatenate(distance_slice(
            #~ leftZP()
            
            #~ while np.min(dist) < 1800 and any(dist != 3000):
            #~ while x[0,0] < 1600:                
                #~ print('returning to orbit')
                #~ x = read()
                
            #~ straight()
            #~ sleep(2)
            
            print('left corner',i,'times')
            i = i + 1
            case = 1
            
except KeyboardInterrupt:
    print("Exiting")

    stop()
    ldrM.Stop()

