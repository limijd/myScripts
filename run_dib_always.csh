#!/bin/csh

ps -A |grep dib.py >& /dev/null

if $? then
    echo "nohup /home/limijd/local.install/github.proj.DIB/dib.py &"
    nohup /home/limijd/local.install/github.proj.DIB/dib.py &
else
    exit 0
endif
