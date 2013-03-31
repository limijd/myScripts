#!/bin/csh

ps -A |grep dib.py >& /dev/null

if $? then
    echo "nohup /home/limijd/local.install/github.proj.DIB/dib.py &"
    nohup stdbuf -o 0 /home/limijd/local.install/github.proj.DIB/dib.py |& tee /tmp/dib.log &
else
    exit 0
endif
