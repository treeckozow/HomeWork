#!/bin/bash

FILE_NAME=$1
WAITING_SECONDS=$2

if [ ! -e "$FILE_NAME" ]; then
    for sec in $(seq 1 $WAITING_SECONDS)
    do
        if [ -e "$FILE_NAME" ]; then
            echo "File $FILE_NAME arrived in server after $sec seconds"
            exit
        fi
        sleep 1
        if [ $sec -eq $WAITING_SECONDS ]; then
	    echo "Timeout"
        fi
    done
else
    echo "File $FILE_NAME exists"
fi
