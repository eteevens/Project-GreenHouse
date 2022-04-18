import board 
#import RPi.GPIO as GPIO
import time
import neopixel
import cv2
import digitalio
import busio
import adafruit_ads1x15.ads1115 as ADS
import adafruit_si7021
from adafruit_veml6070 import VEML6070
from adafruit_ads1x15.analog_in import AnalogIn

fan = digitalio.DigitalInOut(board.D13)
fan.direction = digitalio.Direction.OUTPUT

#turn on fan for 7 sec
while True:
    print("FAN")
    fan.value = True
    time.sleep(5)
    fan.value = False
    time.sleep(3)
    break

GPIO.cleanup()