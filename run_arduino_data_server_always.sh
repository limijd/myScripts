#!/bin/csh

ps -A |grep arduino_app_ >& /dev/null

if $? then
    echo "nohup sudo /home/limijd/local.install/github.scripts/arduino/arduino_app_layer.py --port=21599 --serial_port=/dev/ttyACM0 >& /dev/null"
    nohup  sudo /home/limijd/local.install/github.scripts/arduino/arduino_app_layer.py --port=21599 --serial_port=/dev/ttyACM0 >& /dev/null &
else
    exit 0
endif
