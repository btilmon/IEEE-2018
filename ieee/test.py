import numpy as np
import pigpio
import Lidar_Trial
import Lidar_Motion
import Motor
from time import sleep
#import matplotlib.pyplot as plt

falure = 0

lidar = Lidar_Trial.Lidar()

motor = Lidar_Motion.LDRPWM(17)
#Motor A
m1DIR = 6
m1PWM = 13
#Motor A
m2DIR = 19
m2PWM = 26

left = Motor.Motor(m1DIR,m1PWM)
right = Motor.Motor(m2DIR,m2PWM)

left.Inverse()
right.Drive(0,0)
left.Drive(0,0)

