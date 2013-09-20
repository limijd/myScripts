#!/bin/sh


while [ $0 ]; do 
    eval "$*"
    RTN=$?
    if [ $RTN = 0 ]; then
        break
    else
        echo $RTN
        sleep 20
    fi
done
