#!/bin/bash

docker build . -t checker:matteyeux
docker run -d -p 5000:5000 -it checker:matteyeux
