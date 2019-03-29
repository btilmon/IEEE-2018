
import Motor
import pigpio
from time import sleep

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


left = Motor.Motor(m1PWM,m1in1,m1in2)
right = Motor.Motor(m2PWM,m2in1,m2in2)
left.Inverse()

def rightZP():
    right.Drive(170,0)
    left.Drive(170,0)
    
def leftZP():
    right.Drive(170,1)
    left.Drive(170,1)    
    
def stop():
    right.Stop()
    left.Stop()
    
stop()
ldrM.Stop()
