import requests #send/recieve data from the GUI

import json #to send the data to be displayed on the graph and recieve data
#from the controls
import numpy as np #numpy for random number

from datetime import datetime #date module for current date, time module
#for the current time for the graph

import time #allows the random data to wait

url = "http://127.0.0.1:5000" #address of the server

write_to_app = url + "/read_client" #server page for read
read_controls_from_app = url + "/write_client_controls"
#server page for writing controls
read_schd_from_app = url + "/write_client_schd"
#server page for writing scheduler

checkRateGraph = 0.5 #how often to write to the graph (temp value)

def send_and_recieve():

    value1 = 0 #triangle wave fake data

    counter = 0 #for when the data should be read from the app, temp value

    while True:
        value1 = (value1 + 15) % 100
        value2 = int(np.random.rand() * 100) #random fake data
        value3 = int(np.random.rand() * 100)
        value4 = 95
        value5 = 10
        value6 = 85
        value7 = 50

        data_to_send = {'time':datetime.now().strftime('%H:%M:%S')}
        #adds the time to the json to be sent, this MUST be sent because
        #that is what fills out the y-axis of the graph

        data_to_send['Temperature (in F)'] = value1 #name of the data (to be displayed) : value
        data_to_send['Humidity'] = value2
        data_to_send['Light Level'] = value3
        data_to_send['Max Temperature Set Point'] = value4
        data_to_send['Min Temperature Set Point'] = value5
        data_to_send['Max Humidity Set Point'] = value6
        data_to_send['Day/Night Line'] = value7

        json_data = json.dumps(data_to_send) #turns the data into a JSON string

        requests.post(write_to_app, json=json_data) #posts data to the write address

        if counter == 6:
            controls_data = requests.get(read_controls_from_app, timeout=10)
            #reads from the read from controls address

            print(controls_data.json()) #print out what is read

            schd_data = requests.get(read_schd_from_app, timeout=10)
            #reads from the read from scheduler address

            print(schd_data.json()) #print out what is read

            counter = 0

        time.sleep(checkRateGraph) #wait
        counter = counter + 1 #increment the counter

if __name__ == "__main__":
    send_and_recieve()
