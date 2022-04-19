import RPi.GPIO as GPIO
import time

heat = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(heat, GPIO.OUT)

for i in range(10):
    GPIO.output(heat, GPIO.LOW)
    time.sleep(3)
    GPIO.output(heat, GPIO.HIGH)
    time.sleep(3)

GPIO.cleanup()