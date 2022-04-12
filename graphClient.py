
import json #to send the data to be displayed on the graph and recieve data
#from the controls
import numpy as np #numpy for random number

import socket #transfer data between web GUI and other programs

from datetime import datetime #date module for current date, time module
#for the current time for the graph

import time #allows the random data to wait

from socketClient import client #import the client for data sending

Host = "127.0.0.1"
Port = 5500

value1 = 0

if __name__ == "__main__":
    while True:

        value1 = (value1 + 15) % 100
        value2 = int(np.random.rand() * 100)
        value3 = int(np.random.rand() * 100)

        data_to_send = {'time':datetime.now().strftime('%H:%M:%S')}

        data_to_send['Temperature (in F)'] = value1
        data_to_send['Humidity'] = value2
        data_to_send['Light Level'] = value3

        json_data = json.dumps(data_to_send)
        client(Host, Port, json_data)

        time.sleep(0.5)
