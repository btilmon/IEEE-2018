
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
ser_lidar = serial.Serial(port, 115200, timeout = 5)
'''ser_color = serial.Serial("/dev/ttyACM0",9600)'''
#### Arduino ports #####

ser_lidar.setDTR(False)
print (ser_lidar.name)
lidar = Lidar(ser_lidar)

'''sensors = ser_color.readline().rstrip()'''
'''data = sensors.split('^')'''

#Motor A
m1in1= 26
m1in2= 19
m1PWM = 13
#Motor A
m2in1 = 21
m2in2 = 20
m2PWM = 16

left = Motor.Motor(m1in1,m1in2,m1PWM)
right = Motor.Motor(m2in1,m2in2,m2PWM)
left.Inverse()

########### motor speeds#######
# straight
L_straight = 230
R_straight = 230

# quadrant count
quadrant = 1




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

def read():
    x = data(lidar.getPoints(ser_lidar, polar = True))
    while (x.size < 100):
        x = data(lidar.getPoints(ser_lidar, polar = True))
    return x

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
            
            #~ angle = 350
            #~ width = 4
            
            #~ right.Drive(0,0)
            #~ left.Drive(1,160)
            #~ x = read()
            #~ dist = distance_slice(x, angle, width)  
            
            # turn to center
            x = read()
            
            angle = 180
            width = 5
            
            dist = distance_slice(x, angle, width)
            
            right.Drive(0,245)
            left.Drive(1,245)
            while np.min(dist) < 700:  
            #~ dist1 = distance_slice(x, angle1, width1)
            #~ dist2 = distance_slice(x, angle2, width1) 


            #~ while (np.min(dist2) > 1000 and np.min(dist2) < 2000) == False:

                
                x = read()
                dist = distance_slice(x, angle, width)
                #~ dist2 = distance_slice(x, angle2, width1)
                
            #~ while ((x[0,0] > 1000 and x[0,0] <2000) == False):
                
                
    #~ ##            print('case is', color(ser_color, case))
                print('turning to center')
                #~ print(x[0,0])
                #~ if x[0,0] > 700 and x[0,0] < 2000:
                    #~ break
                #~ else:
                    #~ x = read()

            #~ x = read()
            
            #~ angle1 = 25
            #~ width1 = angle1 - 1
            #~ angle2 = 360 - angle1
            
            #~ dist1 = distance_slice(x, angle1, width1)
            #~ dist2 = distance_slice(x, angle2, width1) 
            
            #~ right.Drive(0,R_straight)
            #~ left.Drive(1,L_straight)
            
            #~ while((np.min(dist1) < 700) and (np.min(dist2) < 700)):

                #~ x = read()
                #~ dist1 = distance_slice(x, angle1, width1)
                #~ dist2 = distance_slice(x, angle2, width1) 

                #~ print(x[0,0])
            
            #~ while((np.min(dist1) > 700) and (np.min(dist2) > 700)):

                #~ x = read()
                #~ dist1 = distance_slice(x, angle1, width1)
                #~ dist2 = distance_slice(x, angle2, width1) 

                #~ print(x[0,0])


            
            right.Drive(0,170)
            left.Drive(0,170)

            x = read()
            angle = 295
            dist = distance_slice(x, 295, 5)
            
            while(np.min(dist) < 800):
                x = read()
                dist = distance_slice(x, 295, 5)
                
            while(np.min(dist) > 800):
                x = read()
                dist = distance_slice(x, 295, 5)

                #~ print('positioning to center')
            #~ print('positioned!')    
            case = 1

        #case 1
        if case == 1:
            print('case = ', case)
            #~ print('circling center')
            start = time.time()
            end = time.time()
            
            x = read()
            slice_angle = 180
            slice_width = 10
            dist = distance_slice(x, slice_angle, slice_width)
            
            print('quadrant is',quadrant)
            #~ if (x[0,0] > 1100 and x[0,0] < 1200) and (any(dist == x[0,0] + 50) or any(dist == x[0,)) == True):
            #~ if (x[0,0] > 1100 and x[0,0] < 1200) and (((any(dist > x[0,0] - 50) == True) and (any(dist < x[0,0] + 50) == True))):
            minm = x[0,0] - 100
            maxm = x[0,0] + 100
            if (x[0,0] > 1000 and x[0,0] < 1200):
                print('congrtas, it works! 0 degree=',x[0,0],'180 degree=',dist)
                quadrant = quadrant + 1
                
                if quadrant%3 == 0:
                    case = 2
            
            #~ while ((end-start) < 10):
            
            slice_width = 3
            slice_angle = 290
            turn_modify = 0
            orbit_corr = 0
            R_turn = 0
            L_turn = 0
            
            right.Drive(0,R_straight)
            left.Drive(1,L_straight + orbit_corr)

            x = read()
            dist2 = distance_slice(x, slice_angle, slice_width)
            
            #begin orbiting
            while np.min(dist2) < 1000: #900 worked well
                                    
                x = read()
                dist2 = distance_slice(x, slice_angle, slice_width)
                
                #~ print('I see the center')
                #~ end = time.time()
    
            while np.min(dist2) > 1000: #900 worked well
                                    
                right.Drive(0,0)
                left.Drive(1,L_straight)
                x = read()
                dist2 = distance_slice(x, slice_angle, slice_width)

                    #~ print('turning towards center')
                    #~ end = time.time()

                #~ end = time.time()


        #case 2
        if case == 2:
            print('case = ', case)
            
            x = read()
            
            c_angle1 = 32
            c_angle2 = 22
            c_width = 4
            
            c_dist1 = distance_slice(x,c_angle1,c_width)
            #~ deriv = np.asarray([dist1[i+1] - dist1[i] for i in range(len(dist1) - 1)])
            c_dist2 = distance_slice(x,c_angle2, c_width)
            
            right.Drive(0,170)
            left.Drive(0,170)
            
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

            right.Drive(0,245)
            left.Drive(1,245)
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
                

            
            right.Drive(1,245)
            left.Drive(0,245)
            
            #reverse out of corner
            while x[0,0] < 600 or x[0,0] == 3000 :
                x = read()
            
            #account for reading walls before entering case 1 again
            right.Drive(1,150)
            left.Drive(1,150)
            
            x = read()
            
            
            while x[0,0] < 2000:
                x = read()
            
            
            right.Drive(0,245)
            left.Drive(1,245)
            
            while x[0,0] > 1700:
                x = read()
            
            
                  
            case = 1
            

            
            
            
           
            
           
    
except KeyboardInterrupt:
    print("Exiting")

    stop()
    left.Stop()
    right.Stop()
