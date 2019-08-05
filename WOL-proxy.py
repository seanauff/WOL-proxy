#!/usr/bin/python
import os
import paho.mqtt.client as mqtt
from wakeonlan import send_magic_packet

# read in needed env variables
MQTT_BROKER_HOST  = os.environ['MQTT_BROKER_HOST']
MQTT_BROKER_PORT  = os.environ['MQTT_BROKER_PORT']
MQTT_CLIENT_ID    = os.environ['MQTT_CLIENT_ID']
MQTT_USERNAME     = os.environ['MQTT_USERNAME']
MQTT_PASSWORD     = os.environ['MQTT_PASSWORD']
MQTT_TOPIC_PREFIX = os.environ['MQTT_TOPIC_PREFIX']

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# set up mqtt client
client = mqtt.Client(client_id=MQTT_CLIENT_ID)
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
client.on_connect = on_connect # on connect callback
client.on_message = on_message # on message callback

# connect to broker
client.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT)
client.loop_start()
client.publish(MQTT_TOPIC_PREFIX+"/status","Online")

# subscribe to command topic
client.subscribe(MQTT_TOPIC_PREFIX+"/command")

# callback for when the client receives a message on the subcribed topic
def on_message(client, userdata, message):
    