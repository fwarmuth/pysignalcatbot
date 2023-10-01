#!/bin/sh
name="signal-api"
docker stop $name
docker rm $name
docker run -d --name $name --restart=always -p 127.0.0.1:18080:8080 \
      -v ./local_data/signal-cli-rest-api/signal-cli:/home/.local/share/signal-cli \
      -e 'MODE=normal' bbernhard/signal-cli-rest-api