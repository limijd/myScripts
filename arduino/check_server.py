#!/usr/bin/python

import socket,time

s=socket.socket(socket.AF_INET)
s.connect(("localhost",21599))
s.sendall("TempHumiSensor")
print s.recv(10240)
s.close()
