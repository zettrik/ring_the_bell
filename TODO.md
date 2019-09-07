# TODOs
* [ ] test vue.js as frontend
 * http://rafaelescala.com/vue-konva/#/
 * with nuxt
* [ ] define game states
  * [ ] implement finite state machine
* [ ] fix firmware errors
  * seems like this would help: https://github.com/espressif/arduino-esp32/issues/393
* [ ] try MQTT/TCP instead of plain UDP packets and see if performance fits
  * WiFiClient client; WiFi.begin(ssid, password); client.print("foo");
  * https://dzone.com/articles/playing-with-docker-mqtt-grafana-influxdb-python-a
* [ ] build tough connections for leds and buttons in gamepad
* [x] build wooden gamepad case (comb with 13mm edge length and 13mm depth)
* [ ] build wooden gamecontrolmaster case
  * [ ] add coin slot and glass bucket
* [ ] setup introduction page; move howto details in separate file
* [ ] describe off-grid powered version for festivals (solar)
* [ ] check licenses
  * open hardware for own schematics (cern license?)
  * dmxpy MIT license
  * schematic files sources ...
* [ ] find cool audio samples
 * http://99sounds.org/
 * https://opengameart.org/
 * http://dig.ccmixter.org/games
 * https://freesound.org/browse/
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
