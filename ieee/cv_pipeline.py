from camera_object import objectImage
import cv2

while True:
	im = objectImage()
	cv2.imshow("frame",im)
	key = cv2.waitKey(1) & 0xFF
	


