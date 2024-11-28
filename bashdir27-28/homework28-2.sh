#!/bin/bash

while [ -e "run.txt" ]
do
    echo "file exists"
    sleep 3
done

echo "file deleted"
