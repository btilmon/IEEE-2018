
		
	
	

import Motor
import pigpio
import numpy as np
import time
import os

import serial
import math
from time import sleep
import threading
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/ttyACM0',9600)


	
def objectColor():
    '''
    Returns matrix of user defined amount of filtered color sensor data for the object colors, deletes tape color from data.
    Takes ~4 seconds to return matrix of 100 reads.
    '''
    reps = 51
    num_reads = 5 * reps #number of times to read 
    
    ser = serial.Serial('/dev/ttyACM0',9600)
    data = ser.readline().rstrip()
    
    sensors = data.split('^')
    sensors = np.asarray(sensors)
    
    while (len(sensors) != 6) or (any(sensors == '') == True):
        ser = serial.Serial('/dev/ttyACM0', 9600)
        data = ser.readline().rstrip()
        
        sensors = data.split('^')
        sensors = np.asarray(sensors)
    filt = np.array([sensors])
    filt = filt[:,0:5] # delete tape color
    filt = filt.astype(int)
   
    while len(filt[0]) <= num_reads:
        ser = serial.Serial('/dev/ttyACM0',9600)
        data = ser.readline().rstrip()
        
        sensors = data.split('^')
        sensors = np.asarray(sensors)
        
        while (len(sensors) != 6) or (any(sensors == '') == True):
            ser = serial.Serial('/dev/ttyACM0', 9600)
            data = ser.readline().rstrip()
            
            sensors = data.split('^')
            sensors = np.asarray(sensors)
        dum = np.array([sensors])
        dum = dum.astype(int)
        dum = dum[:,0:5]# delete tape color
        
        filt = np.append(filt, dum, axis = 1)
        dum = 0
    
    intensity, bins = np.histogram(filt, bins = [1, 108, 215, 322, 429, 536])
    intensity = np.asarray(intensity)
    #~ print(hist)
    #~ print(np.average(filt))

    
    
    return intensity
    

def tapeColor():
    '''
    Returns filtered single value of tape color, only returns tape color.
    To run repeatedly, must put in while loop.
    
    '''
    num_reads = 50 #number of times to read 
    
    ser = serial.Serial('/dev/ttyACM0',9600)
    data = ser.readline().rstrip()
    
    sensors = data.split('^')
    sensors = np.asarray(sensors)
    
    while (len(sensors) != 6) or (any(sensors == '') == True):
        ser = serial.Serial('/dev/ttyACM0', 9600)
        data = ser.readline().rstrip()
        
        sensors = data.split('^')
        sensors = np.asarray(sensors)
    filt = np.array([sensors])
    filt = filt.astype(int)
   
    filt = filt[:,-1] # only use last column of data 
    
    return filt

#~ i = 0
#~ x = np.array([objectColor()])
#~ print(x.shape)
#~ while i < 40:
    #~ print(i)
    #~ y = np.array([objectColor()])
    #~ x = np.append(x, y, axis = 0)
    #~ i = i + 1

#~ row = x.mean(1)
#~ col = x.mean(0)
#~ print('column mean is', col)
#~ print('row mean is',row)
#~ print(x)
    
while True:
    x = np.array(objectColor())
    print(x[0])
    print(x[1])
    print(x[2])
    print(x[3])
    if (x[1] > 90 or x[0] > 90):
        print('yellow majority')
        
    elif ((x[0] < 35) and (x[1] < 35 and x[1] > 5)) and ((x[2] > 20) and (x[3] > 5)):
        print('red majority')
    else:
        print('something else')
    

