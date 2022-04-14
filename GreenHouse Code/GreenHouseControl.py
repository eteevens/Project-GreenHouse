# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO
import adafruit_si7021

from adafruit_ads1x15.analog_in import AnalogIn
#code for the Fan/relay
fan = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(fan, GPIO.OUT)

"""-------------------------------
INITIALIZE SENSORS AND OUTPUTS
-------------------------------"""

# HUMIDITY SENSOR- Create library object using our Bus I2C port
#humidSen = adafruit_si7021.SI7021(board.I2C())

#ADC TEMPERATURE SENSOR- Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}\t{:>5}".format("raw", "v", "t"))

"""-------------------------------
    USER DEFINED VARIABLES
-------------------------------"""
tempHigh = 28 #temp to turn fan on
#humidHigh = 26 #humidity to turn fan on
tempLow = 26 #temp to turn heating pad on

while True:
    
    '''************* GATHER AND SHOW SENSOR DATA ***************************'''
    #gathering adc temperature data
    tempData = chan.voltage
    #convert voltage to celcius 
    tempConv = ((20/2.934)*tempData) + (25.692/2.934)

    print("Temperature = {:>5.2f}°C".format(tempConv))
    print("Humidity = {:>5.2f}%".format(humidSen.temperature))
    #GPIO.output(fan, GPIO.HIGH) #high turns fan off
    #time.sleep(1)
    '''************* CONTROLS BASED ON SENSOR AND USER DATA ****************'''
    
    if (tempConv >= tempHigh):
        print("Temperature higher than {:>1.0f}°C. Turning fan on.".format(tempHigh))
        GPIO.output(fan, GPIO.LOW)
        time.sleep(10)
#         GPIO.output(fan, GPIO.HIGH)
#         time.sleep(5)
    else:
        print("Temperature and humidity lower than {:>1.0f}°C and {:>1.0f}%. Fan off".format(tempHigh, humidHigh))
        GPIO.output(fan, GPIO.HIGH)
        time.sleep(1)
        
#    if (humidSen.temperature >= humidHigh):
#        print("Humidity higher than {:>1.0f}%. Turning fan on.".format(humidHigh))
#        GPIO.output(fan, GPIO.LOW)
#        time.sleep(10)
        
    if(tempConv <= tempLow):
        print("Temperature lower than {:>1.0f}°C. Turning fan on.".format(tempLow))
        
    
GPIO.cleanup()
