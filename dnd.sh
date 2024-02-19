#!/bin/sh

DOCKERFILE_TEST=dockerfiles/Dockerfile.Test
DOCKER_IMAGE_NAME=dnd_test:latest

if [ -z "$1" ]; then
    echo "Must provide a command name"
    exit 1
fi
if [ "$1" = "run" ]; then
    docker compose up --build
elif [ "$1" = "test" ]; then
    shift
    docker build -f $DOCKERFILE_TEST -t $DOCKER_IMAGE_NAME .
    docker run -v ${PWD}:/src $DOCKER_IMAGE_NAME dotnet test "$@"
elif [ "$1" = "format" ]; then
    shift
    docker build -f $DOCKERFILE_TEST -t $DOCKER_IMAGE_NAME .
    docker run -v ${PWD}:/src $DOCKER_IMAGE_NAME dotnet format /src/ShopGen.sln "$@"
else 
    docker build -f $DOCKERFILE_TEST -t $DOCKER_IMAGE_NAME .
    docker run -v ${PWD}:/src $DOCKER_IMAGE_NAME dotnet "$@"
fi