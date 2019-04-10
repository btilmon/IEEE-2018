
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
    right.Drive(210,0)
    left.Drive(211,1)

def reverse():
    right.Drive(230,1)
    left.Drive(230,0)    
    
def rightZP():
    right.Drive(130,0)
    left.Drive(130,0)
    
def leftZP():
    right.Drive(150,1)
    left.Drive(150,1)    
    
#~ def colorFile():
    
    #~ color = np.loadtxt('file.out')
    
    #~ while os.stat('file.out').st_size == 0:
        #~ color = np.loadtxt('file.out')  
              
    #~ return color

def colorMethod():
    msg = ser_color.read(3)
    #~ time.sleep()
    front = int(msg[0])
    side = int(msg[2])
    
    final = np.array([front, side])
    return final

def colorCorner(colorData):
    if colorData[0] == colorData[1]:
        return 1
    else:
        return 0

def dangerZone(case):
    '''
    reverses if something gets too close to robot
    '''

    x = read()
    danger_zone = distance_slice(x, 180, 179)
    danger_dist = 140 # should be 200 but ya know
    
    if np.min(danger_zone) < danger_dist:
        reverse()
        sleep(2)
        return 1
    else:
        return case




    
'''
cases:
    case 0 = move out of corner and position orthogonally to center
    case 1 = orbit around center
    case 2 = move to corner, then enter case 0, enter case 3 if all objects collected
    case 3 = move to original corner and raise flag
'''

try:
    start = time.time()
    orbitTime = 150
    end = 0
    orbit_group = 0
    case = 0
    timer_count = 1
    time_check_constant = 45
    while True:
        end = time.time()
        print(end-start)
        if case == 0:
            print('case = ', case)

            x = read()
            
            angle = 180
            width = 5
            
            dist = distance_slice(x, angle, width)
            begin_dist = np.array([1050, 800, 700])
            straight()
            
            while np.min(dist) < begin_dist[orbit_group]:  
                x = read()
                dist = distance_slice(x, angle, width)
                
                #~ control_dist = np.concatenate([distance_slice(x,350,9), distance_slice(x,10,9)])
                #~ mid_idx = int(len(control_dist)/2)
                left_angle = 300
                right_angle = 60
                #~ print(contro)
                
                
                #dynamically move to center
                #~ while control_dist[mid_idx] < control_dist[-1] and np.min(dist) < 1000:
                    #~ x = read()
                    #~ dist = distance_slice(x, angle, width)
                    #~ control_dist = np.concatenate([distance_slice(x,left_angle,359-left_angle), distance_slice(x,right_angle,right_angle - 1)])
                    #~ print('turning left')
                    #~ right.Drive(200,0)
                    #~ left.Drive(230,1)         
                #~ while control_dist[mid_idx] < control_dist[0] and np.min(dist) < 1000:
                    #~ dist = distance_slice(x, angle, width)                    
                    #~ x = read()
                    #~ control_dist = np.concatenate([distance_slice(x,left_angle,359-left_angle), distance_slice(x,right_angle,right_angle - 1)])                    
                    #~ print('turning right')
                    #~ right.Drive(230,0)
                    #~ left.Drive(200,1) 

########################################################
#######  THIS CODE WORKED WELL ##########################
            rightZP()

            x = read()
            angle = 250
            dist = distance_slice(x, angle, 15)
            
            while(np.min(dist) < 800):
                x = read()
                dist = distance_slice(x, angle, 5)
                
            while(np.min(dist) > 800):
                x = read()
                dist = distance_slice(x, angle, 5)
            
            stop()
            sleep(2)
            col = colorMethod()
            while col[1] == 4:
                col = colorMethod()
            start_col = col[1]
            print('start_col',start_col)
            right.Drive(210,0)
            left.Drive(215,1)

            case = 1
