import serial
import math
from time import sleep
import threading
import numpy as np
import pigpio

Start_Scan = "\xA5\x20" #Begins scanning
Force_Scan = "\xA5\x21" #Overrides anything preventing a scan
Health = "\xA5\x52" #Returns the state of the Lidar
Stop_Scan = "\xA5\x25" #Stops the scan
RESET = "\xA5\x40" #Resets the device
port = "/dev/ttyUSB0"

class Lidar():
    
    def __init__(self):
        self.ser = serial.Serial(port, 115200, timeout = 5)
        self.ser.setDTR(False)

    def initialize(self):
        global ser
        while True:
            line = ""
            falure  =  0
            init = True
            self.ser.write(RESET)
            sleep(2)
            self.ser.write(Start_Scan)
            while (falure < 250):
                falure += 1
                character = self.ser.read()
                line += character
                if (line[0:2] == "\xa5\x5a"):
                    if(len(line) == 7):
                        return 1
                elif (line[0:2] != "\xa5\x5a" and len(line) == 2):
                    line = ""
            if falure == 250:
                return -1
                    
    def Scan(self,reads):
        run = 0 
        while (run<1):
            run += 1
#            print("init")
            line = ""
            x=[]
            lock = False
            block = 0
            falure = 0
            while not lock:
#               print("Locked")
                line = ""
                lock = True
                while (falure < 2):
                    line = ""
                    while (len(line)<5):
                        character = self.ser.read()
                        line += character
                    point = self.point_Polar(line)

                    if (point[1]==0):
                        pointL = point
                        block += 1
                    if (block>1 and point[1]>pointL[1]):
                        x.append(point)
                        pointL = point
                    elif(block>2 and len(x)<reads):
                        print("retrying x: " + str(len(x)))
                        x=[]
                        block = 0
                        falure += 1
                    elif(block>2 and len(x)>reads):
                        print("Good Read x: " + str(len(x)))
                        return x
                    
                
        if (run==1):
            return -1
                    
    def leftshiftbits(self,line):
        line = int(line, 16)
        line = bin(line)
        line = line[:2] + "0" + line[2:-1]
        line = int(line, 2) #convert to integer
        return line

    def point_Polar(self,serial_frame,radians=False):
        #Get Distance
        distance = serial_frame[4].encode("hex") + serial_frame[3].encode("hex")
        distance = int(distance, 16)
        distance = distance / 4 #instructions from data sheet
        #Get Angle
        angle = serial_frame[2].encode("hex") + serial_frame[1].encode("hex")
        angle = self.leftshiftbits(angle) #remove check bit, convert to integer
        angle = angle/64 #instruction from data sheet

        if radians == True:
            theta = (angle * np.pi) / 180 #uncomment to use radians
        
            return(distance,theta) #uncomment to return radians

        else:
            return(distance, angle)

            
