# ring_the_bell
schneller als wie hau den lukas

## Game Principle
### Rules Of "Climb The Ladder"
The goal of this game is to climb the ladder and ring the bell. But
you won't climb alone. You have to be fast as a team.

The ladder has ten random blinking lights. Every player has a gamepad with three
blinking buttons. They also change the color at random. In one moment a color will
settle on the ladder as one the gamepads. Press as fast as you can all buttons 
with same color. All of you have to do is hit the right button just in time to 
climb one step up.

If one of you ist too slow, the next round will start at the same level.
If one of you hits a wrong button, you fall one step down.

Start of the game will be easy and you will climp up quickly. As you raise level
your time will shorten. Also some unforseen things might happen at any time.

Will you reach the top and ring the bell?

### Game States
There is only a limited number of differnent states in the game. Test them in
the prototype with the letters in the brackets.
* [r] random blinking
* [t] wait for reactions
* [u] levelling up
* [d] levelling down
* [w] win / reaching top
* [q] quit

## Pyglet Prototype
There is a software prototype of the game for easier development, testing
the rules and joy of gameplay.

It uses pyglet as game engine. To use the prototype under Debian Linux run the following commands:
```
cd prototype
apt install python3-pip
pip3 install -r requirements.txt
python3 prototype.py
```

## Software
### Gamecontrolmaster
* Raspeberry Pi with Debian Stretch
  * install python3 + requirements
  * ntp server - add this line to /etc/ntp.conf:
    * restrict 172.16.2.0 mask 255.255.255.0 nomodify notrap
  * open firewall ports:
    * 123 for ntp
    * 3333 for ingame udp server
  * start prototype.py
    * starts UDP server in separate thread

### Gamepads
* gamepad.ino
  * recieves time from local ntp server
  * recieves game states from gamecontrolmaster
  * animates button colors
  * sends button states to master

### LED Light Bar
* https://www.instructables.com/id/How-to-Use-an-RGB-LED/ - hue2rgb

#### Tri LED Show Bar DMX
* https://www.thomann.de/de/stairville_show_bar_triled_18x3wb_stock.htm
* https://www.ebay.de/itm/Showtec-Cameleon-Bar-12-3-IP65-LED-12x-3W-RGB-Light-DMX-Lichtleiste-Outdoor-/201976229900

* https://github.com/trevordavies095/DmxPy
* https://www.openlighting.org/
  * https://github.com/OpenLightingProject
```
apt install ola
```
* http://localhost:9090

#### Neopixel
control the lights of the ladder
* https://dordnung.de/raspberrypi-ledstrip/ws2812

## Hardware

### Schematics
![gamepad, buttons, leds](gamepad/gamepad_with_3_buttons_Steckplatine.png)

* https://github.com/espressif/arduino-esp32
* https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
* https://github.com/troelssiggaard/ESP32-fritzing-module - ESP32 wroom Fritzing part

### Bill Of Material
#### Gamecontrolmaster
| Number | Name | Price |
| ------ | ---- | ----- |
| 1x | Pi3 with case, sd-card, power supply | 50€ |
| 1x | 18x 3W RGB Tri LED DMX Show Bar  | 200€ |
| | wood | |
| | speaker | |
| | car horn | |
| | **sum** | **ca 250€** |

#### Gamepads (each)
| Number | Name | Price |
| ------ | ---- | ----- |
| 1x | nodemcu | 7€ |
| 1x | li-ion bms | 1€ |
| 1x | 5V step up | 1,50€ |
| 2x | battery holding for 18650 cell | 2€ |
| 3x | rgb LED for buttons | 0,30€ |
| 1x | green LED for on/off | 0,01€ |
| 1x | blue LED for connection status | 0,01€ |
| 1x | kippschalter | 1€ |
| 3x | arcade buttons | 3,60€ |
| 1x | self made wooden case | 10,00€ |
| | **sum** | **ca 30€** |

