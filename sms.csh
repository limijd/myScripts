#!/bin/tcsh

set me = $1
set buddy = $2


if ( $# != 3 ) then
    echo $*
    echo "Usage: sms <me> <buddy> <msg>"
    exit 1
endif

echo "echo $3 | sendxmpp -t -u $1 -o gmail.com $2"
echo $3 | sendxmpp -t -u $1 -o gmail.com $2
