#!/bin/bash
docker rm chocobo

docker run --name chocobo -p 8000:8000 $1
