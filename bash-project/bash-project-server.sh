#!/bin/bash

FILE_NAME=$1
WAITING_SECONDS=$2


for sec in $(seq 1 $WAITING_SECONDS)
do
    if [ -e "$FILE_NAME" ]; then
        echo "File $FILE_NAME arrived in server after $sec seconds"
        exit
    fi
    sleep 1
done

echo "Timeout"
