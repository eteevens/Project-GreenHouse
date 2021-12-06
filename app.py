import cv2 #openCV for camera controls

import plotly
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import json #to save the data to be displayed
import numpy as np #numpy for random number

from flask import Flask #flask main
from flask import render_template #html pages
from flask import Response #functions

app = Flask(__name__) #initalize the web application

def camera_frames():
    #the camera feed for the page

    vc = cv2.VideoCapture(0) #temporary taking of video feed from computer camera

    while True:
        success, frame = vc.read() #read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            outputFrame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + outputFrame + b'\r\n')

    vc.release()

@app.route('/temp-plot.html')
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
    plot(fig, filename='temp-plot.html')


@app.route('/') #index of the GUI (the viewable page)
def index():
    return render_template('index.html')

@app.route('/video_feed') #video feed route
def video_feed_route():
    return Response(camera_frames(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port='5000', debug=True, threaded=True, use_reloader=False)
