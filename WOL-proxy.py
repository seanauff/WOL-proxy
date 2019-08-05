#!/usr/bin/python
import os
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# read in needed env variables
MQTT_BROKER_HOST  = os.environ['MQTT_BROKER_HOST']
MQTT_BROKER_PORT  = os.environ['MQTT_BROKER_PORT']
MQTT_CLIENT_ID    = os.environ['MQTT_CLIENT_ID']
MQTT_USERNAME     = os.environ['MQTT_USERNAME']
MQTT_PASSWORD     = os.environ['MQTT_PASSWORD']
MQTT_TOPIC_PREFIX = os.environ['MQTT_TOPIC_PREFIX']

