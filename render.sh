#!/bin/bash
# Render README.md using Docker
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build image if it doesn't exist
if ! docker image inspect d0ugal-readme-renderer:latest &>/dev/null; then
  echo "Building Docker image..."
  docker build -t d0ugal-readme-renderer "${SCRIPT_DIR}"
fi

docker run --rm \
  -v "${SCRIPT_DIR}:/workspace" \
  -w /workspace \
  d0ugal-readme-renderer

