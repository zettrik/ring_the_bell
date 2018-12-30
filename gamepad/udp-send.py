#!/usr/bin/env python3
import socket

UDP_IP = "172.16.2.165"
UDP_PORT = 3333

MESSAGE = "bar"

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#s.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
s.connect((UDP_IP, UDP_PORT))
s.send(bytes(MESSAGE, "utf-8"))
s.close()
