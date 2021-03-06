
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
    
    #~ dist = np.asarray(dist,dtype=np.uint8)
    
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


while True:
    angle1 = 10
    width1 = angle1 - 1
    angle2 = 360 - angle1
    
    x = read()
    dist1 = distance_slice(x, angle1, width1)
    dist2 = distance_slice(x, angle2, width1)
    
    print(dist1)
    print(dist2)
    
    dist = np.concatenate([dist1,dist2])
