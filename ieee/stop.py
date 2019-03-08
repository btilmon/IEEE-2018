import scan
import Motor
import pigpio
import numpy as np




left = Motor.Motor(scan.m1DIR,scan.m1PWM)
right = Motor.Motor(scan.m2DIR,scan.m2PWM)
left.Inverse()



right.Drive(0,0)
left.Drive(0,0)

##right.Drive(0,255)
##left.Drive(1,255)


