import cv2 #openCV for camera controls

import json #to send the data to be displayed on the graph and recieve data
#from the controls
import numpy as np #numpy for random number

from threading import Semaphore #semaphore, protects the frame data

from datetime import datetime #date module for current date, time module
#for the current time for the graph

from flask import Flask #flask main
from flask import render_template #html pages
from flask import Response #functions
from flask import stream_with_context #for live graph
from flask import request #for controls and scheduler

import time #allows the random data to wait

graphFrame = {} #the current graph frame, empty initally
graphFrameSem = Semaphore()

#the current controls frame, initalized to standard settings to prevent errors
controlsFrame = {'current_temp_high': 15,
                 'current_temp_low': 10,
                 'current_water_drip_en': False,
                 'current_water_drip_duration': 0,
                 'current_lights': False}
controlsFrameSem = Semaphore()

#the scheduler controls frame, initalized to standard settings to prevent errors
schedulerFrame = {'schd_water_drip_en': False,
                  'schd_water_drip_time': '12:00 am',
                  'schd_water_drip_duration': 0,
                  'schd_water_drip_repeat': 1,
                  'schd_water_drip_inf': False,
                  'schd_light_en': False,
                  'schd_light_start': '12:00 am',
                  'schd_light_stop': '12:15 am'}
schedulerFrameSem = Semaphore()

newDataFlag = False #is there a new data? If true, set the flag
newDataFlagSem = Semaphore()

app = Flask(__name__) #initalize the web application

def camera_frames():
    #the camera feed for the page

    vc = cv2.VideoCapture(0) #temporary taking of video feed from computer camera

    while True:
        success, frame = vc.read() #read the camera frame
        (frame_height, frame_width) = frame.shape[:2] #save the current frame size

        resize_percent = 0.50 #rescale the frame by 50%

        #create scaled frame size
        rescale_frame_width = int(frame_width * resize_percent)
        rescale_frame_height = int(frame_height * resize_percent)

        #save dimensions for resize scaling`
        dimensions = (rescale_frame_width, rescale_frame_height)

        #rescale the frame with cv2's interpolation
        frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_LINEAR)

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            outputFrame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + outputFrame + b'\r\n')

    vc.release()

def graph_display(): #read in graph data to display

    while True:

        newDataFlagSem.acquire()
        global newDataFlag
        if (newDataFlag == True):
            graphFrameSem.acquire()
            graph_data = graphFrame #get the current frame from the graph
            newDataFlag = False #the data was acquired for the graph
            graphFrameSem.release()

            yield f"data:{graph_data}\n\n" #stream data
        newDataFlagSem.release()


def send_controls_data(): #send the controls data
    controlsFrameSem.acquire()
    controls_data = controlsFrame.copy() #get the current frame of the controls data
    controlsFrameSem.release()

    return json.dumps(controls_data)

def convert24(input): #convert time to a 24 hour format, note that this assumes
#the input is of form HH:MM pm/am

    if (input[-2:] == 'am' or input[-2:] == 'AM') and input[:2] == "12":
        #it's between midnight and 1 am so 00:MM needs to be returned
        return "00" + input[2:-3]

    elif (input[-2:] == 'am' or input[-2] == 'AM'):
        #it's in the morning, no need to change anything
        return input[:-3]

    elif (input[-2:] == 'pm' or input[-2] == "PM") and input[:2] == "12":
        #it's between noon and 1 pm, no need to change anything
        return input[:-3]

    elif (input[-2:] == 'pm' or input[-2] == "PM"):
        #it's afternoon and 1 pm or later, need to add 12 hours
        return str(int(input[:2]) + 12) + input[2:-3]

    else:
        #if it doesn't include am/pm, it's not the right format 
        print('error, incorrect format')
        return input


def send_schd_data(): #send the scheduler data
    schedulerFrameSem.acquire()
    schd_data = schedulerFrame.copy() #get the current frame of the schd data
    schedulerFrameSem.release()

    if schd_data['schd_water_drip_time'] != '':
        schd_data['schd_water_drip_time'] = convert24(str(schd_data['schd_water_drip_time']))

    if schd_data['schd_light_start'] != '':
        schd_data['schd_light_start'] = convert24(str(schd_data['schd_light_start']))

    if schd_data['schd_light_stop'] != '':
        schd_data['schd_light_stop'] = convert24(str(schd_data['schd_light_stop']))

    return json.dumps(schd_data)

@app.route('/') #index of the GUI (the viewable page)
def index():
    return render_template('index.html')

@app.route('/video_feed') #video feed route
def video_feed_route():
    return Response(camera_frames(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/graph_feed') #graph feed route
def graph_feed_route():
    response = Response(stream_with_context(graph_display()),
    mimetype='text/event-stream')
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@app.route('/calendar_feed', methods=["POST"]) #calendar feed route
def calendar_feed_route():
    retrieve_cal = request.get_json() #get the user's input from the GUI

    schedulerFrameSem.acquire()
    global schedulerFrame
    schedulerFrame = retrieve_cal
    schedulerFrameSem.release()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/controls_feed', methods=["POST"]) #controls feed route
def controls_feed_route():
    retrieve_output = request.get_json() #get the user's input from the GUI

    controlsFrameSem.acquire()
    global controlsFrame
    controlsFrame = retrieve_output
    controlsFrameSem.release()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/read_client', methods=["POST"]) #read data generated by the client
def read_client_route():
    client_data = request.get_json() #get the data from the data client
    #(the Raspberry Pi code)

    newDataFlagSem.acquire()
    graphFrameSem.acquire()
    global graphFrame, newDataFlag
    graphFrame = client_data #write the new data
    newDataFlag = True #there is new data
    graphFrameSem.release()
    newDataFlagSem.release()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/write_client_controls') #write controls to the client
def write_client_controls_route():
    return Response(send_controls_data(), mimetype='application/json')

@app.route('/write_client_schd') #write scheduler data to the client
def write_client_schd_route():
    return Response(send_schd_data(), mimetype='application/json')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port='5000', debug=True, threaded=True, use_reloader=False)
