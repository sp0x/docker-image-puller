Docker-Compose image puller and deployment trigger
===================

[![](https://images.microbadger.com/badges/version/sp0x/docker-image-puller.svg)](https://hub.docker.com/r/sp0x/docker-image-puller/)
![](https://images.microbadger.com/badges/image/sp0x/docker-image-puller.svg)

## Overview

If you work with docker and continuous integrations tools, you might need to update your images on your servers as soon as your build is finished.  
Or you might need to trigger a build on a platform like Travis-Ci, CircleCi, from a webhook using a third party platform.   
This tool is a tiny webserver listening for webhooks.  
It:
 - Updates the specified image using [Docker-Compose](https://docs.docker.com/compose/).
 - Triggers a build on your CI platform


You just have to run the image on your server, and configure your CI tool or content platform.

## Installation

Launch the image on your server, where the images you want to update are
```
docker run -d \
  --name dip \
  --env TOKEN=abcd4242 \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  tuxity/docker-image-puller
```

Available env variable:
```
TOKEN* - The token that's used for authentication
REGISTRY_URL (default: https://index.docker.io/v1/)
TRAVIS_TOKEN - The token you get from `travis token --com`, if you're using Travis-Ci for build triggers.
HOST (default: 0.0.0.0)
PORT (default: 8080)
DEBUG (default: False)
```

\* mandatory variables. For `TOKEN` You can generate a random string, it's a security measure.

After, you just have to make a request to the server:
```
curl -X POST http://ipofyourserver/images/pull?token=abcd4242&restart_containers=true&image=nginx:latest
```

## Logs

You can access container logs with
```
docker logs --follow dip
````
