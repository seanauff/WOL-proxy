# WOL-proxy

WOL-proxy is a dockerized Wake-On-LAN tool that received commands to send Wake-On-LAN magic packets over MQTT. This allows a computer to be woken on a network where a WOL packet would not normally reach (remote site, etc.)  

The script can be run using docker (takes care of all dependencies) or standalone. It is design to run on Raspberry Pi or equivalent.

## Usage

1. Have a MQTT broker you can connect to. I use [Mosquitto](https://hub.docker.com/_/eclipse-mosquitto).

2. Run the container or script using instructions below.

3. Publish to the mqtt topic, `WOL-proxy/command`, with the MAC address of the computer you wish to wake. The following formats are acceptable: `ab-cd-ef-01-23-45`, `ab:cd:ef:01:23:45`, `ab.cd.ef.01.23.45`, `abcdef012345`. An [example Home Assistant config](/hass-config-example.yaml) is provided.

   By default, WOL-proxy accepts messages on the `WOL-proxy/command` mqtt topic. The `WOL-proxy` prefix can be changed by setting the `MQTT_TOPIC_PREFIX` environment variable. WOL-proxy will then listen for messages on `[MQTT_TOPIC_PREFIX]/command`. Note that adding a trailing `/` to `MQTT_TOPIC_PREFIX` will create an empty level.

   |Value of MQTT_TOPIC_PREFIX|mqtt command topic|
   |--------------------------|-----------------|
   |`WOL-proxy`                |`WOL-proxy/command`|
   |`switches/remoteLAN`          |`switches/remoteLAN/command`|
   |`switches/remoteLAN/`         |`switches/remoteLAN//command`|

### Status Messages

WOL-proxy will report its status on the `[MQTT_TOPIC_PREFIX]/status` topic via retained messages. WOL-Proxy reports `Online` once it connects to the broker. Upon disconnect, the broker will report `Offline`.

## Running via Docker

Pull the image. The `latest` tag has multiarch support, so it should pull the correct image for your system.

```shell
docker pull ghcr.io/seanauff/wol-proxy
```

Start the container with all default environment variables:

```shell
docker run -d --net=host --name=WOL-proxy ghcr.io/seanauff/wol-proxy
```

Start the container with modified environment variables:

```shell
docker run -d --net=host --name=WOL-proxy -e MQTT_BROKER_HOST=<host> -e WOL_BROADCAST_ADDR=<broadcast> ghcr.io/seanauff/wol-proxy
```

*Note:* Container needs to run with host networking in order to send the broadcast packets correctly!

### Environment Variables

| Variable          | Default Value | Notes |
|-------------------|---------------|-------|
| MQTT_BROKER_HOST  |  127.0.0.1    |IP or hostname of MQTT broker       |
| MQTT_BROKER_PORT  |  1883         |Port of MQTT broker       |
| MQTT_CLIENT_ID    |  WOL-proxy  |Change this if the default is already in use by another client       |
| MQTT_USERNAME     |               |Username for connecting to MQTT broker when using auth. TLS not currently supported       |
| MQTT_PASSWORD     |               |Password for connecting to MQTT broker when using auth. TLS not currently supported       |
| MQTT_TOPIC_PREFIX | WOL-proxy   |The first level(s) of the topic for the proxy to subscribe ([prefix]/command) and provide status ([prefix]/status)      |
| MQTT_QOS          | 1             |[QOS](https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels/) level to use to subscribe to command topic       |
| WOL_BROADCAST_ADDR| 255.255.255.255         |Change to the local broadcast IP for best results    |

### Build the image yourself

Clone the repository and build the image:

```shell
git clone https://github.com/seanauff/WOL-proxy.git
docker build -t seanauff/wol-proxy WOL-proxy
```

## Other Install Methods

### Dependencies

This project uses the following libraries:

* [paho-mqtt](https://pypi.org/project/paho-mqtt/)
* [wakeonlan](https://pypi.org/project/wakeonlan/)

Install them with:

```shell
pip install paho-mqtt wakeonlan
```
