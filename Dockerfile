FROM python:3-slim-buster

WORKDIR /usr/src/app

RUN pip install paho-mqtt wakeonlan

ADD WOL-proxy.py .

ENTRYPOINT ["python", "./WOL-proxy.py"]
