cd  "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`

export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"

docker build -t ${LOCAL_IMAGE_NAME} ..

export PREDICTIONS_STREAM_NAME="nycmarch2023predictions"

docker-compose up

export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

