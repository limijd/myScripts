#!/usr/bin/env python3
#-*-coding: utf-8 -*-
import re
import os
import sys
import requests
from bs4 import BeautifulSoup
url = sys.argv[1]

url = %sys.argv[1]
req = requests.get(url)
req.encoding="gb2312"
content = req.text

soup=BeautifulSoup(req.text, features="html.parser")
content = soup.find("div", {"id": "myContent"})

s = re.sub("�", "", s)
new_html = "%s - %sl"%(submit_date, sys.argv[1])
fp = open(new_html, "w")
fp.write("<html><body>\n")
fp.write('<META http-equiv=Content-Type content="text/html; charset=utf-8">\n')
fp.write(s)
fp.write("</body></html>\n")
fp.close()


os.remove(sys.argv[1])
