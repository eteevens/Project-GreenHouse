import RPi.GPIO as GPIO
import time

pump = 32

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pump, GPIO.OUT)

for i in range(2):
    GPIO.output(pump, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(pump, GPIO.LOW)
    time.sleep(5)

GPIO.cleanup()

#0.25 oz per second







































