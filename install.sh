#!/bin/bash
set -e

if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Building Docker image..."
docker build -t fastapi-jwt-app .

echo "Docker image built successfully. To start the server, use the run.sh script."
