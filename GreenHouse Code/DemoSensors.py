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

ti2c = board.I2C()
uv = VEML6070(ti2c)

# HUMIDITY SENSOR- Create library object using our Bus I2C port
humidSen = adafruit_si7021.SI7021(ti2c)

print("DEMO CODE")

#define GPIO pins
pump = digitalio.DigitalInOut(board.D12)
fan = digitalio.DigitalInOut(board.D13)
heat = digitalio.DigitalInOut(board.D16)
lights = neopixel.NeoPixel(board.D18,6,brightness=1)
cam = cv2.VideoCapture(0)

#Set GPIO mode
pump.direction = digitalio.Direction.OUTPUT
fan.direction = digitalio.Direction.OUTPUT
heat.direction = digitalio.Direction.OUTPUT

#ADC TEMPERATURE SENSOR- Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# HUMIDITY SENSOR- Create library object using our Bus I2C port
# humidSen = adafruit_si7021.SI7021(board.I2C())


# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)



'''************* GATHER AND SHOW SENSOR DATA ***************************'''

for i in range(10):
    #gathering adc temperature data
    tempData = chan.voltage
    #convert voltage to celcius 
    tempConv = ((20/2.934)*tempData) + (25.692/2.934)
    
    #uv 
    uv_raw = uv.uv_raw
    risk_level = uv.get_index(uv_raw)
        
    print("Temperature = {:>5.2f}°C".format(tempConv))
    print("Humidity = {:>5.2f}%".format(sensor.relative_humidity))
    print('UV Light Level: {0}'.format(uv_raw))

#turn on water pump for 7 sec
while True:
    print("PUMP")
    pump.value = False
    time.sleep(5)
    pump.value = True
    time.sleep(5)
    break

#0.25 oz per second

#turn on fan for 7 sec
while True:
    print("FAN")
    fan.value = True
    time.sleep(7)
    fan.value = False
    time.sleep(5)
    break

#turn on heat for 7 sec
while True:
    print("HEAT")
    heat.value = True
    time.sleep(7)
    heat.value = False
    time.sleep(5)
    break

#turn on lights for 7 sec
print("LIGHTS")
lights.fill((255,255,255))
time.sleep(5)
lights.fill((0,0,0))
time.sleep(5)
    
#turn on camera for 7 sec
while True:
	ret, image = cam.read()
	cv2.imshow('Imagetest',image)
	cv2.waitKey(10000)
	break

cam.release()
cv2.destroyAllWindows()
