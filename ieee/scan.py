import numpy as np
import pigpio
import Lidar_Trial
import Lidar_Motion
import Motor
from time import sleep
#import matplotlib.pyplot as plt

falure = 0
sleep(0)
lidar = Lidar_Trial.Lidar()

motor = Lidar_Motion.LDRPWM(17)
#~ #Motor A
#~ m1DIR = 6
#~ m1PWM = 13
#~ #Motor A
#~ m2DIR = 19
#~ m2PWM = 26

#~ left = Motor.Motor(m1DIR,m1PWM)
#~ right = Motor.Motor(m2DIR,m2PWM)

#~ left.Inverse()
#~ motor.Spin(255)

reads = 150
vals = np.array([])
diff_list = np.array([])
print('help') 

try:
    if falure == 5:
        print("re-initializing")
        lidar = ""
        sleep(2)
        lidar= Lidar_Trial.Lidar()
        falure = 0
        reads = reads - 10
        print(reads)

    if lidar.initialize() == 1:
        print("initialized")

        #print(lidar.Scan())
        x = lidar.Scan(reads)
        if x == -1:
            falure += 1
            print("failed")
        else:
            falure = 0
            
        x = np.asarray(x)#data is read in one full matrix of values at a time
##            print(x)
            
##                    plt.scatter(x[:,1],x[:,0],s=2)
##                    plt.ylim(0,1000)
##                    plt.show()


                

            

            
        #~ diff_list = 0 #reset difference array to zero to prepare for new matrix of lidar readings
        #~ motor.Spin(0)
        #~ right.Drive(0,0)
        #~ left.Drive(0,0)
##            left.Stop()
##            right.Stop()
                
                
        print(" ")
    else:
        print("Failed to initialize")       
except KeyboardInterrupt:
    print("Exiting")
    motor.Spin(0)
    #~ right.Drive(0,0)
    #~ left.Drive(0,0)
    #~ left.Stop()
    #~ right.Stop()


