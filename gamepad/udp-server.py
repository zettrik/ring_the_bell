#!/usr/bin/env python3
import socket
import datetime

# bind all IP
HOST = "0.0.0.0"
# Listen on Port
PORT = 3333
#Size of receive buffer
BUFFER_SIZE = 1024

print("Starting simple UDP server in endless while loop on port %s." % PORT)

# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the host and port
s.bind((HOST, PORT))
while True:
	#data, addr = s.recvfrom(1024)
	#print(datetime.datetime.now(), data.decode(), end='')
	#print(datetime.datetime.now(), addr.decode(), end='')

    # Receive BUFFER_SIZE bytes data
    # data is a list with 2 elements
    # first is data
    # second is client address
    data, addr = s.recvfrom(BUFFER_SIZE)
    if data:
        #print received data
        #print("Message from %s saying: %s " % (data[1], data[0]))
        print("Message from %s saying: %s " % (addr, data))
        # Convert to upper case and send back to Client
        #s.sendto(data[0].upper(), data[1])
        #s.sendto(data[0].upper(), data[1])
# Close connection
s.close()
