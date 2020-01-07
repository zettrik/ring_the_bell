# Display


## Projector + 10x Canvas 

The quick and cheap way...
* build ten white canvases in hexagonal comb form
* use projector and mapping tool
* connect projector to Pi HDMI 


## Tri LED Show Bar, DMX controlled

Use standard hardware for theaters and clubs, allows better scaling and reuseable elements.
Lights are connected to each other and to the controller with XLR cable/plugs in series. [DMX Basics](http://www.lutron.com/en-US/education-training/Documents/dmx%20webinar_7-29-2010.pdf)

Setup: power plug :arrow_left: USB :arrow_right: Raspberry Pi :arrow_left: USB :arrow_right: USB-DMX controller :arrow_left: XLR :arrow_right: RGB Lights

### A) Light Bars
compact, costs around 200-400€

* https://www.thomann.de/de/stairville_show_bar_triled_18x3wb_stock.htm
* https://www.ebay.de/itm/Showtec-Cameleon-Bar-12-3-IP65-LED-12x-3W-RGB-Light-DMX-Lichtleiste-Outdoor-/201976229900
* https://www.ebay.de/itm/U-king-72W-10PCS-36LED-Par-RGB-Buhnenlicht-DMX-512-Disco-DJ-Wedding-Party-Lichts/292784228642?hash=item442b4cc922:g:irwAAOSwRNhbzr0r:rk:13:pf:0
* https://www.ebay.de/itm/U-king-10STK-36W-Buhnenlicht-18LED-Par-RGB-Licht-7CH-Channel-Disco-Wedding-Party/292806135256?_trkparms=aid%3D444000%26algo%3DSOI.DEFAULT%26ao%3D1%26asc%3D20170221122447%26meid%3D339054517f2c4988a4da3474d06ac717%26pid%3D100752%26rk%3D3%26rkt%3D6%26sd%3D292784228642%26itm%3D292806135256&_trksid=p2047675.c100752.m1982
* https://www.ebay.de/itm/10stk-RGBW-12LED-Par-Buhnenbeleuchtung-DMX512-Licht-Disco-Party-Lichteffekt-F2Y1/183417140600?_trkparms=aid%3D222007%26algo%3DSIM.MBE%26ao%3D1%26asc%3D52545%26meid%3D2c4fce730ffb4a258fd2ce8ef1319b32%26pid%3D100010%26rk%3D6%26rkt%3D12%26sd%3D292784228642%26itm%3D183417140600&_trksid=p2047675.c100010.m2109
* https://www.ebay.de/itm/24x-3W-RGB-LED-Bar-Wall-Washer-8-Sektionen-DMX-Stage-Scheinwerfer-Lichtleiste/332858111664?epid=26014989146&hash=item4d7fe3b6b0:g:gCoAAOSwhZ5b1vIN:rk:10:pf:0

### B) LED Par
10x Pars

* https://www.amazon.de/dp/B07D8MHP9J/ref=psdc_528377031_t1_B07J4TPDG2
* https://www.amazon.de/dp/B07G87HGR8/ref=psdc_528377031_t3_B07J4TPDG2
* https://www.amazon.de/Bühnenbeleuchtung-Latta-Alvor-Lichteffekte-Partybeleuchtung/dp/B07BN9SH4J/

* [Dip Switch Calculator](https://www.chauvetdj.com/chauvet-dj-dip-switch-calculator/)

### DMX Controller
You a need an USB controller for sending DMX signals to the lights.

* USB to DMX adapter
  * Enttec Enttec Open DMX USB (70€)
    * basic USB to DMX converter, lacks microprocessor control, will hiccup if your computer gets stuck
  * Enttec DMX USB Pro MK2, with Linux support (190€)
  * https://www.elektormagazine.de/news/isolierter-usb-dmx512-konverter-1-kv
  * self made adapters: [search e.g. on easyeda.com](https://easyeda.com/search?wd=usb%20dmx)

#### Enttec DMX USB Pro Mk2
* PRO Mk2 comes with a RGB LED indicator located on the top (above the usb connector). The LED will blink between these colours, and each colour signifies the related activity:
  * white: PRO Mk2 is powered on and idle
  * green: DMX1 send or receive (DMX Port 1)
  * yellow: DMX2 send or receive (DMX Port 2)
  * blue: standalone mode (show playback)
  * purple: MIDI in or out
  * red: error or unsupported request

#### DMX Software
* [DmxPy](https://github.com/trevordavies095/DmxPy) - Control USB-DMX Hardware with Python 3. Works with Raspberry Pi and supports Enttec DMX USB Pro.
  * is included in the prototype
* [Open Lighting Architecture](https://www.openlighting.org/) - take a look if you're thinking bigger
* http://www.raspberrypi-dmx.org
* http://www.lightingandsoundamerica.com/mailing/PLASAProtocol/PSummer2015_BuildYourOwnDMXTester.pdf


## DIY Power LED

This is way cheaper than DMX Hardware. You basically need some power LEDs and a
multiplexer. You won't need DMX but will have fun with your own protocol.

* 10x RGB 3W LED
* 3.3V multiplexer 
 * for arduino a 5V would do it: 74HCT245
* some Darlington ULN2003A 
  * 500mA per channel; multi channel possible
  * or use 30x 3.3V n-channel mosfet

* https://learn.adafruit.com/rgb-led-strips/usage
* http://www.tbideas.com/blog/build-an-arduino-shield-to-drive-high-power-rgb-led/


## DIY LED Stripes, Neopixel

Cut stripes in pieces and bring them in form for the combs. Control with
mosfets or darlington + multiplexer (same as with power LEDs).

* https://dordnung.de/raspberrypi-ledstrip/ws2812
* https://diystagedesign.wordpress.com/2014/06/06/rgb-led-strip-panels/
* https://www.instructables.com/id/Driving-RGB-LED-strips-off-an-Arduino/
* https://www.hackerspace-bamberg.de/Dmx2rgb

