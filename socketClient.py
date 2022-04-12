
import sys #allows the passage of arguements from the command line, for testing
#purposes

import socket #transfer data between web GUI and other programs

def client(host, port, data):

    messages = data.encode('UTF-8')
#    print(f'Your message is: {messages}')

    s = socket.socket()         # Create a socket object

    s.connect((host, int(port)))
#    print(f'Now connected to {host}, {port}')
    s.send(messages)
    s.close()                     # Close the socket when done

if __name__ == "__main__":
    for i in range(3):
        client(sys.argv[1], sys.argv[2], sys.argv[3])
