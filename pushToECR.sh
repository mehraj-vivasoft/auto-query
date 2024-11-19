#!/bin/bash

docker-compose build

AWS_REGION="ap-southeast-1"
AWS_ACCOUNT_ID="715841331407"

DOCKER_IMAGE_FASTAPI="auto-query-fastapi"
DOCKER_IMAGE_MAKE_DATASET="auto-query-make-dataset"
DOCKER_IMAGE_HUDURI="auto-query-huduri"

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker tag $DOCKER_IMAGE_FASTAPI:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/mehraj-$DOCKER_IMAGE_FASTAPI:latest
docker tag $DOCKER_IMAGE_MAKE_DATASET:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/mehraj-$DOCKER_IMAGE_MAKE_DATASET:latest
docker tag $DOCKER_IMAGE_HUDURI:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/mehraj-$DOCKER_IMAGE_HUDURI:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/mehraj-$DOCKER_IMAGE_FASTAPI:latest &
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/mehraj-$DOCKER_IMAGE_MAKE_DATASET:latest &
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/mehraj-$DOCKER_IMAGE_HUDURI:latest &

wait