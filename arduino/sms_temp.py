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
msg = u"%s - 湿度: %s, 摄氏温度: %s, 华氏温度: %s" % (now, j[u"Humi"], j[u"TempC"], j[u"TempF"])
import subprocess
#p = subprocess.Popen(["/usr/bin/sendxmpp","-t -u limijd.me.mailer.noreply -o gmail.com limijd"], stdin=subprocess.PIPE)
#p.stdin.write(msg)
#p.close()

subprocess.Popen("echo %s | sendxmpp -t -u limijd.me.mailer.noreply -o gmail.com limijd"%msg, shell=True);







