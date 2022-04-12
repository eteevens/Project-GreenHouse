
import sys #allows the passage of arguements from the command line, for testing
#purposes

import socket #transfer data between web GUI and other programs

import time

def server(host, port):

    s = socket.socket()         # Create a socket object
    s.bind((host, int(port)))        # Bind to the port
    print(f'Now connected to {host}, {port}')

    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print (f'Got connection from {addr}')
        data = c.recv(1024)
        c.close()                # Close the connection

        return data.decode('UTF-8')

if __name__ == "__main__":
    while True:
        value = server(sys.argv[1], sys.argv[2])
        print(value)
        time.sleep(0.5)
