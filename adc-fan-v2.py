# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO

from adafruit_ads1x15.analog_in import AnalogIn
#code for the Fan/relay
fan = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(fan, GPIO.OUT)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}\t{:>5}".format("raw", "v", "t"))

while True:
    tempData = chan.voltage
    tempConv = ((20/2.934)*tempData) + (25.692/2.934)

    print("{:>5}\t{:>5.3f}\t{:>5.3f}".format(chan.value, chan.voltage, tempConv))
    #GPIO.output(fan, GPIO.HIGH) #high turns fan off
    #time.sleep(1)
    
    if (tempConv >= 24):
        print("Temp too high. Turning fan on.")
        GPIO.output(fan, GPIO.LOW)
        time.sleep(10)
#         GPIO.output(fan, GPIO.HIGH)
#         time.sleep(5)
    else:
        print("Temp already low.")
        GPIO.output(fan, GPIO.HIGH)
        time.sleep(1)
    
GPIO.cleanup()
