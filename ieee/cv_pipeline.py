
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
from sklearn.cluster import KMeans
from PIL import Image

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
	lower_yellow = np.array([20,100,100])
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


while True:
	frame = objectImage()
	segmented = segmentedImage(frame)
	seg = segmented

	b = segmented[:,:,0]
	g = segmented[:,:,1]
	r = segmented[:,:,2]
	
	b = b[np.where(b > 120)]
	g = g[np.where(g > 120)]
	r = r[np.where(r > 120)]
	
	yLower = np.uint8([0,70,100])
	yUpper = np.uint8([100,255,255])
	yellow = cv2.inRange(segmented, yLower, yUpper)
	y = cv2.countNonZero(yellow)
	
	print('b', b.size, 'g', g.size, 'r', r.size, 'y', y)
	
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

	cv2.imshow("Frame", seg)
	key = cv2.waitKey(1) & 0xFF

	#~ # if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
#~ while True:
	

	#~ segmented = segmentedImage(frame)

	#~ img = cv2.cvtColor(segmented, cv2.COLOR_HSV2BGR)

	#~ img = img.reshape((img.shape[0] * img.shape[1],3))

	#~ clt = KMeans(n_clusters=4) #cluster number
	#~ clt.fit(img)        

	#~ hist = find_histogram(clt)
	#~ print(hist)


