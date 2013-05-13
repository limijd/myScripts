#!/usr/bin/python2
#-*-coding: utf-8 -*-
#pylint: disable=W0141, W0401, W0614

"""
Translate arduino serial data to JSON structurize data. So other applications 
can be developped based on the JSON data.

DESCRITPION:
    arduino_app_layer.py --port=<port> --serial_port=<port_device>

By: limijd@gmail.com
"""

import sys
import time
import json

from socket import *
import threading
import thread

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
gflags.DEFINE_integer("port", None, "Specify server port", flag_values=GFLAGS)
gflags.DEFINE_string("serial_port", None, "Specify serial device ", flag_values=GFLAGS)

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

if not GFLAGS.port or not GFLAGS.serial_port:
    print "You need to specify --port and --serial_port."
    print ""
    print '%s\nOPTIONS:\n%s' % (__doc__, GFLAGS.MainModuleHelp())
    sys.exit(0)

#==============================================================================
# program body
#==============================================================================

import serial

ser = serial.Serial(GFLAGS.serial_port, 115200)

oneObj = {}

class Factory:
    def __init__(self):
        pass

    def createDataObj(self, line):
        if line.find("TempC")>=0:
            return TempHumiSensor.createObj(line)

    def createErrorObj(self, err):
        return {"type":"Error", "message":err, "utc_sec":time.time()}

class TempHumiSensor:
    def __init__(self, d):
        self.d = d
        pass

    @staticmethod
    def createObj(line):
        import re
        parts = re.split('[,:]', line)
        parts = map(lambda x:x.strip(), parts)
        if len(parts)!=6:
            obj = factory.createErrorObj("read line: %s" % line)
            return obj

        try:
            humi = float(parts[5]) * 0.78
            humi = "%0.2f" % humi
            d = {"type":TempHumiSensor.__name__, "TempC":parts[1], "TempF":parts[3], "Humi":humi}
            d["utc_sec"]=time.time()
            obj = TempHumiSensor(d)
            return obj
        except:
            print parts
            assert(False)

    def __repr__(self):
        return json.dumps(self.d)

locker = threading.Lock()
dataQ = []
 
def forever_read_devcie():
    factory = Factory()

    #skip first line
    ser.readline()

    while True:
        try:
            line = ser.readline()
        except Exception, e:
            import time
            obj = factory.createErrorObj(e.__repr__())
            time.sleep(0.1)
            print "sleep 0.1s"
            continue
        except:
            import time
            obj = factory.createErrorObj("device read error")
            time.sleep(0.1)
            print "sleep 0.1s"
            continue

        #parse line
        obj = factory.createDataObj(line)
        if obj:
            locker.acquire()
            if len(dataQ) > 1000:
                dataQ.pop()
                dataQ.append(obj)
            else:
                dataQ.append(obj)
            locker.release()

t = threading.Thread(target=forever_read_devcie)
t.daemon = True
t.start()

def server_handler(clientsock,addr):
    tries = 0
    while 1:
        req_type = clientsock.recv(BUFSIZ)
        if not req_type:
            break

        req_type = req_type.strip()
        print "Thanks! Preparing data for %s" % req_type

        while True:
            locker.acquire()
            for i in xrange(len(dataQ),0,-1):
                obj = dataQ[i-1]
                jobj = json.loads(obj.__repr__())
                if jobj["type"]==req_type:
                    print "Sending data: %s" % obj.__repr__()
                    clientsock.send(obj.__repr__())
                    clientsock.close()
                    locker.release()
                    return
            locker.release()
            print "...",

            tries = tries + 1
            time.sleep(0.1)

            if tries>=10:
                clientsock.send(json.dumps({"type":"NO_DATA"}))
                clientsock.close()
                return

    clientsock.send(json.dumps({"type":"WRONG_COMMAND"}))
    clientsock.close()
    return


if __name__=='__main__':
    HOST = 'localhost'
    PORT = GFLAGS.port
    BUFSIZ = 10240
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(2)

    clients = []
    while 1:
        print 'Waiting for connection at port: %d ...' % PORT
        clientsock, addr = serversock.accept()
        clients.append(clientsock)
        print '...Connected from: %s' % addr.__repr__()
        thread.start_new_thread(server_handler, (clientsock, addr))

    print "Closing server."
    for client in clients:
        client.close()
    serversock.close()
