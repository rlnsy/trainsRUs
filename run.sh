#!/bin/bash

set -e

STACK_UP="stack-up"
STACK_DOWN="stack-down"
BACKEND_UP="backend-up"
BACKEND_DOWN="backend-down"
FRONTEND_DEBUG="frontend"

print_usage() {
  echo "USAGE: ./run.sh [ $STACK_UP | $STACK_DOWN | | $BACKEND_UP | $BACKEND_DOWN | $FRONTEND_DEBUG ]"
  echo "$STACK_UP: Run full stack container"
  echo "$STACK_DOWN: Tear down full stack container"
  echo "$BACKEND_UP: Run backend stack with tests"
  echo "$BACKEND_DOWN: Tear down backend stack container"
  echo "$FRONTEND_DEBUG: Run frontend in development environment"
}

check_docker() {
  docker --version > /dev/null
  STATUS=$?
  if [[ $STATUS != 0 ]]; then
    echo "You need to install docker CLI!"
    exit 1
  fi
}

DESIRED_PROTOCOL=$1

if [[ $DESIRED_PROTOCOL == $STACK_UP ]]; then
  check_docker
  docker-compose -f config/full-stack.yml up --build --force-recreate
  echo "Remember to tear down the stack!"
  exit 0
elif [[ $DESIRED_PROTOCOL == $STACK_DOWN ]]; then
  check_docker
  docker-compose -f config/full-stack.yml down
  exit 0
elif [[ $DESIRED_PROTOCOL == $BACKEND_UP ]]; then
  check_docker
  docker-compose -f config/dev-backend.yml up --build --force-recreate
  echo "Remember to tear down the stack!"
  exit 0
elif [[ $DESIRED_PROTOCOL == $BACKEND_DOWN ]]; then
  check_docker
  docker-compose -f config/dev-backend.yml down
  exit 0
elif [[ $DESIRED_PROTOCOL == $FRONTEND_DEBUG ]]; then
  cd web
  yarn install
  yarn serve
else
  print_usage
  exit 0
fi
