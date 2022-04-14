import RPi.GPIO as GPIO
import time

fan = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(fan, GPIO.OUT)

for i in range(2):
    GPIO.output(fan, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(fan, GPIO.LOW)
    time.sleep(5)

GPIO.cleanup()