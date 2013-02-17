#!/bin/csh

if $USER != "root" then
    exit 1
endif

/home/limijd/dev-sandbox/github.scripts/check_internet_up.csh

if $? then
    echo "internet is bad, need reboot" | mail -s "limijd-mint-c60 is going to reboot" limijd@gmail.com
endif
