#!/bin/bash

app_name=$1
tag=${2:-latest}

if [ -z $app_name ]; then
    echo 'Usage: .scripts/build <app_name> <tag>'
    exit 1
fi

echo Building ${app_name}:${tag}
echo

cd $app_name

docker build -t yomain/${app_name}:${tag} .

cd ..
