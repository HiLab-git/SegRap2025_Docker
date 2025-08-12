# Stop at first error
set -e

DOCKER_TAG="example-algorithm-segrap2025-task1" # change this as needed

echo "+++++ Exporting the Docker image to a tar.gz file +++++"
docker save $DOCKER_TAG | gzip -c > ${DOCKER_TAG}.tar.gz

echo "+++++ Docker image exported successfully to ${DOCKER_TAG}.tar.gz +++++"