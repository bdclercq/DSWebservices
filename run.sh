#!/usr/bin/env bash

#docker-compose -f docker-compose.yml build --no-cache
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
