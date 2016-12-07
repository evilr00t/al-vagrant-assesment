#!/usr/bin/env bash

curl -s $1 2>&1 | grep $2 > /dev/null
if [ $? -eq 0 ]; then
  echo "Found $2 in the content"
else
  echo "Content $2 not found"
  exit 1
fi
