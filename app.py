import cv2 #openCV for camera controls

import plotly
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import json #to save the data to be displayed
import numpy as np #numpy for random number

import calendar #calender for the timing controls
from datetime import date #date module for current date

from flask import Flask #flask main
from flask import render_template #html pages
from flask import Response #functions

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

def graph_display():
    #the graph display for the page

    #make the graph figure
    value1 = np.array(range(100))
    value2 = np.random.rand(100) * 10

    df = pd.DataFrame({
        'value1': value1,
        'value2': value2
    })

    fig = px.line(df)
    plot(fig, filename='templates/temp-plot.html')

def calendar_display():
    #the calendar display for the page
    today = date.today() #get current date
    cal = calendar.HTMLCalendar(0) #make a calendar

    cal_html = str(cal.formatmonth(today.year, today.month))

    calendar_file = open("templates/temp-calendar.html", "w") #write the calendar
    #to a file
    calendar_file.write(cal_html)
    calendar_file.close()


@app.route('/') #index of the GUI (the viewable page)
def index():
    return render_template('index.html')

@app.route('/video_feed') #video feed route
def video_feed_route():
    return Response(camera_frames(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/graph_feed') #graph feed route
def graph_feed_route():
    return render_template('temp-plot.html')

@app.route('/calendar_feed') #calendar feed route
def calendar_feed_route():
    calendar_display()
    return render_template('temp-calendar.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port='5000', debug=True, threaded=True, use_reloader=False)
