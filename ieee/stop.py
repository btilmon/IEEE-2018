
import Motor
import pigpio
from time import sleep

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



#~ while True:
    #~ print("forward")
    #~ right.Drive(0,255)
    #~ left.Drive(0,255)
    #~ sleep(3)

    #~ print("Reverse")
    #~ right.Drive(1,255)
    #~ left.Drive(1,255)
    #~ sleep(3)
    
    #~ right.Drive(0,255)
    #~ left.Drive(1,255)
    #~ sleep(3)
    
    #~ right.Drive(1,255)
    #~ left.Drive(0,255)
    #~ sleep(3)
    
right.Drive(0,0)
left.Drive(1,0)

#rightzero point turn
##while True:
##        
##    right.Drive(0,255)
##    left.Drive(0,255)

#left zero point turn
##right.Drive(0,0)
##left.Drive(1,255)

