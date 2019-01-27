#!/usr/bin/env python3

"""
Thanks to Dave Paul for DMXPy and Trevor Davies who ported it to Python3.

* https://github.com/davepaul0/DmxPy
* https://github.com/trevordavies095/DmxPy

MIT License

Copyright (c) 2018 L Trevor Davies

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import serial, sys
import time


DMXOPEN = bytes([126])
DMXCLOSE = bytes([231])
DMXINTENSITY = bytes([6]) + bytes([1]) + bytes([2])
DMXINIT1 = bytes([3]) + bytes([2]) + bytes([0]) + bytes([0]) + bytes([0])
DMXINIT2 = bytes([10]) + bytes([2]) + bytes([0]) + bytes([0]) + bytes([0])


class DMX:
    def __init__(self, serialPort):
        try:
            self.serial = serial.Serial(serialPort, baudrate=57600)
        except:
            print("Error: could not open Serial Port")
            sys.exit(0)
        self.serial.write(DMXOPEN + DMXINIT1 + DMXCLOSE)
        self.serial.write(DMXOPEN + DMXINIT2 + DMXCLOSE)
        self.dmxData = [bytes([0])] * 513   #128 plus "spacer".
        self.blackout()
        self.render()


    def setChannel(self, chan, intensity):
        if chan > 512: chan = 512
        if chan < 0: chan = 0
        if intensity > 255: intensity = 255
        if intensity < 0: intensity = 0
        self.dmxData[chan] = bytes([intensity])


    def blackout(self):
        for i in range(1, 512, 1):
            self.dmxData[i] = bytes([0])

    def set_rgb(self, base_channel=1, color=0):
        if color == 0: self.set_black(base_channel)
        if color == 1: self.set_red(base_channel)
        if color == 2: self.set_green(base_channel)
        if color == 3: self.set_blue(base_channel)
        if color == 4: self.set_white(base_channel)
        if color == 5: self.set_gold(base_channel)

    def set_black(self, channel):
        self.setChannel(channel + 0, 0)
        self.setChannel(channel + 1, 0)
        self.setChannel(channel + 2, 0)
        self.setChannel(channel + 3, 0)
        self.setChannel(channel + 4, 0)

    def set_red(self, channel):
        self.setChannel(channel + 0, 255)
        self.setChannel(channel + 1, 0)
        self.setChannel(channel + 2, 0)
        self.setChannel(channel + 3, 0)
        self.setChannel(channel + 4, 0)

    def set_green(self, channel):
        self.setChannel(channel + 0, 0)
        self.setChannel(channel + 1, 255)
        self.setChannel(channel + 2, 0)
        self.setChannel(channel + 3, 0)
        self.setChannel(channel + 4, 0)

    def set_blue(self, channel):
        self.setChannel(channel + 0, 0)
        self.setChannel(channel + 1, 0)
        self.setChannel(channel + 2, 255)
        self.setChannel(channel + 3, 0)
        self.setChannel(channel + 4, 0)

    def set_white(self, channel):
        self.setChannel(channel + 0, 255)
        self.setChannel(channel + 1, 255)
        self.setChannel(channel + 2, 255)
        self.setChannel(channel + 3, 255)
        self.setChannel(channel + 4, 0)

    def set_gold(self, channel):
        self.setChannel(channel + 0, 255)
        self.setChannel(channel + 1, 255)
        self.setChannel(channel + 2, 0)
        self.setChannel(channel + 3, 0)
        self.setChannel(channel + 4, 0)

    def render(self):
        sdata = b''.join(self.dmxData)
        ## repeat serial.write - usb adapter works unreliable at the raspberry pi
        for i in range(0, 3):
            self.serial.write(DMXOPEN + DMXINTENSITY + sdata + DMXCLOSE)
            time.sleep(0.05)

    def rotate_rgb(self):
        lights = {   1: [255,0,0,0], 11: [0,255,0,0], 21:[0,0,255,0],
                    31: [255,0,0,0], 41: [0,255,0,0], 51:[0,0,255,0],
                    61: [255,0,0,0], 71: [0,255,0,0], 81:[0,0,255,0],
                    91: [255,0,0,0] }
        self.set_lights(lights)
        time.sleep(0.25)
        lights = {   1: [0,255,0,0], 11: [0,0,255,0], 21:[255,0,0,0],
                    31: [0,255,0,0], 41: [0,0,255,0], 51:[255,0,0,0],
                    61: [0,255,0,0], 71: [0,0,255,0], 81:[255,0,0,0],
                    91: [0,255,0,0] }
        self.set_lights(lights)
        time.sleep(0.25)
        lights = {   1: [0,0,255,0], 11: [255,0,0,0], 21:[0,255,0,0],
                    31: [0,0,255,0], 41: [255,0,0,0], 51:[0,255,0,0],
                    61: [0,0,255,0], 71: [255,0,0,0], 81:[0,255,0,0],
                    91: [0,0,255,0] }
        self.set_lights(lights)
        time.sleep(0.25)

    def set_lights(self, lights):
        print(lights.keys())
        print(lights.values())
        dmx.blackout()
        for light in lights.keys():
            for channel in range(0, len(lights[light])):
                dmx_address = int(light + channel)
                brightness = lights[light][channel]
                dmx.setChannel(dmx_address, brightness)
        dmx.render()


if __name__ == "__main__":
    print("Testing RGB with DMX Controller.")
    dmx = DMX("/dev/ttyUSB0")
    while True:
        dmx.rotate_rgb()

