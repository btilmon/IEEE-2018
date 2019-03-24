#~ from picamera.array import PiRGBArray
#~ from picamera import PiCamera
#~ import time

#~ camera = PiCamera()
#~ rawCapture = PiRGBArray(camera)

#~ time.sleep(0.1)

#~ camera.capture(rawCapture, format = "bgr")
#~ image = rawCapture.array

#~ print(image.shape)

import picamera 
import os
from PIL import Image
from time import sleep
import numpy as np

camera = picamera.PiCamera()
camera.start_preview()
camera.capture('/home/pi/Desktop/image.jpg')
camera.stop_preview()

#~ img = np.asarray(Image.open('/home/pi/Desktop/image.jpg').convert('L'))
img = Image.open('/home/pi/Desktop/image.jpg').convert('L')
img.show()
#~ print(len(img))
#~ img = np.asarray([img])
#~ img.save('/home/pi/Desktop/grey.jpg')



os.remove("/home/pi/Desktop/image.jpg")
