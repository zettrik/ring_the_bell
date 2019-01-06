#include "WiFi.h"
#include "AsyncUDP.h"

#include <time.h>
#include <esp_wifi.h>

/* gamepad */
const char *my_name = "uno";
const int gamepad_version = 1;

/* wifi */
const char *ssid = "***";
const char *password = "***";
IPAddress local_ip(127, 0, 0, 0); // will be set via dhcp
WiFiClient espClient;
unsigned long wifi_connects = 0;

/* udp */
IPAddress server_ip(172, 16, 2, 232);
const int server_port = 3333;
const unsigned long send_interval = 1000000; // 1s
AsyncUDP udp;
uint8_t *incoming = 0;
char msg[15];

/* I/O */
const byte led0 = 5; // on board LED
const byte led_1_r = 32; // red LED on first button
const byte led_1_g = 33;
const byte led_1_b = 25;
const byte led_2_r = 26;
const byte led_2_g = 27;
const byte led_2_b = 14;
const byte led_3_r = 12;
const byte led_3_g = 13;
const byte led_3_b = 15;
const byte button1 = 36; // first input button
const byte button2 = 39;
const byte button3 = 34;
byte button1_state = 0;
byte button2_state = 0;
byte button3_state = 0;
byte button1_pressed = 0;
byte button2_pressed = 0;
byte button3_pressed = 0;
unsigned long button1_presstime = 0;
unsigned long button2_presstime = 0;
unsigned long button3_presstime = 0;

/* ntp */
//const char *ntpServer = "1.debian.pool.ntp.org";
const char *ntpServer = "172.16.2.232";
const unsigned long check_ntp_interval = 36000000;
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;
unsigned long now = 0;
unsigned long before = 0;
unsigned long rtc_now;
unsigned long time_delta;
unsigned long ntp_last_check;
time_t unixseconds;

void setup() {
    Serial.begin(115200);
    Serial.println("===");
    Serial.print("my name is: ");
    Serial.println(my_name);
    Serial.print("version: ");
    Serial.println(gamepad_version);
    Serial.println("---");
    pinMode(led0, OUTPUT);
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
    
    setup_wifi();
    setup_udp_listener();
    udp.broadcastTo("Hello my name is Uno running v1!", server_port);
    get_ntp_time();
}

void loop() {
  digitalWrite(led0, 0);
  now = system_get_time();
  read_buttons();
  if ((before + send_interval) <= now) {
    send_states();
    before = now;
  }
  //test_reaction();
}

/*
 * test reaction time
 */
void test_reaction() {
  Serial.println("testing reaction time");
  delay(5700);
  digitalWrite(led_1_r, 1);
  button1_presstime = now - before;
  sprintf(msg,"%16lu", button1_presstime);
  udp.broadcastTo(msg, server_port);
  digitalWrite(led_1_r, 0);
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
 * send button states via udp
 */
void send_states() {      
  digitalWrite(led_1_r, 1);
  sprintf(msg,"%16lu", button1_presstime);
  udp.broadcastTo(msg, server_port);

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
        
  button1_pressed = 0;
  button2_pressed = 0;
  button3_pressed = 0;
  button1_presstime = 0;
  button2_presstime = 0;
  button3_presstime = 0;
  digitalWrite(led_1_r, 0);
}

/*
 * udp
 */
void setup_udp_listener() {
  if(udp.listen(server_port)) {
        Serial.print("UDP Listening on: ");
        Serial.print(WiFi.localIP());
        Serial.print(":");
        Serial.println(server_port);
        udp.onPacket([](AsyncUDPPacket packet) {
            Serial.print("UDP Packet Type: ");
            Serial.print(packet.isBroadcast()?"Broadcast":packet.isMulticast()?"Multicast":"Unicast");
            Serial.print(", From: ");
            Serial.print(packet.remoteIP());
            Serial.print(":");
            Serial.print(packet.remotePort());
            Serial.print(", To: ");
            Serial.print(packet.localIP());
            Serial.print(":");
            Serial.print(packet.localPort());
            Serial.print(", Length: ");
            Serial.print(packet.length());
            Serial.print(", Data: ");
            Serial.write(packet.data(), packet.length());
            Serial.println();
            incoming = packet.data();
            /*TODO fix comparison
            if (incoming == 2) {
              Serial.println("---------FREEZE-----------");
              //get in freeze mode
            }
            incoming = 0;
            */
        });
    }
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

