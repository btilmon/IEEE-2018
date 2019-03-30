#~ from picamera.array import PiRGBArray
#~ from picamera import PiCamera
#~ import time

#~ camera = PiCamera()
#~ rawCapture = PiRGBArray(camera)

#~ time.sleep(0.1)

#~ camera.capture(rawCapture, format = "bgr")
#~ image = rawCapture.array

#~ print(image.shape)

#~ import picamera 
#~ import os
#~ from PIL import Image
#~ from time import sleep
#~ import numpy as np

#~ camera = picamera.PiCamera()
#~ camera.start_preview()
#~ camera.capture('/home/pi/Desktop/image.jpg')
#~ sleep(30)
#~ camera.stop_preview()

#~ img = np.asarray(Image.open('/home/pi/Desktop/image.jpg').convert('L'))
#~ img = Image.open('/home/pi/Desktop/image.jpg').convert('L')
#~ img.show()
#~ print(len(img))
#~ img = np.asarray([img])
#~ img.save('/home/pi/Desktop/grey.jpg')



#~ os.remove("/home/pi/Desktop/image.jpg")



# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

#~ boundaries = [
	#~ ([17, 15, 100], [80, 80, 200]),
	#~ ([86, 31, 4], [220, 88, 50]),
	#~ ([25, 146, 190], [62, 174, 250]),
	#~ ([103, 86, 65], [145, 133, 128])
#~ ]

#~ # capture frames from the camera
#~ for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #~ # grab the raw NumPy array representing the image, then initialize the timestamp
    #~ # and occupied/unoccupied text
    #~ image = frame.array
    #~ for (lower, upper) in boundaries:
		
		#~ lower = np.array(lower, dtype = "uint8")
		#~ upper = np.array(upper, dtype = "uint8")
		
		#~ mask = cv2.inRange(image, lower, upper)
		#~ output = cv2.bitwise_and(image, image, mask = mask)
		
		#~ cv2.imshow("images", np.hstack([image, output]))
		#~ cv2.waitKey(0)
		
    # show the frame
    #~ cv2.imshow("Frame", image)
    #~ key = cv2.waitKey(1) & 0xFF
    
    
    # clear the stream in preparation for the next frame
    #~ rawCapture.truncate(0)

    #~ # if the `q` key was pressed, break from the loop
    #~ if key == ord("q"):
        #~ break

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    
    #converting from bgr to hsv color scale
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
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
        
        
    
    mask = green + red + yellow + blue
    final = cv2.bitwise_and(image, image, mask = mask)
    

    
    #~ # show the frame
    cv2.imshow("Frame", final)
    key = cv2.waitKey(1) & 0xFF
    
    
    #~ # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
