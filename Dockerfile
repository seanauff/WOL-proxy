FROM lsiobase/alpine:3.19

ENV \
    PATH="/pyvenv/bin:${PATH}"

RUN apk add python3 && \
    python3 -m venv /pyvenv && \
    pip3 install paho-mqtt wakeonlan

COPY root /
COPY WOL-proxy.py /app
