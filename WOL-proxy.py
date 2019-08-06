#!/usr/bin/python
import os
import re
import paho.mqtt.client as mqtt
from wakeonlan import send_magic_packet

# read in needed env variables
MQTT_BROKER_HOST   = os.getenv('MQTT_BROKER_HOST',"127.0.0.1")
MQTT_BROKER_PORT   = int(os.getenv('MQTT_BROKER_PORT',1883))
MQTT_CLIENT_ID     = os.getenv('MQTT_CLIENT_ID',"WOL-proxy")
MQTT_USERNAME      = os.getenv('MQTT_USERNAME',"")
MQTT_PASSWORD      = os.getenv('MQTT_PASSWORD',"")
MQTT_TOPIC_PREFIX  = os.getenv('MQTT_TOPIC_PREFIX',"WOL-proxy")
MQTT_QOS           = int(os.getenv('MQTT_QOS',1))
WOL_BROADCAST_ADDR = os.getenv('WOL_BROADCAST_ADDR',"255.255.255.255")
#print("All env vars read.")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected to broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT} with result code {rc}.")

    client.publish(MQTT_TOPIC_PREFIX+"/status",payload="Online",qos=1,retain=True)

    # subscribe to command topic
    client.subscribe(MQTT_TOPIC_PREFIX+"/command", MQTT_QOS)

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subcribed to commands on topic \"{MQTT_TOPIC_PREFIX}/command\" with QOS {granted_qos[0]}.")
    print(f"Wake-On-LAN proxy service started.")  

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection from broker (RC={rc}). Attempting to reconnect...")

# callback for when the client receives a message on the subscribed topic
def on_message(client, userdata, message):
    message.payload = message.payload.decode()
    print(f"Message received with payload {message.payload}")
    if re.match(r"[0-9a-f]{2}([-:\.]?)[0-9a-f]{2}(\1[0-9a-f]{2}){4}$", message.payload.lower()):
        send_magic_packet(message.payload,ip_address=WOL_BROADCAST_ADDR)
        print(f"Magic packet sent to {message.payload}.")
    else:
        print(f"Message payload has invalid mac address format!")

# set up mqtt client
client = mqtt.Client(client_id=MQTT_CLIENT_ID)
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    print("Username and password set.")
client.will_set(MQTT_TOPIC_PREFIX+"/status", payload="Offline", qos=1, retain=True)    
client.on_connect = on_connect # on connect callback
client.on_message = on_message # on message callback
client.on_disconnect = on_disconnect # on disconnect callback
client.on_subscribe = on_subscribe # on subscribe callback

# connect to broker
client.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT)

# start loop
client.loop_forever()
