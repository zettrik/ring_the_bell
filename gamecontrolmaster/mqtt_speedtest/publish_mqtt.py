#!/usr/bin/env python3
import time, json, sensors
import paho.mqtt.client as mqtt

delay = 10 # wait for X seconds till next mqtt send
mqtt_broker = "192.168.1.111"
mqtt_port = 1883
mqtt_channel = "test/foo"
mqtt_keepalive = 300; # seconds

# publish callback function
def on_publish(client, userdata, result):
   #print("data published")
   pass

# create client object and connect
client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, mqtt_keepalive)

# assign publish callback function
client.on_publish = on_publish

# publish messages
while True:
   dict_msg = time.time()
   msg = json.dumps(dict_msg)
   ret = client.publish(mqtt_channel, msg)
   print(msg)
   time.sleep(delay)
