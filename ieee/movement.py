import numpy as np
import pigpio
import Lidar_Trial
import Lidar_Motion
import matplotlib.pyplot as plt

falure = 0

lidar = Lidar_Trial.Lidar()

motor = Lidar_Motion.LDRPWM(17)
motor1 = Lidar_Motion.LDRPWM(2)
motor2 = Lidar_Motion.LDRPWM(3)
motor.Spin(255)
motor1.Spin(0)
motor2.Spin(0)
reads = 150
vals = np.array([])
diff_list = np.array([])
try:
    while True:
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
            while falure < 5:
                #print(lidar.Scan())
                x = lidar.Scan(reads)
                if x == -1:
                    falure += 1
                    print("failed")
                else:
                    falure = 0
                    
                    x = np.asarray(x)#data is read in one full matrix of values at a time
##                    plt.scatter(x[:,1],x[:,0],s=2)
##                    plt.ylim(0,1000)
##                    plt.show()
                    for i in range(0, x.shape[0]-1):
                        diff = int(np.abs(x[i+1,0] - x[i,0]))
                        diff_list = np.append(diff_list,diff) #append differences to array

                    direction = x[np.where(diff_list == np.max(diff_list)),1] #declare angle to move towards
                    distance = x[np.where(diff_list == np.max(diff_list)),0] #distance to attain
                    
                    if np.any(x[0:30,0]) < distance:
                        print('hellloooo')
                        motor1.Spin(10)
                        motor2.Spin(10)
                    
                    diff_list = 0 #reset difference array to zero to prepare for new matrix of lidar readings

                    
                    
                print(" ")
        else:
            print("Failed to initialize")
except KeyboardInterrupt:
    print("Exiting")
    motor.Spin(0)
    motor1.Spin(0)
    motor2.Spin(0)
