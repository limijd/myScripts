#!/usr/bin/env python
#-*-coding: utf-8 -*-

"""
Catch new process with the specific name 

usage:
show_new_process <procname>

"""

import os
import sys
import getopt
import time

if __name__ != "__main__":
    sys.exit(0);

ARGV = {
    "procname="    : None,
}

opts, args  = getopt.getopt(sys.argv[1:], "h", (["help"]+ARGV.keys()))
for o, a in opts:
    if o in ("-h", "--help"):
        print __doc__
        sys.exit(1)
    if a:
        ARGV[o[2:]+"="] = a
    else:
        ARGV[o[2:]] = True


import subprocess
class OnePs:
    def __init__(self, procname):
        command = "ps -u %s " % os.environ["USER"]
        p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (pin, pout, perr) = (p.stdin, p.stdout, p.stderr)
        output = pout.readlines()
        status = pout.close()
        perr.close()
        pin.close()

        self.output = output
        self.procname = procname
        self.result = {}

        self.analyze()

    def analyze(self):
        for l in self.output:
            parts = l.split()
            proc = parts[3]
            self.result[parts[0]] = proc

    def getResult(self):
        return self.result        

    def showNewResult(self, result):
        for k in self.result.keys():
            if not k in result.keys():
                if self.procname:
                    if self.result[k] == self.procname:
                        print  "NEW PROCESS by %s: %s %s" % (os.environ["USER"], k, self.result[k])
                else:
                    if self.result[k] != "ps":
                        print  "NEW PROCESS by %s: %s %s" % (os.environ["USER"], k, self.result[k])


            

prevPs = None
currPs = None

while True:
    prevPs = currPs
    currPs = OnePs(ARGV["procname="])

    if prevPs and currPs:
        currPs.showNewResult(prevPs.getResult())
    time.sleep(1)


        


