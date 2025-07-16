#!/bin/bash
set -e

./install.sh

CONTAINER_ID=$(docker ps -aqf name=fastapi-jwt-app)
if [ ! -z "$CONTAINER_ID" ]; then
    echo "Stopping old docker container..."
    docker stop $CONTAINER_ID || true
    docker rm $CONTAINER_ID || true
fi

echo "Starting FastAPI JWT container on port 8000..."
docker run -d --name fastapi-jwt-app -p 8000:8000 fastapi-jwt-app
sleep 2
echo "Container started. App is accessible at http://localhost:8000/"
