# Gamecontrolmaster


## Pyglet Prototype

There is a software prototype of the game for easier development, testing
the rules and joy of gameplay.

![Screenshot Prototype](doc/prototype_screenshot.png)

It uses pyglet as game engine. Most software the protoype depends on is in the
Debian Linux distribution. The newest version of pyglet comes via pip. Install
with the following commands.
```
cd prototype
apt install python3-pip freeglut3-dev python3-serial
pip3 install -r requirements.txt
python3 prototype.py
```

### Start on Boot
* create /lib/systemd/system/prototype.service with:
```
[Unit]
Description=Prototype
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/ring_the_bell/prototype/
ExecStart=/usr/bin/python3 prototype.py

[Install]
WantedBy=multi-user.target
```
* chmod 644 /lib/systemd/system/prototype.service
* systemctl daemon-reload
* systemctl enable prototype.service

### Keybindings (Pre State Machine)

There is only a limited number of differnent states in the game. Test them in
the prototype with the letters in the brackets.
* [s] start
* [t] request gamepads to resync their time (ntp)
* [r] random blinking
* [f] freeze, wait for reactions
* [e] release
* [u] level up
* [d] level down
* [w] win
* [q] quit


## Raspberry Pi With Raspbian (Debian Stretch)

* Install [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
* You will need these essential Debian packages for gamecontrolmaster:
  * `python3 ntp`
  * Also install python3 from requirements.txt.
* There is no standalone mode yet. Use the gamemaster headless via ssh, in addition with the following handy packages:
  * `git` - to get the software
  * `screen` - for disruptable ssh sessions
  * `htop` - resource monitoring
  * `mc` - commandline file manager
  * `tcpdump` - debug network traffic
  * `vim` - file editor
* For all features install a dekstop like fluxbox
  * `lightdm fluxbox lxterminal bbrun`

## Components

### Wifi In AP Mode

* [Raspberry Pi help on this](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)
* name: "speedybees"
* password: "rockyoursocksoff"
* IP address: 172.16.2.2
* or set up a separate access point instead of the onboard chip
  * switch wifi to client mode on Pi
  * leave IP address of Rapsberry Pi: 172.16.2.2
  * set IP address of access point: 172.16.2.1
  * use same wifi name + credentials or recompile firmware for gamepads
  * enable DHCP server on access point for address range: 172.16.2.3 - 172.16.2.254
  * no internet connection or DNS is needed but it will nat an existing one

### NTP

* ntp server - add this line to /etc/ntp.conf:
  * restrict 172.16.2.0 mask 255.255.255.0 nomodify notrap

### Firewall

* open firewall ports:
  * 123 for ntp
  * 3333 for ingame udp server

### non-root USB

* allow non-root users access to the USB interface:
  * adduser <your_pi_user> dialout

### prototype.py

* start prototype.py
  * starts UDP server in separate thread
  * shows game state on screen
  * send UDP packets with game state
  * recieves UDP packets with buttons states from pads


## Troubleshooting

In case you're building this setup the first time or you have trouble with some
components here are some debugging hints:

* take a look at /var/log/daemon.log for connected gamepads (and other clients)
* see ntp requests (changed timestamps) with: tcpdump -i wlan0 -v -n port 123
* see udp packets (transmitted game signals) with: tcpdump -i wlan0 -n port 3333
  * -tt for unix timestamp
  * -X for ASCII content of packets
* test basic DMX signals with: python3 prototype/libs/dmx.py
  * or: apt install ola
  * and try ola_dmxmonitor and ola_dmxconsole


