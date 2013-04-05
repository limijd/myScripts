#!/bin/csh

/usr/bin/sensors k10temp-pci-00c3 | grep temp1 | sed 's/ \+/ /g' | cut -d ' ' -f 2 | sed 's/°C//' |& tee -a ~/log/cpu_temp_log.txt >& /dev/null
