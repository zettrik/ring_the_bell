#include "WiFi.h"
#include "AsyncUDP.h"

#include <time.h>
#include <esp_wifi.h>

/* wifi */
const char* my_name = "uno";
const char* ssid = "***";
const char* password = "***";
IPAddress local_ip(127, 0, 0, 0); // will be set via dhcp
WiFiClient espClient;
unsigned long wifi_connects = 0;

/* udp */
IPAddress server_ip(172, 16, 2, 232);
const int server_port = 3333;
const int led1 = 5; // on board LED
AsyncUDP udp;

/* ntp */
const char* ntpServer = "1.debian.pool.ntp.org";
const unsigned long check_ntp_interval = 36000000;
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;
unsigned long now = 0;
unsigned long before = 0;
unsigned long rtc_now;
unsigned long time_delta;
unsigned long ntp_last_check;

void setup() {
    Serial.begin(115200);
    Serial.println("===");
    Serial.println(my_name);
    Serial.println("---");
    pinMode(led1, OUTPUT);
    
    setup_wifi();
    setup_udp_listener;
    udp.broadcastTo("Hello my name is Uno!", server_port);
    get_ntp_time();
}

void loop() {
    delay(1000);
    udp.broadcastTo(my_name, server_port);
    Serial.println("udp");
    digitalWrite(led1, 0);
    delay(1000);
    digitalWrite(led1, 1);
    delay(1000);
}

/*
 * udp
 */
void setup_udp_listener() {
    if(udp.connect(server_ip, server_port)) {
        Serial.println("UDP connected");
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
            //reply to the client
            packet.printf("Got %u bytes of data", packet.length());
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
    digitalWrite(led1, 0);
    delay(250);
    digitalWrite(led1, 1);
    delay(125);
    digitalWrite(led1, 0);
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
  Serial.print(system_get_time());
  Serial.print(", ");
  Serial.println(&timeinfo, "%Y-%m-%d %H:%M:%S");
}

