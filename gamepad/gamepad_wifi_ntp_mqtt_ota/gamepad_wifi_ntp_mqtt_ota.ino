#include <WiFi.h>
#include <EspMQTTClient.h>
#include <time.h>
#include <esp_wifi.h>
//#include <ESPmDNS.h>  // for ota
//#include <WiFiUdp.h>  // for ota
#include <ArduinoOTA.h>  // for ota

/* gamepad info & modes*/
const char *my_name = "gamepad-uno";
const int gamepad_version = 2;
char game_mode = ' ';
unsigned long mode_interval = 1000000; // 1s in µs
unsigned long send_interval = 10000000; // 10s in µs

/* wifi */
//const char *ssid = "speedybees";
//const char *password = "rockyoursocksoff";
const char *ssid = "Bill Hicks";
const char *password = "blum3ngi3ss3n";
IPAddress local_ip(127, 0, 0, 0); // will be set via dhcp
WiFiClient espClient;
unsigned long wifi_connects = 0;
long wifi_signal = 0;

/* mqtt */
EspMQTTClient mqtt_client(
  "WifiSSID",
  "WifiPassword",
  "192.168.1.111",  // MQTT Broker server ip
  "", // mqtt user
  "", // mqtt pw
  "uno" // client name
);
const char *topic_status = "gamepad/dos/status";
const char *topic_in = "gamepad/dos/in";
const char *topic_out = "gamepad/dos/out";
const char *topic_mode = "gamepad/dos/mode";
char msg[15];

/* I/O */
const byte led0 = 5; // on board LED
const byte led_1_r = 32; // G32, red LED on first button
const byte led_1_g = 33; // G23
const byte led_1_b = 25; // G25
const byte led_2_r = 26; // G26
const byte led_2_g = 27; // G27
const byte led_2_b = 14; // G14
const byte led_3_r = 12; // G12
const byte led_3_g = 13; // G13
const byte led_3_b = 4;  // G4, blue LED on third button
const byte button1 = 36; // first input button
const byte button2 = 39;
const byte button3 = 34;
const byte touch1 = 15; // Touch Sensor 3 at G15
const byte bat_sensor = 2; // G2, connect to batterie (+)
byte button1_state = 0;
byte button2_state = 0;
byte button3_state = 0;
byte button1_pressed = 0;
byte button2_pressed = 0;
byte button3_pressed = 0;
unsigned long button1_presstime = 0;
unsigned long button2_presstime = 0;
unsigned long button3_presstime = 0;
int touch_value1 = 0;

/* ntp */
const char *ntpServer = "1.debian.pool.ntp.org";
//const char *ntpServer = "172.16.2.2";
const unsigned long check_ntp_interval = 36000000;
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;
unsigned long now = 0;
unsigned long before = 0;
unsigned long interval_before = 0;
unsigned long rtc_now;
unsigned long time_delta;
unsigned long ntp_last_check;
time_t unixseconds;
struct timeval thistime;

/* buttons leds */
//long random;


void setup() {
  Serial.begin(115200);
  Serial.println("===");
  Serial.print("my name is: ");
  Serial.println(my_name);
  Serial.print("version: ");
  Serial.println(gamepad_version);
  Serial.println("---");
  setCpuFrequencyMhz(240);
  pinMode(led0, OUTPUT);
  digitalWrite(led0, 0);
  pinMode(led_1_r, OUTPUT);
  pinMode(led_1_g, OUTPUT);
  pinMode(led_1_b, OUTPUT);
  pinMode(led_2_r, OUTPUT);
  pinMode(led_2_g, OUTPUT);
  pinMode(led_2_b, OUTPUT);
  pinMode(led_3_r, OUTPUT);
  pinMode(led_3_g, OUTPUT);
  pinMode(led_3_b, OUTPUT);
  pinMode(button1, INPUT_PULLDOWN);
  pinMode(button3, INPUT_PULLDOWN);
  pinMode(button2, INPUT_PULLDOWN);
  pinMode(bat_sensor, INPUT_PULLDOWN);

  check_battery();    
   
  // initialize random number generator
  randomSeed(analogRead(0));

  // system starting, all buttons blue
  buttons_all_blue();
  setup_wifi();
  setup_mqtt();
  get_ntp_time();
  
  
  // let all button leds blink so gamer sees everything is working
  //buttons_rotation();
  buttons_single_color();
  buttons_flash();
  // system is up, green leds for 3 sec
  buttons_all_green();
  delay(1000);
  buttons_all_off();

  // prepare firmware updates over the air
  // keep the firewall on your arduino dev pc open
  setup_ota();
}

