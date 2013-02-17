#!/bin/csh

set SITE=google.com
ping -c 5 -W 1 ${SITE}|& grep 'min/avg/max/mdev' >/dev/null

exit $?
