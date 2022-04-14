import cv2
import time

cam = cv2.VideoCapture(0)

while True:
	ret, image = cam.read()
	cv2.imshow('Imagetest',image)
	cv2.waitKey(5000)
	break
#	k = cv2.waitKey(1)
#	if k != -1:
#		break
cv2.imwrite('/home/pi/Pictures/testimage.jpg', image)

cam.release()
cv2.destroyAllWindows()







