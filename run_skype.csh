#!/bin/csh
#fix skype borken sound issue.
setenv PULSE_LATENCY_MSEC 50

nohup /usr/bin/skype &