void loop() {
  ArduinoOTA.handle(); // listening for new firmwares
  check_battery();
  gettimeofday(&thistime, NULL);
  now = (thistime.tv_sec * 1000000 + thistime.tv_usec);
  //now = system_get_time();
  read_buttons();
  
  read_touchsensors();
  mqtt_client.loop();

  /* regular status reports */
  if ((before + send_interval) <= now) {
    check_wifi_signal();
    mqtt_client.publish(topic_status, String(wifi_signal));
    read_touchsensors();
    mqtt_client.publish(topic_status, String(touch_value1));
    before = now;
    send_button_times();
    reset_buttons();
  }
  
  /* game modes */
  if ((interval_before + mode_interval) < now) {
    if (game_mode == 'r') {
      Serial.println("in random mode");
      mode_random();
    }
    else if (game_mode == 'f') {
      Serial.println("in freeze mode");
      mqtt_client.publish(topic_mode, "f");
      mode_freeze();
    }
    else {
      //buttons_rotation();
      //print_local_time();
    }
    Serial.print("now: ");
    Serial.println(now);
    interval_before = now;
  }
}

/*
 * read touch sensors
 */
void read_touchsensors() {
  touch_value1 = touchRead(touch1);
  //Serial.print("touch: ");
  //Serial.println(touch_value1);
}

/*
 * read actual state of buttons
 */
void read_buttons() {
  button1_state = digitalRead(button1);
  button2_state = digitalRead(button2);
  button3_state = digitalRead(button3);
  // save the first time a button was pressed in this interval
  if ((button1_state == 1) && (button1_pressed == 0)) {
    button1_pressed = 1;
    button1_presstime = now - before;
  }
  if ((button2_state == 1) && (button2_pressed == 0)) {
    button2_pressed = 1;
    button2_presstime = now - before;
  }
  if ((button3_state == 1) && (button3_pressed == 0)) {
    button3_pressed = 1;
    button3_presstime = now - before;
  }
}

/*
 * send button states via mqtt
 */
void send_button_times() {
  digitalWrite(led_1_r, 1);
  sprintf(msg,"%16lu", button1_presstime);
  
  // some debug infos...
  Serial.println("press times in micro seconds (b1, b2, b3)");
  Serial.print(button1_presstime);
  Serial.print(", ");
  Serial.print(button2_presstime);
  Serial.print(", ");
  Serial.println(button3_presstime);
  time(&unixseconds);
  Serial.print("unixseconds: ");
  Serial.println(unixseconds);
  Serial.print("uptime: ");
  Serial.println(now);
  
  mqtt_client.publish(topic_out, "b1");
}

void reset_buttons() {
  button1_pressed = 0;
  button2_pressed = 0;
  button3_pressed = 0;
  button1_presstime = 0;
  button2_presstime = 0;
  button3_presstime = 0;
  digitalWrite(led_1_r, 0);
}

/*
 * low voltage shutdown
 */
void check_battery() { 
  if (digitalRead(bat_sensor) < 600) {
    buttons_all_red();
    //delay(3000);
    //shutdown();
  }
}

void shutdown() {
  Serial.println("Low voltage shutoff is not yet implemented.");
}

/*
 * wifi
 */
void setup_wifi() {
  WiFi.softAPdisconnect(true);
  WiFi.disconnect(true);
  WiFi.persistent(false); //  every wifi.begin() writes to flash, this stops it
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Starting wifi connection");
  // Try max. 20 seconds to connect to access point.
  //while(WiFi.status() != WL_CONNECTED) {
  for (int i = 0; i <= 79; i++) {
    // blink slowly while connecting
    digitalWrite(led0, 0);
    delay(250);
    digitalWrite(led0, 1);
    delay(125);
    digitalWrite(led0, 0);
    Serial.print(".");
    if (WiFi.status() == WL_CONNECTED) {
      i = 80;
      wifi_connects += 1;
    }
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  local_ip = WiFi.localIP();
  Serial.println(local_ip);
  for (int i = 0; i < 10; i++) {
    // blink fast when successful
    digitalWrite(led0, 0);
    delay(25);
    digitalWrite(led0, 1);
    delay(25);
  }
}

/*
 * wifi signal strength
 */
void check_wifi_signal(){
  wifi_signal = 0;
  for (int i = 0; i < 5; i++){
    wifi_signal += WiFi.RSSI();
    delay(20);
  }
  wifi_signal = wifi_signal / 5;
  //Serial.print("wifi signal strength: ");
  //Serial.println(wifi_signal);
}

/*
 * mqtt
 */
void setup_mqtt() {
  mqtt_client.enableDebuggingMessages();
}
// This function is called once everything is connected (Wifi and MQTT)
// WARNING : YOU MUST IMPLEMENT IT IF YOU USE EspMQTTClient
void onConnectionEstablished()
{
  // Subscribe to topic and display received message to Serial
  mqtt_client.subscribe(topic_in, [](const String & payload) {
    Serial.print("mqtt recieved at unixseconds: ");
    Serial.println(unixseconds);
    Serial.print("  now: ");
    Serial.println(now);
    Serial.print("mqtt message: ");
    Serial.println(payload);
    if ( payload == "t") {
      mqtt_client.publish(topic_mode, String('t'));
      mqtt_client.publish(topic_out, String(unixseconds));
      mqtt_client.publish(topic_out, String(now));
      get_ntp_time();
    }
    if ( payload == "r") {
      mqtt_client.publish(topic_mode, String('r'));
      mode_random();
    }
    if ( payload == "f") {
      mqtt_client.publish(topic_mode, String('f'));
      mqtt_client.publish(topic_out, String(unixseconds));
      mqtt_client.publish(topic_out, String(now));
      mode_freeze();
    }
    
    mqtt_client.publish(topic_out, String(payload));
  });

  // Publish a message to topic
  //mqtt_client.publish("test/foo", "hooooray"); // You can activate the retain flag by setting the third parameter to true
  // Execute delayed instructions
  //mqtt_client.executeDelayed(5 * 1000, []() {
    //mqtt_client.publish("test/foo", "5 seconds later");
  //});
}

/*
 * flash firmware over the air
 */
void setup_ota() {
  // Port defaults to 3232
  //ArduinoOTA.setPort(3232);
  // Hostname defaults to esp3232-[MAC]
  ArduinoOTA.setHostname(my_name);
  // No authentication by default
  //ArduinoOTA.setPassword("admin");
  // Password can be set with it's md5 value as well
  // MD5(admin) = 21232f297a57a5a743894a0e4a801fc3
  //ArduinoOTA.setPasswordHash("21232f297a57a5a743894a0e4a801fc3");

  ArduinoOTA.onStart([]() {
      String type;
      if (ArduinoOTA.getCommand() == U_FLASH)
        type = "sketch";
      else // U_SPIFFS
        type = "filesystem";
      // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
      Serial.println("Start updating " + type);
    });
  ArduinoOTA.onEnd([]() {
      Serial.println("\nEnd");
    });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
      Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
    });
    .onError([](ota_error_t error) {
      Serial.printf("Error[%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
      else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
      else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
      else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
      else if (error == OTA_END_ERROR) Serial.println("End Failed");
    });
  ArduinoOTA.begin();
}

