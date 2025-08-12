# Stop at first error
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DOCKER_TAG="example-algorithm-segrap2025-task2" # change this as needed
DOCKER_NOOP_VOLUME="${DOCKER_TAG}-volume"

INPUT_DIR="${SCRIPT_DIR}/test/input"
OUTPUT_DIR="${SCRIPT_DIR}/test/output"
MEM_LIMIT="64g"

echo "+++++ Cleaning up the output folder +++++"
if [ -d "$OUTPUT_DIR" ]; then
  # Ensure permissions are setup correctly
  # This allows for the Docker user to write to this location
  rm -rf "${OUTPUT_DIR}"/*
  chmod -f o+rwx "$OUTPUT_DIR"
else
  mkdir -p "$OUTPUT_DIR" # for mac
  chmod o+rwx "$OUTPUT_DIR" # for mac
fi

echo "+++++ (Re)build the container +++++"
docker build "$SCRIPT_DIR" \
  --platform=linux/amd64 \
  --tag $DOCKER_TAG 2>&1

echo "+++++ Doing a forward pass +++++"
USE_GPUS="--gpus all"  # Uncomment this line to enable GPU support
docker volume create "$DOCKER_NOOP_VOLUME"
docker run --rm \
    --memory="${MEM_LIMIT}" \
    --memory-swap="${MEM_LIMIT}" \
    --platform=linux/amd64 \
    --network none \
    $USE_GPUS \
    --volume "$INPUT_DIR":/input \
    --volume "$OUTPUT_DIR":/output \
    --volume "$DOCKER_NOOP_VOLUME":/tmp \
    $DOCKER_TAG
docker volume rm "$DOCKER_NOOP_VOLUME"

# Adjust permissions directly on the host if needed, may require you to enter password
HOST_UID=$(id -u)
HOST_GID=$(id -g)
sudo chown -R $HOST_UID:$HOST_GID "$OUTPUT_DIR"

echo "+++++ Wrote results to ${OUTPUT_DIR} +++++"