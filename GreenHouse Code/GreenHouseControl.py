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
import datetime
from datetime import datetime

ti2c = board.I2C()
uv = VEML6070(ti2c)

# HUMIDITY SENSOR- Create library object using our Bus I2C port
humidSen = adafruit_si7021.SI7021(ti2c)

print("CONTROLS CODE")

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


# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

'''************* CONTROLS FUNCTIONS ***************************'''

#gathering data
def gather_temp_data(): #returns temp in Celcius 
    #gathering adc temperature data
    tempData = chan.voltage
    #convert voltage to celcius 
    tempConv = ((20/2.934)*tempData) + (25.692/2.934)
    print("Temperature = {:>5.2f}°C".format(tempConv))
    return tempConv

def gather_light_data(): #returns uv light level- 1 to 10
    uv_raw = uv.uv_raw
    print('UV Light Level: ',uv_raw)
    return uv_raw
    
def gather_humid_data(): #returns humidity level- 1 to 100%
    humidity = humidSen.relative_humidity
    print("Humidity = {:>5.2f}%".format(sensor.relative_humidity))
    return humidity

#control pump
def run_pump(duration):
    print('Running pump for ', duration, 'seconds')
    pump.value = False
    time.sleep(duration)
    pump.value = True
    time.sleep(3)

#control fan
def run_fan():
    print("Fan is on")
    fan.value = True
    
def stop_fan():
    print("Fan is off")
    fan.value = False

def run_fan_duration(duration):
    print('Running fan for ', duration, 'seconds')
    fan.value = True
    time.sleep(duration)
    fan.value = False
    time.sleep(3)

#control heating pad
def run_heat():
    print("Heat is on")
    heat.value = True
    
def stop_heat():
    print("Heat is off")
    heat.value = False

def run_heat_duration(duration):
    print('Running heat for ', duration, 'seconds')
    heat.value = True
    time.sleep(duration)
    heat.value = False
    time.sleep(3)

#control lights
def run_lights():
    print("Lights are on")
    lights.fill((255,255,255))
    
def stop_lights():
    print("Lights are off")
    lights.fill((0,0,0))

def run_lights_duration(duration):
    print('Running lights for ', duration, 'seconds')
    lights.fill((255,255,255))
    time.sleep(duration)
    lights.fill((0,0,0))
    time.sleep(3)
   
#timing
def get_current_time():
    current_time = datetime.now().time().isoformat('minutes') #HHMM
    print('Current time called is ', current_time)
    return current_time

'''************* GATHER DATA, RUN CONTROLS ***************************'''
while True:
    
    #read in data packet

    #Regular Inputs to process
    currTempLow = current_temp_low #int
    currTempHigh = current_temp_high #int
    currDripEn = current_water_drip_en #bool
    currDripDur current_water_drip_duration #int
    currLight = current_lights #bool
    currHumidHigh = current_humidity_high #int
    currFan = current_fan #bool


    #Scheduled Inputs to process
    scWaterDripEn = schd_water_drip_en #bool
    scWaterDripDur = sch_water_drip_time #time in 24h
    schd_water_drip_repeat #int
    schd_water_drip_inf #bool
    schd_light_en #bool
    schd_light_start #time in 24h
    schd_light_stop #time in 24h
    
    
    #read values from pi
    currentTemp = gather_temp_data()
    currentLight = gather_light_data()
    currentHumid = gather_humid_data()
    
    #basic controls- not in scheduler
    
    #fan controls
    if ((currentTemp >= currTempHigh) || (currentHumid >= currHumidHigh) || (currFan = True)):
        run_fan()
        
    if ((currentTemp <= curTempLow)v|| (currFan = False)):
        stop_fan()
        
    #Heat controls
    
    if (currentTemp <= currTempLow):
        run_heat()
    
    if (currentTemp > currTempLow):
        stop_heat()
        
    #Water drip controls
    if (currDripEn = True):
        run_pump(currDripDur)
        
    #Light controls
    if (currLight = True):
        run_lights()
        
    if (currLight = False):
        stop_lights()
        
        
        
