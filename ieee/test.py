import Motor
import pigpio
import numpy as np
from time import sleep

#Motor A
m1DIR = 6
m1PWM = 13
#Motor B
m2DIR = 19
m2PWM = 26


right = Motor.Motor(m1DIR,m1PWM)
left = Motor.Motor(m2DIR,m2PWM)

#right.Inverse()

right.Drive(0,255)
left.Drive(0,255)
sleep(2)

right.Drive(1,255)
left.Drive(1,255)
sleep(5)

right.Drive(1,255)
left.Drive(0,255)
sleep(2)
right.Drive(0,255)
left.Drive(1,255)
sleep(2)

right.Stop()
left.Stop()

##try:
##    while True:
##        sleep(1)
##except KeyboardInterrupt:
##    right.Stop()
##    left.Stop()