/*
 * ntp
 */
void get_ntp_time() {
  Serial.println("Fetching time via ntp...");
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  print_local_time();
}

void check_ntp_time() {
  if (now - ntp_last_check >= check_ntp_interval) {
    get_ntp_time();
    ntp_last_check = now;
    print_local_time();
  }
}
          
void print_local_time() {
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
  Serial.print("local time: ");
  Serial.println(&timeinfo, "%Y-%m-%d %H:%M:%S");
}

/*
 * buttons blinking in action
 */
void buttons_rotation() {
  for (int i = 0; i <= 4; i++) {
    set_buttons(1,0,0,0,1,0,0,0,1);
    delay(333);
    buttons_all_off();
    delay(50);
    set_buttons(0,1,0,0,0,1,1,0,0);
    delay(333);
    buttons_all_off();
    delay(50);
    set_buttons(0,0,1,1,0,0,0,1,0);
    delay(333);
    buttons_all_off();
    delay(50);
  }
  set_buttons(0,0,0,0,0,0,0,0,0);
}

void buttons_single_color() {
  for (int i = 0; i <= 4; i++) {
    buttons_all_red();
    delay(333);
    buttons_all_off();
    delay(100);
    buttons_all_green();
    delay(333);
    buttons_all_off();
    delay(100);
    buttons_all_blue();
    delay(333);
    buttons_all_off();
    delay(100);
  }
}

void buttons_all_red() {
  set_buttons(1,0,0,1,0,0,1,0,0);
}

void buttons_all_green() {
  set_buttons(0,1,0,0,1,0,0,1,0); 
}

void buttons_all_blue() {
  set_buttons(0,0,1,0,0,1,0,0,1);
}

void buttons_all_off() {
  set_buttons(0,0,0,0,0,0,0,0,0);
}

void buttons_all_on() {
  set_buttons(1,1,1,1,1,1,1,1,1);
}

void buttons_flash() {
  for (int i = 0; i <= 8; i++) {
    buttons_all_on();
    delay(150);
    buttons_all_off();
    delay(150);
  }
}

void mode_random() {
  game_mode = 'r';
  buttons_random_rgb();
}

void mode_freeze() {
  game_mode = 'f';
  for (int i = 0; i <= 5; i++) {
    buttons_random_rgb();
    delay(500);
  }
  buttons_random_rgb();
  /* TODO
  save_timestamp();
  read buttons press times
  submit via mqtt
  */
  game_mode = ' ';
}

void buttons_random_rgb() {
  set_buttons( random(1, 3), random(1, 3), random(1, 3),
    random(1, 3), random(1, 3), random(1, 3),
    random(1, 3), random(1, 3), random(1, 3)
  );
}

void set_buttons(int l1r, int l1g, int l1b, int l2r, int l2g, int l2b, int l3r, int l3g, int l3b){
    digitalWrite(led_1_r, l1r);
    digitalWrite(led_1_g, l1g);
    digitalWrite(led_1_b, l1b);
    digitalWrite(led_2_r, l2r);
    digitalWrite(led_2_g, l2g);
    digitalWrite(led_2_b, l2b);
    digitalWrite(led_3_r, l3r);
    digitalWrite(led_3_g, l3g);
    digitalWrite(led_3_b, l3b);
}
