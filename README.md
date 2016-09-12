Docker Image Puller
===================

[![Docker Automated buil](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?maxAge=2592000)](https://hub.docker.com/r/tuxity/docker-image-puller/)
[![DUB](https://img.shields.io/dub/l/vibe-d.svg?maxAge=2592000)](https://github.com/Tuxity/docker-image-puller/blob/master/LICENSE)

## Overview

If you work with docker and continuous integrations tools, you might need to update your images on your servers as soos as your build is finish.

This tool is a tiny webserver listening for a `POST` and automatically update the specified image using [Docker](https://docs.docker.com/engine/reference/api/docker_remote_api/) API.

You just have to run the image on your server, and configure your CI tool.

CI tools to make the POST request:
- [Drone](http://readme.drone.io/plugins/webhook/)


## Installation

Launch the image on your server, where the images you want to update are
```
docker run -d \
  --name dip \
  --env TOKEN=abcd4242 \
  -p 8080:8080
  -v /var/run/docker.sock:/var/run/docker.sock \
  tuxity/docker-image-puller
```

Available env variable:
```
TOKEN
HOST (default: 0.0.0.0)
PORT (default: 8080)
DEBUG (default: False)
```

`TOKEN` is a mandatory variable, without it it won't work. You can generate a random string, it's a security measure.

After, you just have to make a request to the server:
```
POST http://ipofyourserver/images/pull?token=abcd4242&image=nginx:latest
```

## Logs

You can access container logs with
```
docker logs --follow dip
````