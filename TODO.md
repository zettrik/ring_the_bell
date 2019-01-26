# TODOs
* [ ] debug mysterious dmx behaviour
* [ ] fix firmware errors
  * seems like this would help: https://github.com/espressif/arduino-esp32/issues/393
* [ ] add low voltage protection or red warning led on gamepads
  * attiny85 for disconnecting the esp32 when batteries run low
  * circuit itself will need about 10mA
* [ ] build tough connections for leds and buttons in gamepad
* [ ] define game states and implement
* [ ] build wooden gamepad case (comb with 13mm edge length and 13mm depth)
* [ ] setup introduction page; move howto details in separate file
* [ ] gamepad blockdiagram
* [ ] describe off-grid powered version for festivals (solar)
* [ ] check licenses
  * open hardware for own schematics (cern license?)
  * dmxpy MIT license
* [ ] find cool audio samples
* [x] gamepad suggestions for open hardware BMS and 5V step up
* [x] setup wifi in pi server
* [x] clone git to pi server
* [x] build prototype to test gameplay
* [x] gamepad udp send button states (pad no., button no., color, timestamp)
* [x] gamepad recieve game states and change modus (random blinking, waiting, show win/loose...)
* [x] gamepad control button rgb colors
* [x] setup pi server
