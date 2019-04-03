
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


#~ python_bin = "/home/pi/.virtualenvs/opencv4/bin/python3.5"
#~ script_file = "/home/pi/IEEE-2018/ieee/cv_pipeline.py"


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
quadrant = 1

#~ dist_group1 = 
##################Lidar#################################

port = "/dev/ttyUSB0"
ser_lidar = serial.Serial(port, 115200, timeout = 5)
'''ser_color = serial.Serial("/dev/ttyACM0",9600)'''
#### Arduino ports #####

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
    right.Drive(245,0)
    left.Drive(245,1)

def reverse():
    right.Drive(245,1)
    left.Drive(245,0)    
    
def rightZP():
    right.Drive(150,0)
    left.Drive(150,0)
    
def leftZP():
    right.Drive(150,1)
    left.Drive(150,1)    
    
def colorFile():
    
    color = np.loadtxt('file.out')
    
    while os.stat('file.out').st_size == 0:
        color = np.loadtxt('file.out')  
              
    return color

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
        #~ while True:
            #~ urmom = np.loadtxt('file.out')
            #~ print(urmom)
        #~ command_template = '/bin/bash -c "source {}/{}/bin/activate && python3.5 -"'
        #~ command = shlex.split(command_template.format(os.environ['WORKON_HOME'], 'opencv4'))
        #~ print(command)
        #~ process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
        #~ print((ctypes.c_char).from_address(process))
        #~ print(process.communicate()[0])
       
        #~ cv_pipeline.color(pipe_out)
        #~ val = os.read(pipe_in, 56)
        #~ print(val)
        
        #case 0
        if case == 0:
            print('case = ', case)

            x = read()
            
            angle = 180
            width = 5
            
            dist = distance_slice(x, angle, width)
            
            straight()
            
            while np.min(dist) < 800:  
                x = read()
                dist = distance_slice(x, angle, width)
            
            #~ angle90 = 90
            #~ spread = 10
            
            #~ x = read()
            #~ dist90 = distance_slice(x, angle90, spread)
            
            #~ rightZP()
            
            #~ while np.min(dist90) > 700:
                #~ x = read()
                #~ dist90 = distance_slice(x, angle90, spread)
            
            



########################################################
#######  THIS CODE WORKED WELL ##########################
            right.Drive(170,0)
            left.Drive(170,0)

            x = read()
            angle = 295
            dist = distance_slice(x, 295, 5)
            
            while(np.min(dist) < 800):
                x = read()
                dist = distance_slice(x, 295, 5)
                
            while(np.min(dist) > 800):
                x = read()
                dist = distance_slice(x, 295, 5)

            case = 1
############################################################

        #case 1
        if case == 1:
            print('case = ', case)
            
            
#######################################################################################################
########      THIS CODE WORKED DECENTLY WELL ###########################
            #~ start = time.time()
            #~ end = time.time()
            
            #~ x = read()
            #~ slice_angle = 180
            #~ slice_width = 20
            #~ dist = distance_slice(x, slice_angle, slice_width)
            
            color = colorFile()
            if color[0] == color[1]:
                case = 2

            
            slice_width = 3
            slice_angle = 290
            
            straight()

            x = read()
            dist2 = distance_slice(x, slice_angle, slice_width)
            
            #begin orbiting
            while np.min(dist2) < 1000 and (color[0] != color[1]): #900 worked well
                                    
                x = read()
                dist2 = distance_slice(x, slice_angle, slice_width)
                
                color = colorFile()
                if color[0] == color[1]:
                    case = 2
            
            
            while np.min(dist2) > 1000 and (color[0] != color[1]): #900 worked well
                                    
                right.Stop()
                left.Drive(245, 1)
                x = read()
                dist2 = distance_slice(x, slice_angle, slice_width)
                
                color = colorFile()
                if color[0] == color[1]:
                    case = 2
                #~ if x[0,0] < 900:
                    #~ case = 0
#############################################################################################################


        #case 2
        if case == 2:
            print('case = ', case)
            
            x = read()
            
            c_angle1 = 23
            c_angle2 = 13
            c_width = 4
            
            c_dist1 = distance_slice(x,c_angle1,c_width)
            #~ deriv = np.asarray([dist1[i+1] - dist1[i] for i in range(len(dist1) - 1)])
            c_dist2 = distance_slice(x,c_angle2, c_width)
            
            right.Drive(150,0)
            left.Drive(150,0)
            
            #detect corner
            while any(c_dist2 > c_dist1) == True:
                x = read()
                c_dist1 = distance_slice(x,c_angle1,c_width)
                c_dist2 = distance_slice(x,c_angle2, c_width)
                
            while any(c_dist2 < c_dist1) == True:
                x = read()
                c_dist1 = distance_slice(x,c_angle1, c_width)
                c_dist2 = distance_slice(x, c_angle2, c_width)
                
            
            #move towards corner
            x = read()
            
            angle1 = 5
            width1 = angle1 - 1
            angle2 = 360 - angle1
            
            dist1 = distance_slice(x, angle1, width1)
            dist2 = distance_slice(x, angle2, width1) 

            right.Drive(245,0)
            left.Drive(245,1)
            while((np.min(dist1) > 300) and (np.min(dist2) > 300)):

                
                x = read()
                dist1 = distance_slice(x, angle1, width1)
                dist2 = distance_slice(x, angle2, width1) 
                
                #~ while any(x[0,0] < x[5,0]) == True:
                    #~ right.Drive(0,200)
                    #~ left.Drive(0,170)
                    
                    #~ x = read()
                    #~ c_dist1 = distance_slice(x, c_angle1, c_width)
                    #~ c_dist2 = distance_slice(x, c_angle2, c_width)
                

            
            reverse()
            
            #reverse out of corner
            while x[0,0] < 500 or x[0,0] == 3000 :
                x = read()

        
            x = read()
            angle0 = 30
            width = 10
            dist0 = distance_slice(x, angle0, width)
            
            leftZP()
            
            while np.min(dist) < 900:
                x = read()
                dist = distance_slice(x, angle, width)        
            
            #~ right.Drive(245,0)
            #~ left.Drive(245,1)
            
            #~ while x[0,0] > 1700:
                #~ x = read()
                
            
            stop()
            
            
            case = 0
            

            
            
            
           
            
           
    
except KeyboardInterrupt:
    print("Exiting")

    stop()
    ldrM.Stop()

