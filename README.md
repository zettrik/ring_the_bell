# ring_the_bell
schneller als wie hau den lukas

## Game Principle
### Rules
The goal of this game is to climb the ladder and ring the bell. But
you won't climb alone. You have to be fast as a team.

The ladder has ten random blinking lights. Every player has a gamepad with three
blinking buttons. They also change the color at random. In one moment a color will
settle on the ladder as one the gamepads. Press as fast as you can all buttons 
with same color. All of you have to hit the right button just in time to climb one
step up.

If one of you ist too slow, the next round will start at the same level.
If one of you hits a wrong button, you fall one step down.

Start of the game will be easy and you might climp up quickly.
But then some unforseen things will happen.

Will you reach the top and ring the bell?


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
### Neopixel
control the lights of the ladder
* https://dordnung.de/raspberrypi-ledstrip/ws2812


## Hardware

### Schematics
![gamepad/gamepad_with_3_buttons_Steckplatine.png]

* https://github.com/espressif/arduino-esp32
* https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
* https://github.com/troelssiggaard/ESP32-fritzing-module - ESP32 wroom Fritzing part

### Bill Of Material
#### Gamecontrolmaster
| Number | Name | Price |
| ------ | ---- | ----- |
| 1x | Pi3 (or an old notebook) | 50€ |
| 1x 5m | Neopixel + power supply  | 50€ |
| | wood | |
| | speaker | |
| | car horn | |
| | flash light | |
| | **sum** | **ca 100€** |

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
| 1x | self made case | 3,00€ |
| | **sum** | **ca 20€** |

