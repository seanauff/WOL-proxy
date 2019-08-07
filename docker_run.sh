#!/bin/sh

# basic run command, uses all default env vars
docker run -d --net=host seanauff/wol-proxy

# command to set env vars to custom values
# docker run -d --net=host -e 