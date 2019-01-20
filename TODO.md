# TODOs
* [ ] fix firmware errors
  * seems like this would help: https://github.com/espressif/arduino-esp32/issues/393
* [ ] add low voltage protection + red led on gamepads
  * attiny85 for disconnecting the esp32 when batteries run low
  * circuit itself will need about 10mA
* [ ] build tough connections for leds and buttons in gamepad
* [ ] define game states and implement
* [ ] build wooden gamepad case (comb with 13mm edge length and 13mm depth)
* [ ] describe off-grid powered version for festivals (solar)
* [x] setup wifi in pi server
* [x] clone git to pi server
* [x] build prototype to test gameplay
* [x] gamepad udp send button states (pad no., button no., color, timestamp)
* [x] gamepad recieve game states and change modus (random blinking, waiting, show win/loose...)
* [x] gamepad control button rgb colors
* [x] setup pi server
