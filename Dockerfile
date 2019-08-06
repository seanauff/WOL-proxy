FROM python:3

WORKDIR /usr/src/app

RUN pip install paho-mqtt wakeonlan

ADD WOL-proxy.py .

ENV MQTT_BROKER_HOST=127.0.0.1
ENV MQTT_BROKER_PORT=1883
ENV MQTT_CLIENT_ID=WOL-proxy
ENV MQTT_USERNAME=
ENV MQTT_PASSWORD=
ENV MQTT_TOPIC_PREFIX=WOL-proxy
ENV MQTT_QOS=1
ENV WOL_BROADCAST_ADDR=255.255.255.255

ENTRYPOINT ["python", "./WOL-proxy.py"]
