#!/usr/bin/python
import os
import re
import paho.mqtt.client as mqtt
from wakeonlan import send_magic_packet

# read in needed env variables
MQTT_BROKER_HOST   = os.environ['MQTT_BROKER_HOST']
MQTT_BROKER_PORT   = os.environ['MQTT_BROKER_PORT']
MQTT_CLIENT_ID     = os.environ['MQTT_CLIENT_ID']
MQTT_USERNAME      = os.environ['MQTT_USERNAME']
MQTT_PASSWORD      = os.environ['MQTT_PASSWORD']
MQTT_TOPIC_PREFIX  = os.environ['MQTT_TOPIC_PREFIX']
MQTT_QOS           = os.environ['MQTT_QOS']
WOL_BROADCAST_ADDR = os.environ['WOL_BROADCAST_ADDR']
#print("All env vars read.")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected to broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT} with result code {rc}.")

    client.publish(MQTT_TOPIC_PREFIX+"/status","Online")

    # subscribe to command topic
    client.subscribe(MQTT_TOPIC_PREFIX+"/command", qos=int(MQTT_QOS))

    print(f"Wake-On-LAN proxy service started.")    

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subcribed to commands on topic \"{MQTT_TOPIC_PREFIX}/command\" with QOS {granted_qos}.")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection from broker. Attempting to reconnect...")

# callback for when the client receives a message on the subscribed topic
def on_message(client, userdata, message):
    if re.match(r"[0-9a-f]{2}([-:\.]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", message.payload.lower()):
        send_magic_packet(message.payload,ip_address=WOL_BROADCAST_ADDR)
        print(f"Magic packet sent to {message.payload}.")
    else:
        print(f"Message recieved with invalid format: {message.payload}")

# set up mqtt client
client = mqtt.Client(client_id=MQTT_CLIENT_ID)
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    print("Username and password set.")
client.on_connect = on_connect # on connect callback
client.on_message = on_message # on message callback
client.on_disconnect = on_disconnect # on disconnect callback
client.on_subscribe = on_subscribe # on subscribe callback

# connect to broker
client.connect(MQTT_BROKER_HOST, port=int(MQTT_BROKER_PORT))

# start loop
client.loop_forever()
