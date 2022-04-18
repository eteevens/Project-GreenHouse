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

pump = digitalio.DigitalInOut(board.D12)

pump.direction = digitalio.Direction.OUTPUT

while True:
    print("PUMP")
    pump.value = False
    time.sleep(5)
    pump.value = True
    time.sleep(5)
    break

#0.25 oz per second







































