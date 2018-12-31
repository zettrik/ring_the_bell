#!/usr/bin/env python3
import socket
import sys
import time

UDP_IP = "localhost"
UDP_PORT = 3333


print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#s.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
s.connect((UDP_IP, UDP_PORT))
msg = ""
while True:
    print("enter message: ")
    msg = cmd=sys.stdin.readline()
    print(time.time())
    s.send(bytes(msg, "utf-8"))
s.close()
