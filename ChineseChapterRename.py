#! /usr/bin/env python3
#-*-coding: utf-8 -*-

import os
import glob 
import re
import cn2an

for fn in glob.glob("*.mp3"):
    m = re.match('第[零一二三四五六七八九十百千]+回', fn, re.UNICODE)
    if not m:
        continue
    m = m.group(0)
    cn = m[1:-1]
    an = cn2an.cn2an(cn)

    sfn = re.sub('第[零一二三四五六七八九十百千]+回', '', fn, re.UNICODE)
    sfn = sfn.strip()

    newfn = "第%03d回 - %s" %(an, sfn)
    print(newfn)
    os.rename(fn, newfn)


