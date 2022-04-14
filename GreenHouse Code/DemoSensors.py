import RPi.GPIO as GPIO
import time
import cv2

pump = 32
fan = 33
heat = 36
cam = cv2.VideoCapture(0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pump, GPIO.OUT)
GPIO.setup(fan, GPIO.OUT)
GPIO.setup(heat, GPIO.OUT)

#turn on water pump for 7 sec
for i in range(1):
    GPIO.output(pump, GPIO.LOW)
    time.sleep(3)
    GPIO.output(pump, GPIO.HIGH)
    time.sleep(5)

#0.25 oz per second

#turn on fan for 7 sec
for i in range(1):
    GPIO.output(fan, GPIO.HIGH)
    time.sleep(7)
    GPIO.output(fan, GPIO.LOW)
    time.sleep(5)

#turn on heat for 7 sec
for i in range(1):
    GPIO.output(heat, GPIO.HIGH)
    time.sleep(7)
    GPIO.output(heat, GPIO.LOW)
    time.sleep(5)

#turn on lights for 7 sec
    
#turn on camera for 7 sec
while True:
	ret, image = cam.read()
	cv2.imshow('Imagetest',image)
	cv2.waitKey(10000)
	break

cam.release()
cv2.destroyAllWindows()

GPIO.cleanup()