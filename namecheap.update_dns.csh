#!/bin/csh

#need to provide dynamic dns password
wget 'https://dynamicdns.park-your-domain.com/update?host=@&domain=limijd.me&password=$1' -o /dev/null

