#!/usr/bin/python2
#-*-coding: utf-8 -*-
#pylint: disable=W0141, W0401, W0614

import sys

if __name__ != "__main__":
    sys.exit(0)
#==============================================================================
# Option handling
#==============================================================================
import gflags
GFLAGS = gflags.FlagValues()
gflags.DEFINE_boolean("help", False, "print help information", GFLAGS)
gflags.DEFINE_boolean("debug", False, "print debug information", GFLAGS)
gflags.DEFINE_boolean("verbose", False, "print verbose information", GFLAGS)
gflags.DEFINE_integer("num", 0, "range number", flag_values=GFLAGS)
gflags.DEFINE_integer("dig", 2, "digits", flag_values=GFLAGS)

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

#==============================================================================
# program body
#==============================================================================

for i in range(GFLAGS.num):
    fs = '%%0%dd' % GFLAGS.dig
    print fs%i
