
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

def find_histogram(clt):
	"""
	create a histogram with k clusters
	:param: clt
	:return:hist
	"""
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins=numLabels)

	hist = hist.astype("float")
	hist /= hist.sum()

	return hist

while True:
	frame = objectImage()
	#~ segmented = segmentedImage(frame)
	segmented = segmentedImage(frame)

	h = segmented[:,:,0]
	s = segmented[:,:,1]
	v = segmented[:,:,2]
	print(h.shape)
	
	h = h[np.where(v > 40)]
	s = s[np.where(v > 0)]
	v = v[np.where(v > 0)]
	

	print(h.shape) 
	
	
	#~ print(segmented.shape)
	#~ seg = segmented[:,:,0][segmented[:,:,2] > 0]
	#~ seg = np.delete(segmented, segmented[:,:,2] < 80, axis = 2)
	#~ seg = segmented[:,:,:][np.where(
	#~ print(seg.shape)
	
	r = 0
	g = 0
	b = 0
	y = 0
	
	#~ col = np.array([0,0,0,0])
	
	r = ((h < 10) | (h > 350) & (h < 360)).sum() 
	g = ((80 < h) & (h < 120)).sum()
	b = ((h > 215) & (h < 245)).sum()
	y = ((50 < h) & (h < 60)).sum()
	
	
	#~ r = np.count_nonzero(h < 10)
	#~ g = np.count_nonzero(all(80 < h < 100))
	#~ b = np.count_nonzero(all(210 < h < 230))
	#~ y = np.count_nonzero(all(55 < h < 75))
	
	col = np.array([r,g,b,y])
	print(np.argmax(col))
	print(col)
	
	
	#~ for i in range(0, len(segmented)):
		#~ for j in range(0, len(segmented[0])):
			#~ h = segmented[i, j, 0]
			
			#~ if h < 10:
				#~ col[0] = col[0] + 1
			#~ if 80 < h < 100:
				#~ col[1] = col[1] + 1
			#~ if 210 < h < 230:
				#~ col[2] = col[2] + 1
			#~ if 55 < h < 75:
				#~ col[3] = col[3] + 1
	#~ print(r)
		
	#~ print(h.size)
	
	#~ img = cv2.cvtColor(segmented, cv2.COLOR_BGR2RGB)
	#~ pil_img = Image.fromarray(img)
	
	#~ h = pil_img.histogram()
	
	#~ r = h[0:256]
	#~ g = h[256:256*2]
	#~ b = h[256*2: 256*3]
	
	
	
	#~ print(Image.getcolors(pil_img))
	#~ img = img.reshape((img.shape[0] * img.shape[1],3))
	#~ clt = KMeans(n_clusters=4) #cluster number
	#~ clt.fit(img)        
	#~ img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#~ count, bins = np.histogram(segmented, bins = 20)
	#~ print(count)
	cv2.imshow("Frame", segmented)
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


