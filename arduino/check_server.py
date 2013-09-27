#!/usr/bin/python
#-*-coding: utf-8 -*-

import socket,time
import json

s=socket.socket(socket.AF_INET)
s.connect(("localhost",21599))
s.sendall("TempHumiSensor")
j = json.loads(s.recv(10240))
s.close()

import datetime
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print u"%s - 湿度: %s, 温度: %s" % (now, j[u"Humi"], j[u"TempC"])


