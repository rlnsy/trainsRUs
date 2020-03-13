#!/bin/bash

set -e

CONTAINER_UP="stack-up"
CONTAINER_DOWN="stack-down"

print_usage() {
  echo "USAGE: cdkrunner [ $CONTAINER_UP | $CONTAINER_DOWN ]"
  echo "$CONTAINER_UP: Set up stack and run application"
  echo "$CONTAINER_DOWN: Tear down stack and container"
}

DESIRED_PROTOCOL=$1

if [[ $DESIRED_PROTOCOL == $CONTAINER_UP ]]; then
    echo "Setting up stack..."
    docker --version > /dev/null
    STATUS=$?
    if [[ $STATUS != 0 ]]; then
      echo "You need to install docker CLI!"
      exit 1
    fi
    docker-compose up --build --force-recreate
elif [[ $DESIRED_PROTOCOL == $CONTAINER_DOWN ]]; then
    echo "Tearing down stack..."
    docker-compose down
else
    print_usage
fi

exit 0
