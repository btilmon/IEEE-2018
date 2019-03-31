
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import sys
#~ import skvideo.io

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

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, image1 = cap.read()


   
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image2 = frame.array
        rawCapture.truncate(0)
        break
        
    objects = segmentedImage(image1)
    tape = segmentedImage(image2)

    horizontal = np.hstack((objects,tape))

    cv2.imshow('frame',horizontal)
    #~ cv2.imshow('frame',tape)    
    
    #~ rawCapture.truncate(0)
    #~ cap.release()
    
    # if the `q` key was pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
        
#main pipeline
#~ for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    #~ #capture pi camera image
    #~ image1 = frame.array 
    #~ #capture usb camera image

    #~ cv2.imshow('frame',image2)
    #~ cv2.imshow('frame',image1)    
    
    #~ rawCapture.truncate(0)
    #~ cap.release()
    
    #~ # if the `q` key was pressed, break from the loop
    #~ key = cv2.waitKey(1) & 0xFF
    #~ if key == ord("q"):
        #~ break



    #return segmented images
    #~ objects = segmentedImage(image1) 
    #~ tape = segmentedImage(image2) 
    
    #~ print(objects)
    #Delete pi cam and usb cam images for memory

