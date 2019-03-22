import Motor
import pigpio
import numpy as np
import time
import os

import serial
import math
from time import sleep
import threading


#Motor A
m1DIR = 6
m1PWM = 13
#Motor A
m2DIR = 19
m2PWM = 26

left = Motor.Motor(m1DIR,m1PWM)
right = Motor.Motor(m2DIR,m2PWM)
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
	
	if '' in sensors:
	    data = ser.readline().rstrip()
	    sensors = data.split('^')
	elif '0' in sensors:
	    data = ser.readline().rstrip()
	    sensors = data.split('^')
	elif len(sensors) != 3:
	    data = ser.readline().rstrip()
	    sensors = data.split('^')
	#~ print('the other sensor',sensors)
	
	sensors = np.asarray(map(int, sensors))
	return sensors

	
try:
    case = 0
    while True:
	x = read()
        if case == 0:
            print('case = ', case)
            
            right.Drive(0,0)
            left.Drive(1,160)
            
            
            print(x)
            while ((x[1] > 1000 and x[1] <2000) == False):
                
                
    ##            print('case is', color(ser_color, case))
                print('turning to center')
		print(x)
                if x[1] > 1000 and x[1] < 2000:
                    break
                else:
                    #~ x = read()
		    
                   
		    print(x)
	    print(x)
            print('turned to center')
            

            sleep(.5)

            #~ x = read()
	    sleep(.5)
           
            while(x[0] > 800):
                right.Drive(0,R_straight)
                left.Drive(1,L_straight)
                #~ x = read()
		print('in loop',x)
		sleep(.5)
                
	    print('broke',x[0])
            break
except KeyboardInterrupt:
    print("Exiting")

    stop()
    left.Stop()
    right.Stop()
