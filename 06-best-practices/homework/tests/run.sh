#!/usr/bin/env bash
cd  "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`

export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"

docker build -t ${LOCAL_IMAGE_NAME} ..

export PREDICTIONS_STREAM_NAME="nycmarch2023predictions"

docker-compose up s3 -d # releases the terminal if you use -d

sleep 5

export S3_ENDPOINT_URL="http://localhost:4566" # just in case

export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration

pipenv run python integration_test.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down