#!/bin/bash

FILE=$1
BUCKET=$2
TIME=$3

aws s3 cp "$FILE" "s3://$BUCKET/" || { echo "Upload failed"; exit 1; }
aws s3 presign "s3://$BUCKET/$(basename "$FILE")" --expires-in "$TIME"
