#!/bin/bash

# Check if a tag is provided
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "Usage: $0 <username> <password> <image tag>"
  exit 1
fi

# Assign the tag and image name to a variable
USER=$1
PASS=$2
TAG=$3
IMAGE_NAME="containers.repo.sciserver.org/ssec-snaptron/snapmine"

# Log in to Docker Hub
echo "-----------------------------------------------------------------------------------"
echo "    Logging in to Docker containers.repo.sciserver.org ..."
echo "-----------------------------------------------------------------------------------"

echo "docker login -u $USER -p $PASS containers.repo.sciserver.org"
docker login -u $USER -p $PASS containers.repo.sciserver.org

# Check if the login was successful
if [ $? -ne 0 ]; then
  echo "--------------------------  Docker login failed   -------------------------------"
  exit 1
fi

# Build the Docker image
echo "-----------------------------------------------------------------------------------"
echo "    Building Docker image with tag for linux/amd64: $TAG "
echo "-----------------------------------------------------------------------------------"
echo build --no-cache --platform=linux/amd64 -t $IMAGE_NAME:$TAG .
docker build --no-cache --platform=linux/amd64 -t $IMAGE_NAME:$TAG .

# Check if the build was successful
if [ $? -ne 0 ]; then
  echo "--------------------------  Docker build failed   -------------------------------"
  exit 1
fi

# Push the Docker image to the repository
echo "-----------------------------------------------------------------------------------"
echo "    Pushing Docker image to repository with tag: $TAG "
echo "-----------------------------------------------------------------------------------"
echo docker push $IMAGE_NAME:$TAG
docker push $IMAGE_NAME:$TAG

# Check if the push was successful
if [ $? -ne 0 ]; then
  echo "--------------------------  Docker push failed   -------------------------------"
  exit 1
fi

echo "-----------------------------------------------------------------------------------"
echo "    $IMAGE_NAME:$TAG built and pushed successfully"
echo "-----------------------------------------------------------------------------------"

