import board
import json
import requests
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
from datetime import timedelta

from threading import Semaphore #semaphore, protects the frame data

from flask import Flask #flask main
from flask import render_template #html pages
from flask import Response #functions
from flask import stream_with_context #for live graph
from flask import request #for controls and scheduler

ti2c = board.I2C()
uv = VEML6070(ti2c)

# HUMIDITY SENSOR- Create library object using our Bus I2C port
humidSen = adafruit_si7021.SI7021(ti2c)

print("***********************************************")
print("********* Senior Design Winter 2022 ***********")
print("*********     Group GreenHouse      ***********")
print('*********      ',datetime.now().date(),'         ***********')
print("*********  GreenHouse Control Code  ***********")
print("***********************************************")

#define GPIO pins
pump = digitalio.DigitalInOut(board.D12)
fan = digitalio.DigitalInOut(board.D13)
heat = digitalio.DigitalInOut(board.D16)
lights = neopixel.NeoPixel(board.D18,6,brightness=1)
#cam = cv2.VideoCapture(0)

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

def gather_light_data(): #returns uv light level- 0 to 100
    uv_raw = uv.uv_raw
    print('UV Light Level:',uv_raw)
    return uv_raw

def gather_humid_data(): #returns humidity level- 1 to 100 %
    humidity = humidSen.relative_humidity
    print("Humidity = {:>5.2f} %".format(humidSen.relative_humidity))
    return humidity

#timing
def get_current_time():
    current_time = datetime.now().time().isoformat('minutes') #HHMM
    print('Current time called is ', current_time)
    return current_time

def get_current_date():
    current_day = datetime.now().date()
    print('Current date is ', current_day)
    return current_day

#control pump
def run_pump(duration):
    print('Running pump for ', duration, 'seconds')
    pump.value = False
    time.sleep(duration)
    pump.value = True
    time.sleep(61-duration)

#control fan
def run_fan():
    print("Fan is on")
    fan.value = True

def stop_fan():
    print("Fan is off")
    fan.value = False
    time.sleep(3)

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

def increment_day(dayToRun,repeat):
    nextDay = dayToRun + timedelta(days=repeat)
    print('Next water date is ', nextDay)
    return nextDay

'''initalize controls- EVERYTHING OFF'''
pump.value = True
fan.value = False
heat.value = False
#lights.fill((0,0,0))
time.sleep(3)

url = "http://172.20.10.7:5000" #address of the server

write_to_app = url + "/read_client" #server page for read
read_controls_from_app = url + "/write_client_controls"
#server page for writing controls
read_schd_from_app = url + "/write_client_schd"
#server page for writing scheduler

currentDate = get_current_date()
dateToRun = currentDate

'''************* GATHER DATA, RUN CONTROLS ***************************'''
while True:

    #read in data packet

    #reads from the controls
    controls_data = requests.get(read_controls_from_app, timeout=10)
    web_controls_input = controls_data.json()

    print("web_controls_input: " + web_controls_input)

    #reads from the scheduler
    schd_data = requests.get(read_schd_from_app, timeout=10)
    web_schd_input = schd_data.json()

    print("web_schd_input " + web_schd_input)

    #Regular Inputs to process
    currTempLow = web_controls_input['current_temp_low'] #int
    currTempHigh = web_controls_input['current_temp_high'] #int
    currDripEn = web_controls_input['current_water_drip_en'] #bool
    currDripDur = web_controls_input['current_water_drip_duration'] #int
    currLight = web_controls_input['current_lights'] #bool
    currHumidHigh = web_controls_input['current_humid_high'] #int
    currHeat = web_controls_input['current_heat_pad']
    currFan = web_controls_input['current_fan']

    #Scheduled Inputs to process
    scWaterDripEn = web_schd_input['schd_water_drip_en'] #bool
    scWaterDripTime = web_schd_input['schd_water_drip_time'] #time in 24h
    scWaterDripDur = web_schd_input['schd_water_drip_duration']
    scWaterDripRepeat = web_schd_input['schd_water_drip_repeat'] #int
    scLightEn = web_schd_input['schd_light_en'] #bool
    scLightStart = web_schd_input['schd_light_start'] #time in 24h
    scLightStop = web_schd_input['schd_light_stop'] #time in 24h


    #read values from pi
    print("----------------------------------------")
    currentTemp = gather_temp_data()
    currentLight = gather_light_data()
    currentHumid = gather_humid_data()
    currentTime = get_current_time()
    currentDate = get_current_date()
    print("----------------------------------------")

    #send to other program
    data_to_send = {'time':currentTime, 'Temperature (in C)':f'{currentTemp:.2f}',
                    'Humidity':f'{currentHumid:.2f}', 'Light Level':f'{currentLight:.2f}'}

    json_data = json.dumps(data_to_send)

    requests.post(write_to_app, json=json_data, timeout=10) #post data to the write address


    #basic controls- not in scheduler

    #fan controls
    print(currFan)

    #print(float(currentTemp) >= float(currTempHigh))

    if (float(currentTemp) >= float(currTempHigh)):
        print('Condition to turn fan on met- temp')
        run_fan()

    if (float(currentHumid) >= float(currHumidHigh)):
        print('Condition to turn fan on met- humid')
        run_fan()

    if (bool(currFan) == True):
        print('Condition to turn fan on met- user')
        run_fan()


    if (float(currentTemp) <= float(currTempLow):
        print('Condition to turn fan off met- temp')
        stop_fan()

    if (bool(currFan) == False)):
        print('Condition to turn fan off met- user')
        stop_fan()

    #Heat controls

    if ((float(currentTemp) <= float(currTempLow)):
        print('Condition to turn heat on met- temp')
        run_heat()

    if  (bool(currHeat) == True)):
        print('Condition to turn heat on met- user')
        run_heat()

    if (float(currentTemp) > float(currTempLow)):
        print('Condition to turn heat off met- temp')
        stop_heat()

    if  (bool(currHeat) == False)):
        print('Condition to turn heat off met- user')
        stop_heat()

    #Water drip controls
    if (bool(currDripEn) == True):
        print('Condition to turn drip on met')
        run_pump_duration(currDripDur)

    #Light controls
    if (bool(currLight) == True):
        print('Condition to turn light on met')
        #run_lights()

    if (bool(currLight) == False):
        print('Condition to turn light off met')
        #stop_lights()

    #time scheduler

    #water pump
    if(scWaterDripEn == True):
        print('Condition to enable water drip met')
        if((currentDate == dateToRun) and (currentTime == scWaterDripTime)):
            print('time to water')
            run_pump(scWaterDripDur)
            dateToRun = increment_day(currentDate,scWaterDripRepeat)

    #lights
    if(scLightEn == True):
        print('Condition to enable lights met')
        if(currentTime == scLightStart):
            print('time to turn on light')
            #run_lights()
        if(currentTime == scLightStop):
            print('time to turn off light')
            #stop_lights()

    time.sleep(1)
