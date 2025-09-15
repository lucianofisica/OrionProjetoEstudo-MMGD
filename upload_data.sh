#!/bin/bash
set -e

# This script uploads a given file to the MinIO landing-zone bucket.
#
# Usage:
#   ./upload_data.sh <path/to/your/datafile.csv>
#
# Example:
#   ./upload_data.sh ../Downloads/dados-aneel.csv
#
# Before running, make sure you have:
# 1. Docker running with the services from docker-compose.yml.
# 2. The MinIO client (mc) installed, or run this via a Docker container.
# 3. A .env file with MINIO_ROOT_USER and MINIO_ROOT_PASSWORD.

if [ -z "$1" ]; then
  echo "Error: Please provide the path to the data file as the first argument."
  echo "Usage: $0 <path/to/datafile.csv>"
  exit 1
fi

DATA_FILE=$1
# Extract the filename from the path
FILENAME=$(basename "$DATA_FILE")
BUCKET="landing-zone"

# Load environment variables from .env file
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

if [ -z "$MINIO_ROOT_USER" ] || [ -z "$MINIO_ROOT_PASSWORD" ]; then
  echo "Error: MINIO_ROOT_USER and MINIO_ROOT_PASSWORD must be set in your .env file."
  exit 1
fi

echo "Waiting for MinIO to start..."
sleep 5

echo "Configuring MinIO client (mc)..."
mc alias set minio http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

echo "Creating bucket '$BUCKET' if it doesn't exist..."
mc mb minio/${BUCKET} --ignore-existing

echo "Uploading '$FILENAME' to bucket '$BUCKET'..."
mc cp "$DATA_FILE" "minio/${BUCKET}/${FILENAME}"

echo "Upload of '$FILENAME' complete!"
echo "You can view the file at http://localhost:9001/browser/${BUCKET}/"