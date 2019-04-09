
# import the necessary packages
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
from time import sleep
import cv2
import numpy as np
from sklearn.cluster import KMeans
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=1,
    help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
 
# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)




#~ def objectColor():
# loop over the frames from the video stream
def objectImage():
    
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = frame[140:180,10:350,:] #width x height since camera inverted
        #~ frame = imutils.resize(frame, width=400)


        #~ cv2.imshow("2", frame)
        #~ k = cv2.waitKey(5) & 0xFF
        #~ if k == 27:
            #~ break
            
        #~ sleep(5)
        return frame

    cv2.destroyAllWindows()
    vs.stop()

#~ while True:
    #~ objectImage()
