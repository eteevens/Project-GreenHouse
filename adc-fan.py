#set up ADC
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO

from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)


#fan setup

fan = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan, GPIO.OUT)


##########################################################
#   Control Fan with adc temp                            #
##########################################################

# print("{:>5}\t{:>5}\t{:>5}".format("raw", "v", "t"))

#fanOnTemp- high C
fanOnTemp = 25

#fanOffTemp- low C
#fanOffTemp = 26

while True:
    tempData = chan.voltage
    #Actual temp: C
    tempConv = ((20/2.934)*tempData) + (25.692/2.934)
    
    #debug
    print("{:>5}\t{:>5.3f}\t{:>5.3f}".format(chan.value, chan.voltage, tempConv))
    #print(tempConv, fanOnTemp)
    #GPIO.output(fan, GPIO.LOW)
    
    if (tempConv > fanOnTemp):
        #fan on
        print("temp above 25! turn fan on.")
        GPIO.output(fan, True)
        time.sleep(10)
        
    if (tempConv <= fanOnTemp):
        #fan off
        print("temp below 25! turn fan off.")
        GPIO.output(fan, False)
        time.sleep(5)
        