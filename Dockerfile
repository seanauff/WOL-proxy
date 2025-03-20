FROM python:3-slim-buster

LABEL org.opencontainers.image.source=https://github.com/seanauff/WOL-proxy
LABEL org.opencontainers.image.description="WOL-proxy is a dockerized Wake-On-LAN tool that received commands to send Wake-On-LAN magic packets over MQTT. "
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /usr/src/app

RUN pip install paho-mqtt wakeonlan

ADD WOL-proxy.py .

ENTRYPOINT ["python", "-u", "./WOL-proxy.py"]
