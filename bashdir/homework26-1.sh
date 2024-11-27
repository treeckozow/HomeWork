#!/bin/bash


name="tahor"
password=54321

if [ $password -eq 54321 -a "$name" == "tahor" ]; then
    echo "access granted"
else
    echo "access denied"
fi



