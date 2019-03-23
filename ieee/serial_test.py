
		
	
	

import Motor
import pigpio
import numpy as np
import time
import os

import serial
import math
from time import sleep
import threading

ser = serial.Serial('/dev/ttyACM0',9600)


	
def color():
    '''
    Returns matrix of user defined amount of filtered color sensor data.
    
    Last column in returned data is tape color.
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
   
    while len(filt) <= num_reads:
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
        filt = np.append(filt, dum, axis = 0)
        dum = 0
    
    return filt
    

x = color()

def histogram(x):
    
    
    
