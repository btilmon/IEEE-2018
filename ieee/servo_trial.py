import pigpio
import Motor
from time import sleep

#Motor A
m1DIR = 6
m1PWM = 13
#Motor A
m2DIR = 19
m2PWM = 26

left = Motor.Motor(m1DIR,m1PWM)
right = Motor.Motor(m2DIR,m2PWM)

left.Inverse()

left.Drive(0,255)
right.Drive(0,255)

try:
    while True:
        print("on")
        sleep(2)
except KeyboardInterrupt:
    left.Stop()
    right.Stop()
