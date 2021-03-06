#!/usr/bin/env python3
import socket
import time
import threading

## bind all IP
HOST = "0.0.0.0"
BRDCST = "255.255.255.255"
## Listen on Port
PORT = 3333
## Size of receive buffer
## we use just one byte for the button id
BUFFER_SIZE = 1024

class UDP_Server():
    def __init__(self, port):
        global PORT
        PORT = port
        self.stopped = False
        self.socket = None
        self.thread = None
        self.packets = {}

    def start(self):
        print("start UDP server on port: %s" % PORT)
        ## create a socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ## bind the socket to the host and port
        self.socket.bind((HOST, PORT))
        ## start listening on socket in a thread
        self.thread = threading.Thread(target=self.listen, args=())
        self.thread.start()

    def stop(self):
        ## TODO recvfrom blocks thread as long as no packets were recieved
        ## send an udp packet to shutdown fast
        print("stop UDP server")
        self.stopped = True
        try:
            #self.socket.shutdown(1)
            self.socket.close()
        except:
            print("unclean UDP server shutdown")
        self.thread.join()
        self.thread = None
        self.socket = None

    def listen(self):
        """ infinitly read buffer
        """
        while True:
            ## exit when stop flag is set
            if self.stopped:
                print("exit buffer read loop")
                return

            ## receive BUFFER_SIZE bytes of data
            data, addr = self.socket.recvfrom(BUFFER_SIZE)
            if data:
                self.packets[time.time()] = (addr[0], str(data))
                print("UDP packet from %s saying: %s " % (addr[0], str(data)))

    def clear_packet_cache(self):
        """ remove alle recieved packets from internal variable
        """
        self.packets = {}

    def get_packets(self):
        """ return alle recieved packets since last call and empty queue afterwards
        """
        pckts = self.packets
        self.clear_packet_cache()
        return pckts

    def send(self, msg):
        """ send UDP packet as broadcast
        """
        #print("sending UDP broadcast: %s" % msg)
        message = str(msg).encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(message, (BRDCST, PORT))
        s.close()

    def send_to_ip(self, ip, msg):
        """ send UDP packet to IP
        """
        #print("sending UDP message to IP: %s %s" % (msg, ip))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((ip, PORT))
        s.send(bytes(msg, "utf-8"))
        s.close()

if __name__ == "__main__":
    print("Starting simple UDP server in endless while loop on port %s." % PORT)
    server = UDP_Server(PORT)
    server.start()
    time.sleep(10)
    print("Stopping UDP server.")
    server.stop()
