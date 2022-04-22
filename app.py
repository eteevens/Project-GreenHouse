import cv2 #openCV for camera controls

import json #to send the data to be displayed on the graph and recieve data
#from the controls
import numpy as np #numpy for random number

from threading import Semaphore #semaphore, protects the frame data

from flask import Flask #flask main
from flask import render_template #html pages
from flask import Response #functions
from flask import stream_with_context #for live graph
from flask import request #for controls and scheduler

graphFrame = {} #the current graph frame, empty initally
graphFrameSem = Semaphore()

#the current controls frame, initalized to standard settings to prevent errors
controlsFrame = {'current_temp_low': float(10),
                 'current_temp_high': float(30),
                 'current_humid_high': 90,
                 'current_water_drip_en': False,
                 'current_water_drip_duration': 0,
                 'current_lights': False,
                 'current_fan': False,
                 'current_heat_pad': False}
controlsFrameSem = Semaphore()

#the scheduler controls frame, initalized to standard settings to prevent errors
schedulerFrame = {'schd_water_drip_en': False,
                  'schd_water_drip_time': '12:00 am',
                  'schd_water_drip_duration': 0,
                  'schd_water_drip_repeat': 1,
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
#the input is of form HH:MM pm/am with a leading 0 in the hours

    if input[:2].isdigit() and input[3:5].isdigit(): #check to make sure the
    #inputted values for HH and MM are numbers
        if int(input[:2]) <= 12 and int(input[3:5]) <= 59:
            #check to make sure the HH are in 12 hour format and that the
            #minutes don't exceed possible values

            if input[-2:].lower() == 'am' and input[:2] == "12":
                #it's between midnight and 1 am so 00:MM needs to be returned
                return "00" + input[2:-3]
            elif input[-2:].lower() == 'am':
                #it's in the morning, no need to change anything
                return input[:-3]
            elif input[-2:].lower() == 'pm' and input[:2] == "12":
                #it's between noon and 1 pm, no need to change anything
                return input[:-3]
            elif input[-2:].lower() == 'pm':
                #it's afternoon and 1 pm or later, need to add 12 hours
                return str(int(input[:2]) + 12) + input[2:-3]
            else:
                #if it fails any of the previous checks, it's not in the right format
                print('error, incorrect format')
                return 0
        else:
            #if it fails any of the previous checks, it's not in the right format
            print('error, incorrect format')
            return 0
    else:
        #if it fails any of the previous checks, it's not in the right format
        print('error, incorrect format')
        return 0


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

def display_controls_data(): #display the current controls data
    controlsFrameSem.acquire()
    display_controls = controlsFrame.copy() #get the current frame of the controls data
    controlsFrameSem.release()

    display_data = {}

    display_data["Min Temperature"] = display_controls["current_temp_low"]
    display_data["Max Temperature"] = display_controls["current_temp_high"]
    display_data["Max Humidity"] = display_controls["current_humid_high"]
    display_data["Water Drip Enabled"] = display_controls["current_water_drip_en"]
    display_data["Water Drip Duration"] = display_controls["current_water_drip_duration"]
    display_data["Light Enabled"] = display_controls["current_lights"]
    display_data["Fan Enabled"] = display_controls["current_fan"]
    display_data["Heat Pad Enabled"] = display_controls["current_heat_pad"]

    return json.dumps(display_data)

def display_schd_data(): #display the current controls data
    schedulerFrameSem.acquire()
    schd_controls = schedulerFrame.copy() #get the current frame of the schd data
    schedulerFrameSem.release()

    display_data = {}

    display_data["Water Drip Schedule Enable"] = schd_controls["schd_water_drip_en"]
    display_data["Run the Water Drip At"] = schd_controls["schd_water_drip_time"]
    display_data["Water Drip Duration"] = schd_controls["schd_water_drip_duration"]
    display_data["Water Drip Repeat Interval"] = schd_controls["schd_water_drip_repeat"]
    display_data["Lights Schedule Enable"] = schd_controls["schd_light_en"]
    display_data["Lights Turn On at"] = schd_controls["schd_light_start"]
    display_data["Lights Turn Off at"] = schd_controls["schd_light_stop"]


    return json.dumps(display_data)

@app.route('/') #index of the GUI (the viewable page)
def index():
    return render_template('index.html')

@app.route('/video_feed') #video feed route, this handles the camera
def video_feed_route():
    return Response(camera_frames(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/graph_feed') #graph feed route, this takes in data and renders the graph
def graph_feed_route():
    response = Response(stream_with_context(graph_display()),
    mimetype='text/event-stream')
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

#routes to display the user's current input into the user's controls
@app.route('/current_controls_settings') #display the current control settings
#(for frontend)
def current_controls_settings_route():
    return Response(display_controls_data(), mimetype='application/json')

@app.route('/schd_controls_settings') #display the scheduled control settings
#(for frontend)
def schd_controls_settings_route():
    return Response(display_schd_data(), mimetype='application/json')

#routes to read in data from the user's controls
@app.route('/calendar_feed', methods=["POST"]) #calendar feed route
def calendar_feed_route():
    retrieve_cal = request.get_json() #get the user's input from the GUI

    #recasts the number inputs (which come in as strings)
    retrieve_cal['schd_water_drip_repeat'] = int(retrieve_output['schd_water_drip_repeat'])
    retrieve_cal['schd_water_drip_duration'] = int(retrieve_output['schd_water_drip_duration'])

    schedulerFrameSem.acquire()
    global schedulerFrame
    schedulerFrame = retrieve_cal
    schedulerFrameSem.release()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/controls_feed', methods=["POST"]) #controls feed route
def controls_feed_route():
    retrieve_output = request.get_json() #get the user's input from the GUI

    #recasts the number inputs (which come in as strings), note that the
    #temperatures are floats but the humidity and water drip duration are ints
    retrieve_output['current_temp_low'] = float(retrieve_output['current_temp_low'])
    retrieve_output['current_temp_high'] = float(retrieve_output['current_temp_high'])
    retrieve_output['current_humid_high'] = int(retrieve_output['current_humid_high'])
    retrieve_output['current_water_drip_duration'] = int(retrieve_output['current_water_drip_duration'])

    controlsFrameSem.acquire()
    global controlsFrame
    controlsFrame = retrieve_output
    controlsFrameSem.release()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/read_client', methods=["POST"]) #read data generated by the client,
#this data will be fed to the graph
def read_client_route():
    client_data = request.get_json() #get the data from the data client
    #(the Raspberry Pi code)

    controlsFrameSem.acquire()
    setPoints = controlsFrame.copy() #get the current frame of the controls data
    controlsFrameSem.release()

    graph_data = json.loads(client_data) #add the control set points to the graph

    graph_data['Max Temperature Set Point'] = setPoints['current_temp_high']
    graph_data['Min Temperature Set Point'] = setPoints['current_temp_low']
    graph_data['Max Humidity Set Point'] = setPoints['current_humid_high']

    client_data = json.dumps(graph_data)

    newDataFlagSem.acquire()
    graphFrameSem.acquire()
    global graphFrame, newDataFlag
    graphFrame = client_data #write the new data
    newDataFlag = True #there is new data
    graphFrameSem.release()
    newDataFlagSem.release()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

#routes to allow the data client to read in the user's control values
@app.route('/write_client_controls') #write controls to the client
def write_client_controls_route():
    return Response(send_controls_data(), mimetype='application/json')

@app.route('/write_client_schd') #write scheduler data to the client
def write_client_schd_route():
    return Response(send_schd_data(), mimetype='application/json')

@app.route('/close_doc', methods=["POST"]) #makes sure that when the
#document is closed, all the semaphores are released
def close_doc_route():
    print('the page is reloading')
    schedulerFrameSem.release()
    controlsFrameSem.release()
    graphFrameSem.release()
    newDataFlagSem.release()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port='5000', debug=True, threaded=True, use_reloader=False)
