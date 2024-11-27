#!/bin/bash

file_path="/var/log/syslog"

if [ -e "$file_path" ]; then
    echo "exists"
else
    echo "doesn't exist"
fi

dir_path="/ome/ubuntu"

if [ -e "$dir_path" ]; then
    echo "exists"
else
    echo "doesn't exist"
fi
