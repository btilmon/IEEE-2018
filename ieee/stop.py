import scan
import Motor
import pigpio
import numpy as np
from time import sleep



left = Motor.Motor(scan.m1DIR,scan.m1PWM)
right = Motor.Motor(scan.m2DIR,scan.m2PWM)
left.Inverse()


##
right.Drive(0,0)
left.Drive(0,0)

#rightzero point turn
##while True:
##        
##    right.Drive(0,255)
##    left.Drive(0,255)

#left zero point turn
##right.Drive(0,0)
##left.Drive(1,255)

