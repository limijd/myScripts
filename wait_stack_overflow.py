#!/usr/bin/env python
#-*-coding: utf-8 -*-
#pylint: disable=W0141

"""
wait_stack_overflow.py [OPTIONS] <size_kbytes>

DESCRITPION:
    monitor the process's stack map and quit immediately if stack overflows the trigger bound
    Useful to debug stack overflow testacses.

"""

import sys
import gflags
import subprocess
import time

if __name__ != "__main__":
    sys.exit(0)

#==============================================================================
# Option handling
#==============================================================================
GFLAGS = gflags.FlagValues()
gflags.DEFINE_boolean("help", False, "print help information", GFLAGS)
gflags.DEFINE_integer("interval", 3, "setup the sample interval to the process", flag_values=GFLAGS)
gflags.DEFINE_integer("pid", None, "the target process", flag_values=GFLAGS)
gflags.DEFINE_integer("trigger_bound", 1024, "in Kbytes, the triger bound of the stack overflow", flag_values=GFLAGS)


#option parsing
try:
    GARGV = GFLAGS(sys.argv)
except gflags.FlagsError, e:
    print '%s\n%s\nOPTIONS:\n%s' % (e, __doc__, GFLAGS.MainModuleHelp())
    sys.exit(1)

#option and argument check
if GFLAGS.help:
    print '%s\nOPTIONS:\n%s' % (__doc__, GFLAGS.MainModuleHelp())
    sys.exit(0)

print GFLAGS.pid
if not GFLAGS.pid:
    print '%s\nOPTIONS:\n%s' % (__doc__, GFLAGS.MainModuleHelp())
    sys.exit(1)
#==============================================================================
# program body
#==============================================================================

prev_kbytes = 0
cmd = "pmap %d" % GFLAGS.pid
while True:
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pin, pout, perr = p.stdin, p.stdout, p.stderr
        output = pout.readlines()
        status = pout.close()
        perr.close()
        pin.close()
        if(status):
            print "Can't execute command:" + command + "!\n"
            sys.exit(1)
        for l in output:
            parts = l.split()
            if "stack" in parts:
                kbytes = parts[1].strip("k")
                kbytes = int(kbytes.strip("K"))

                if kbytes!=prev_kbytes:
                    print "\nWaiting: current stack: %d Kbytes, target: %d Kbytes" % (kbytes, GFLAGS.trigger_bound)
                    prev_kbytes = kbytes
                else:
                    print ".",
                    sys.stdout.flush()

                if kbytes>=GFLAGS.trigger_bound:
                    print "Stack overflowed over %d, exit waiting" % GFLAGS.trigger_bound
                    sys.exit(0)
                break
            else:
                pass
        time.sleep(GFLAGS.interval)


