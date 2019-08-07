# WOL-proxy

WOL-proxy is a dockerized Wake-On-LAN tool that received commands to send Wake-On-LAN magic packets over MQTT. This allows a computer to be woken on a network where a WOL packet would not normally reach (remote site, etc.)  

The script can be run using docker (takes care of all dependencies) or standalone. It is design to run on Raspberry Pi or equivalent.

## Running via Docker

Pull the image using either `amd64` or `arm` in place of `[tag]`:

```shell
docker pull seanauff/wol-proxy:[tag]
```

Start the container with all default environment variables:

```shell
docker run -d --net=host seanauff/wol-proxy:[tag]
```

Start the container with modified environment variables:

```shell
docker run -d --net=host -e MQTT_BROKER_HOST=[host] -e WOL_BROADCAST_ADDR=[broadcast] seanauff/wol-proxy:[tag]
```

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
