#!/usr/bin/python
# -*- coding: utf-8 -*- 


print "Content-type: text/plain;charset=utf-8\n\n"

command = "rtm --plain ls list:#NextAction "

import subprocess

p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)


lines = p.stdout.readlines()

items = []

import string
for l in lines:
    if l == "":
        continue
    if not l:
        continue
    parts = string.split(l, maxsplit=1)
    if not parts:
        continue
    first = parts[0]

    if len(parts)==0:
        continue
    try:
        int(first)
    except:
        continue

    l = " ".join(parts[1:])
    import re
    re.sub("\[.*\]", "", l)
    parts = l.split("|")
    items.append(parts[0])

num = len(items)
from random import randrange
index = randrange(num)

print items[index]
