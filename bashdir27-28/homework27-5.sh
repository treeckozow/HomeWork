#!/bin/bash

names="server client service microservice"

for name in $names
do 
    touch "$name.sh"
done

for name in $names
do
    rm -f "$name.sh"
done

