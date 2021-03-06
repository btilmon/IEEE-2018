
# import the necessary packages
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
import numpy as np
import camera_object
from camera_object import objectImage
import camera_tape
from camera_tape import tapeImage
import serial 
from serial import Serial
from time import sleep

ser = serial.Serial("/dev/serial0", baudrate = 115200, timeout=.09)


	
def segmentedImage(image):
	
	'''
	- Returns segmented image with a red, blue, green, and yellow mask.
	'''
	#converting from bgr to hsv color scale
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	
	#red thresholds
	#range for lower red
	lower_red = np.array([0,120,70])
	upper_red = np.array([10,255,255])
	rmask1 = cv2.inRange(hsv, lower_red, upper_red)
	#range for upper red
	lower_red = np.array([170,120,70])
	upper_red = np.array([180,255,255])
	rmask2 = cv2.inRange(hsv, lower_red, upper_red)    
	
	red = rmask1 + rmask2
	#~ rmask1 = cv2.morphologyEx(rmask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
	#~ red = cv2.morphologyEx(rmask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
	
	#green thresholds
	lower_green = np.array([30,65,65])
	upper_green = np.array([80,255,255])
	green = cv2.inRange(hsv, lower_green, upper_green)
	#~ gmask = cv2.morphologyEx(gmask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
	#~ green = cv2.morphologyEx(gmask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))    
	
	#yellow thresholds
	lower_yellow = np.array([20,20,20])
	upper_yellow = np.array([30,255,255])
	yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
	#~ ymask = cv2.morphologyEx(ymask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
	#~ yellow = cv2.morphologyEx(ymask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))    
	
	#blue thresholds
	lower_blue = np.array([90,50,50])
	upper_blue = np.array([110,255,255])
	blue = cv2.inRange(hsv, lower_blue, upper_blue)
	#~ bmask = cv2.morphologyEx(bmask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
	#~ blue = cv2.morphologyEx(bmask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))    
	
	#add masks to segment r,g,b,y
	mask = green + red + yellow + blue
	final = cv2.bitwise_and(image, image, mask = mask)
	return final

def color():
	arr1 = np.zeros((4,))
	arr2 = np.zeros((4,))
	arr3 = 0
	i = 0

	while True:
		
		frame = objectImage()
		segmented = segmentedImage(frame)
		seg = segmented

		b = segmented[:,:,0]
		g = segmented[:,:,1]
		r = segmented[:,:,2]
		
		b = b[np.where(b > 170)]
		g = g[np.where(g > 170)]
		r = r[np.where(r > 170)]
		
		
		
		yLower = np.uint8([0,100,100])
		yUpper = np.uint8([100,255,255])
		yellow = cv2.inRange(segmented, yLower, yUpper)
		y = cv2.countNonZero(yellow)
		
		blackLower = np.uint8([0,0,0])
		blackUpper = np.uint8([0,0,0])
		black = cv2.inRange(segmented, blackLower, blackUpper)
		black1 = cv2.countNonZero(black)
		
		#~ print('black pix',black,'total pix',len(segmented) * len(segmented[0]))		
		
	
		#~ print('b', b.size, 'g', g.size, 'r', r.size, 'y', y)
		#~ cv2.imshow("Frame", seg)	
		
		frame = tapeImage()
		segmented = segmentedImage(frame)
		seg = segmented

		b1 = segmented[:,:,0]
		g1 = segmented[:,:,1]
		r1 = segmented[:,:,2]
		
		b1 = b1[np.where(b1 > 170)]
		g1 = g1[np.where(g1 > 170)]
		r1 = r1[np.where(r1 > 170)]
		
		yLower = np.uint8([0,100,100])
		yUpper = np.uint8([100,255,255])
		yellow = cv2.inRange(segmented, yLower, yUpper)
		y1 = cv2.countNonZero(yellow)

		blackLower = np.uint8([0,0,0])
		blackUpper = np.uint8([0,0,0])
		black = cv2.inRange(segmented, blackLower, blackUpper)
		black = cv2.countNonZero(black)
	
		#~ print('b', b1.size, 'g', g1.size, 'r', r1.size, 'y', y1)
		
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break

		#~ cv2.imshow("2", seg)
		

		arr1 = np.array([r.size, g.size, b.size, y])
		arr2 = np.array([r1.size, g1.size, b1.size, y1])

		max1 = np.argmax(arr1)
		max2 = np.argmax(arr2)
		
		thres_black = .98
		
		#~ print(np.average(b1),np.average(g1),np.average(r1))
		if black > (thres_black * len(segmented) * len(segmented[0])):
			max2 = 4
		if black1 > (thres_black * len(seg) * len(seg[0])):
			max1 = 5			
		final = str(max1) + "," + str(max2)			
		maxarr = np.array([max1, max2])			
			
		print(final)
			
		ser.write(final.encode())
		time.sleep(1)
		#~ print("writing")

while True:

	color()