############################################################

        #case 1
        if case == 1:
            print('case = ', case)
            print('orbit ring # = ', orbit_group)
            
            slice_width = np.array([15, 20, 20])
            slice_angle = np.array([305, 300, 300])
            
            lDrive = np.array([220, 205, 190]) 

            dist2 = distance_slice(x, slice_angle[orbit_group], slice_width[orbit_group])
            
            left_thres = np.array([300, 355, 425])
            right_thres = np.array([305, 360, 430])
            
            left_angle = 270
            right_angle = 60            
            
            left_dist = distance_slice(x, left_angle, 359 - left_angle)
            right_dist = distance_slice(x, right_angle, 15)
            
            #~ case = dangerZone(case)
                
            if (end - start) > orbitTime:
                color = colorMethod()
                if color[1] == start_col:
                    case = 2
                    print('Going to corner - time running out')
            else:        
                req = colorCorner(colorMethod())
                if req == 1:
                    case = 2
                    print('Going to corner - colors matched')
            if (end - start)/time_check_constant > timer_count:
                timer_count = timer_count + 1
                case = 2
                print('Going to corner - timer check')
        
            #~ #begin orbiting
            while np.min(dist2) < 900:## and (color[0] != color[1]): #900 worked well
                straight()
                x = read()
                dist2 = distance_slice(x, slice_angle[orbit_group], slice_width[orbit_group])
                left_dist = distance_slice(x, left_angle, 359 - left_angle)
                right_dist = distance_slice(x, right_angle, 15)                
                #~ case = dangerZone(case)
                
                if (end - start) > orbitTime:
                    color = colorMethod()
                    if color[1] == start_col:
                        case = 2
                        print('Going to corner - time running out')
                else:        
                    req = colorCorner(colorMethod())
                    if req == 1:
                        case = 2
                        print('Going to corner - colors matched')
                if (end - start)/time_check_constant > timer_count:
                    timer_count = timer_count + 1
                    case = 2
                    print('Going to corner - timer check')
                        
                while (np.min(left_dist) < left_thres[orbit_group]) and (np.min(left_dist) < right_thres[orbit_group]) and (np.min(dist2) < 900): 
                    x = read()
                    left_dist = distance_slice(x, left_angle, 359 - left_angle)
                    right_dist = distance_slice(x, right_angle, 40)

                    dist2 = distance_slice(x, slice_angle[orbit_group], slice_width[orbit_group])
                    right.Drive(190, 0)
                    left.Drive(180, 1)                    
                    #~ case = dangerZone(case) 
                    
                x = read()
                dist2 = distance_slice(x, slice_angle[orbit_group], slice_width[orbit_group])
                
                if (end - start) > orbitTime:
                    color = colorMethod()
                    if color[1] == start_col:
                        case = 2
                        print('Going to corner - time running out')
                else:        
                    req = colorCorner(colorMethod())
                    if req == 1:
                        case = 2
                        print('Going to corner - colors matched')
                if (end - start)/time_check_constant > timer_count:
                    timer_count = timer_count + 1
                    case = 2
                    print('Going to corner - timer check')
                    
                while (np.min(left_dist) > right_thres[orbit_group]) and (np.min(left_dist) > left_thres[orbit_group]) and (np.min(dist2) < 900):
                    x = read()
                    left_dist = distance_slice(x, left_angle, 359 - left_angle)
                    right_dist = distance_slice(x, right_angle, 40) 

                    dist2 = distance_slice(x, slice_angle[orbit_group], slice_width[orbit_group])
                    right.Drive(165, 0)
                    left.Drive(lDrive[orbit_group], 1)

            if (end - start) > orbitTime:
                color = colorMethod()
                if color[1] == start_col:
                    case = 2
                    print('Going to corner - time running out')
            else:        
                req = colorCorner(colorMethod())
                if req == 1:
                    case = 2
                    print('Going to corner - colors matched')
            if (end - start)/time_check_constant > timer_count:
                timer_count = timer_count + 1
                case = 2
                print('Going to corner - timer check')
                    
            x = read()
            dist2 = distance_slice(x, slice_angle[orbit_group], slice_width[orbit_group])
            while np.min(dist2) > 900:## and (color[0] != color[1]): #900 worked well
                x = read()
                dist2 = distance_slice(x, slice_angle[orbit_group], slice_width[orbit_group])
                right.Stop()
                left.Drive(180, 1)
        
#############################################################################################################


        #case 2
        if case == 2:
            print('case = ', case)
            
            x = read()
            
            c_angle1 = 24
            c_angle2 = 14
            c_width = 4
            
            c_dist1 = distance_slice(x,c_angle1,c_width)
            c_dist2 = distance_slice(x,c_angle2, c_width)
            
            right.Drive(180,0)
            left.Stop()
            
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
            while np.min(dist) > 300:
                x = read()
                
                angle1 = 3
                width1 = angle1 - 1
                angle2 = 360 - angle1
                
                dist = np.concatenate([distance_slice(x, angle1, width1), distance_slice(x, angle2, width1) ])
                
                dx = 0.1
                dy = np.diff(dist)/dx
                diff = x[10,0] - x[(len(x) - 10),0]
                
                while  diff < 0 and (np.min(dist) > 300):
                    #~ print('turning left')
                    right.Drive(220,0)
                    left.Drive(245,1) 
                    x = read()
                    dist = np.concatenate([distance_slice(x, angle1, width1), distance_slice(x, angle2, width1) ])
                    
                    diff = x[10,0] - x[(len(x) - 10),0]
                    
                while  diff > 0 and (np.min(dist) > 300):
                    #~ print('turning right')
                    right.Drive(245,0)
                    left.Drive(220,1) 
                    x = read()
                    dist = np.concatenate([distance_slice(x, angle1, width1), distance_slice(x, angle2, width1) ])
                    
                    diff = x[10,0] - x[(len(x) - 10),0]               
                
                
                straight()

                
            if (end - start) > orbitTime:
                case = 3
            else:
                
                reverse_dist = np.array([1000, 850, 750])
                
                #reverse out of corner
                reverse()
                while x[0,0] < reverse_dist[orbit_group] or x[0,0] == 3000 :
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

                if (orbit_group == 2):
                    orbit_group = 0
                else:
                    orbit_group = orbit_group+1
                #~ oTime = 0
                #~ oTime = time.time()
                case = 1
        if case == 3:
            print('Raise flag')
            stop()
            ldrM.Stop()
            break
    
            
except KeyboardInterrupt:
    print("Exiting")

    stop()
    ldrM.Stop()

