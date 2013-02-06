#!/usr/bin/python

import os
import sys
import string
import getopt
import time


if __name__ != "__main__":
    sys.exit(0);


opts, args  = getopt.getopt(sys.argv[1:], "h", ["help"])
for o, a in opts:
	if o in ("-h", "--help"):
	    print "usage: waitnofile.py <file>"


fname = args[0]
stime = 0
while os.path.exists(fname):
    stime = stime + 10;
    print fname + " still exists ! wait " + str(stime) + " seconds..."
    time.sleep(10);

