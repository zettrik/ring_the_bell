#!/usr/bin/env python3
import os, re, sys, urllib, time
import paho.mqtt.client as mqtt

## mqtt config
mqtt_broker = "192.168.1.111"
mqtt_port = 1883
mqtt_topic = "test/foo"
mqtt_keepalive = 300; # seconds


def on_connect(mqttc, userdata, flags, result_code):
    print("listening on topic: %s" % mqtt_topic)
    #print("connected to broker with result code = " + str(result_code))
    mqttc.subscribe(topic=mqtt_topic, qos=0)

def on_disconnect(mqttc, userdata, result_code):
    #print("disconnected from broker with result_code = " + str(result_code))
    return()

def on_message(mqttc, userdata, msg):
    unixtime = time.time()
    mqtt_msg = msg.payload
    triptime = unixtime - float(mqtt_msg)
    #print('message received...')
    #print('topic: %s' % str(msg.topic))
    #print('msg: %s' % str(mqtt_msg))
    #print('time: %s' % unixtime)
    print("mqtt roundtrip time: %s" % triptime)
    #mcp_value = msg.payload.decode('UTF-8')
    #print('utf-8')
    #print(mcp_value)
    #ad = mcp_value.split(",")


def on_subscribe(mqttc, userdata, mid, granted_qos):
    #print('subscribed to channel (qos=' + str(granted_qos) + ')')
    return()

def on_unsubscribe(mqttc, userdata, mid, granted_qos):
    #print('unsubscribed from channel (qos=' + str(granted_qos) + ')')
    return()

if __name__ == '__main__':
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_unsubscribe = on_unsubscribe
    # connect to mqtt broker
    try:
        print("connecting to mqtt broker: %s:%s" % (mqtt_broker, mqtt_port))
        mqttc.connect(mqtt_broker, mqtt_port, mqtt_keepalive)
    except ConnectionRefusedError:
        sys.exit(1)

    # start mqtt listening process
    mqttc.loop_forever()
