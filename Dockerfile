FROM python:3

WORKDIR /usr/src/app

RUN pip install paho-mqtt wakeonlan

ADD WOL-proxy.py .

ENV MQTT_BROKER_HOST   = 127.0.0.1 \
    MQTT_BROKER_PORT   = 1883 \
    MQTT_CLIENT_ID     = "WOL-proxy" \
    MQTT_USERNAME      = "" \
    MQTT_PASSWORD      = "" \
    MQTT_TOPIC_PREFIX  = "WOL-proxy" \
    WOL_BROADCAST_ADDR = "255.255.255.255"

ENTRYPOINT ["python", "./WOL-proxy.py"]