#!/bin/sh
set -eu

IMAGE="${GRAPHALIZER_TEST_IMAGE:-nicklinney/graphalizer-test:0.0.0-dev}"

docker build --target test --tag "$IMAGE" .
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev,size=2g \
  --shm-size 2g \
  --memory 12g \
  --memory-swap 12g \
  --cpus 8 \
  --pids-limit 256 \
  "$IMAGE"
