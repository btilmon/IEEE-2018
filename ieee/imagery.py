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
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    #range for upper red
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)    
    
    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(image, image, mask = mask1)
    

    
    #~ # show the frame
    cv2.imshow("Frame", res1)
    key = cv2.waitKey(1) & 0xFF
    
    
    #~ # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
