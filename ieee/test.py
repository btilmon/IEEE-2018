import serial
import math
from time import sleep
import threading
import numpy as np
import pigpio
import Lidar_Trial
import Lidar_Motion

falure = 0

lidar= Lidar_Trial.Lidar()
motor = Lidar_Motion.LDRPWM(17)
motor.Spin(255)
reads = 150
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
                    x = np.asarray(x)
                    print(x.shape)
                print(" ")
        else:
            print("Failed to initialize")
except KeyboardInterrupt:
    print("Exiting")
    motor.Spin(0)
