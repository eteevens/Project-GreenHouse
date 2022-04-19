#import RPi.GPIO as GPIO
import time
import board
import digitalio

fan = digitalio.DigitalInOut(board.D13)
fan.direction = digitalio.Direction.OUTPUT

while True:
    fan.value = True
    time.sleep(7)
    fan.value = False
    time.sleep(5)
    break
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(fan, GPIO.OUT)

#for i in range(10):
#    GPIO.output(fan, GPIO.HIGH)
#    time.sleep(10)
#    GPIO.output(fan, GPIO.LOW)
#    time.sleep(5)

#GPIO.cleanup()