#!/usr/bin/env python3
import paho.mqtt.client

class MQTT:
    def __init__(self, mqtt_broker, mqtt_port):
        # create client object and connect
        self.client = paho.mqtt.client.Client()
        self.client.connect(mqtt_broker, mqtt_port, 300)

    def publish(self, mqtt_channel, msg):
        self.client.publish(mqtt_channel, msg)

if __name__ == "__main__":
    print("MQTT...")
    mqtt_channel = "gamepad/dos"
    mq = MQTT("192.168.1.111", 1883)
    mq.publish(mqtt_channel, "foo")
