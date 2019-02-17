# TODOs
* [ ] define game states
  * [ ] implement finite state machine
* [ ] fix firmware errors
  * seems like this would help: https://github.com/espressif/arduino-esp32/issues/393
* [ ] try MQTT/TCP instead of plain UDP packets and see if performance fits
* [ ] build tough connections for leds and buttons in gamepad
* [ ] build wooden gamepad case (comb with 13mm edge length and 13mm depth)
* [ ] setup introduction page; move howto details in separate file
* [ ] describe off-grid powered version for festivals (solar)
* [ ] check licenses
  * open hardware for own schematics (cern license?)
  * dmxpy MIT license
  * schematic files sources ...
* [ ] find cool audio samples
* [x] gamepad blockdiagram
* [x] add low voltage disconnect and red warning on gamepads
* [x] debug mysterious dmx behaviour 
 * Enttec USB DMX Pro Mk2 needs 300mA @ 5V supply
 * Pi USB output seems to be not stable enough, also not with USB hub
 * power supply for Pi must be sufficient
* [x] gamepad suggestions for open hardware BMS and 5V step up
* [x] setup wifi in pi server
* [x] clone git to pi server
* [x] build prototype to test gameplay
* [x] gamepad udp send button states (pad no., button no., color, timestamp)
* [x] gamepad recieve game states and change modus (random blinking, waiting, show win/loose...)
* [x] gamepad control button rgb colors
* [x] setup pi server
