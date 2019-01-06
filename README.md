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
* [f] freeze, wait for reactions
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
    * shows game state on screen
    * send UDP packets with game state
    * recieves UDP packets with buttons states from pads

#### UDP Packets
* modus can be:
  * 0: nothing
  * 1: Helo
  * 2: Freeze
  * 3: Release
  * 4: NTP resync
  * 5: Animation1
  * 6: Animation2

### Gamepads
* gamepad.ino
  * recieves time from local ntp server
  * recieves commands from gamecontrolmaster
    * game states
    * ntp resync
  * animates button colors
  * sends button states to master

#### UDP Packets
* timestamp, button1, color, dt, button2, color, dt, button3, color, dt
 * dt means after how many ms button was last pressed in this second
 * e.g.: "1546727493, 1,1,0, 2,3,427, 3,1,755"

### RGB Light Bar
* https://www.instructables.com/id/How-to-Use-an-RGB-LED/ - hue2rgb

#### Tri LED Show Bar DMX
* https://www.thomann.de/de/stairville_show_bar_triled_18x3wb_stock.htm
* https://www.ebay.de/itm/Showtec-Cameleon-Bar-12-3-IP65-LED-12x-3W-RGB-Light-DMX-Lichtleiste-Outdoor-/201976229900
* https://www.ebay.de/itm/U-king-72W-10PCS-36LED-Par-RGB-Buhnenlicht-DMX-512-Disco-DJ-Wedding-Party-Lichts/292784228642?hash=item442b4cc922:g:irwAAOSwRNhbzr0r:rk:13:pf:0
* https://www.ebay.de/itm/U-king-10STK-36W-Buhnenlicht-18LED-Par-RGB-Licht-7CH-Channel-Disco-Wedding-Party/292806135256?_trkparms=aid%3D444000%26algo%3DSOI.DEFAULT%26ao%3D1%26asc%3D20170221122447%26meid%3D339054517f2c4988a4da3474d06ac717%26pid%3D100752%26rk%3D3%26rkt%3D6%26sd%3D292784228642%26itm%3D292806135256&_trksid=p2047675.c100752.m1982
* https://www.ebay.de/itm/10stk-RGBW-12LED-Par-Buhnenbeleuchtung-DMX512-Licht-Disco-Party-Lichteffekt-F2Y1/183417140600?_trkparms=aid%3D222007%26algo%3DSIM.MBE%26ao%3D1%26asc%3D52545%26meid%3D2c4fce730ffb4a258fd2ce8ef1319b32%26pid%3D100010%26rk%3D6%26rkt%3D12%26sd%3D292784228642%26itm%3D183417140600&_trksid=p2047675.c100010.m2109
* https://www.ebay.de/itm/24x-3W-RGB-LED-Bar-Wall-Washer-8-Sektionen-DMX-Stage-Scheinwerfer-Lichtleiste/332858111664?epid=26014989146&hash=item4d7fe3b6b0:g:gCoAAOSwhZ5b1vIN:rk:10:pf:0

* https://github.com/trevordavies095/DmxPy
* https://www.openlighting.org/
  * https://github.com/OpenLightingProject
```
apt install ola
```
* http://localhost:9090

#### LED Stripes, Neopixel
* https://dordnung.de/raspberrypi-ledstrip/ws2812
* https://diystagedesign.wordpress.com/2014/06/06/rgb-led-strip-panels/

#### DIY Power LED
* 10x RGB 3W LED
* I2C shield
* 3.3V-5V level shifter: 74HCT245
* Darlington ULN2003 with multi channel use or 3.3V n-channel mosfet
* https://learn.adafruit.com/rgb-led-strips/usage
* http://www.tbideas.com/blog/build-an-arduino-shield-to-drive-high-power-rgb-led/

## Hardware

### Schematics
![gamepad, buttons, leds](gamepad/gamepad_with_3_buttons_Steckplatine.png)

* https://github.com/espressif/arduino-esp32
* https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
* https://github.com/troelssiggaard/ESP32-fritzing-module - ESP32 wroom Fritzing part

### Bill Of Material
#### Gamecontrolmaster & Light Bar
| Number | Name | Price |
| ------ | ---- | ----- |
| 1x | Pi3 with case, sd-card, power supply | 50€ |
| 1x | Light Bar | 200€ |
| 11x | comb from 6x wood (12mm x 12mm x 9mm)| 30€ |
| 11x | milk glass as front plate for combs (24mm x 24mm) | 70€ |
| 11x | wooden back plate for combs (24mm x 24mm) | 70€ |
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
| 1x | comb from 6x wood (12mm x 12mm x 9mm)| 3€ |
| | **sum** | **ca 30€** |

