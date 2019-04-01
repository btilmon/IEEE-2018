
# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

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
    upper_red = np.array([200,255,255])
    rmask2 = cv2.inRange(hsv, lower_red, upper_red)    
    
    rmask1 = rmask1 + rmask2
    rmask1 = cv2.morphologyEx(rmask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    red = cv2.morphologyEx(rmask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
    
    #green thresholds
    lower_green = np.array([30,65,65])
    upper_green = np.array([80,255,255])
    gmask = cv2.inRange(hsv, lower_green, upper_green)
    gmask = cv2.morphologyEx(gmask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    green = cv2.morphologyEx(gmask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))    
    
    #yellow thresholds
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])
    ymask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    ymask = cv2.morphologyEx(ymask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    yellow = cv2.morphologyEx(ymask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))    
    
    #blue thresholds
    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])
    bmask = cv2.inRange(hsv, lower_blue, upper_blue)
    bmask = cv2.morphologyEx(bmask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    blue = cv2.morphologyEx(bmask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))    
    
    #add masks to segment r,g,b,y
    mask = green + red + yellow + blue
    final = cv2.bitwise_and(image, image, mask = mask)
    
    return final

############ THREADED APPROACH ############
# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream().start()
time.sleep(2.0)

while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	objects = segmentedImage(frame)
	
	
	
	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", objects)
		key = cv2.waitKey(1) & 0xFF
 
	# update the FPS counter
	#~ fps.update()
	
#~ # stop the timer and display FPS information
#~ fps.stop()
#~ print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
#~ print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
