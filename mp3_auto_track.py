#! /usr/bin/env python3
#-*-coding: utf-8 -*-

import os
import sys
import glob 
import re
import cn2an

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER

strip_str = sys.argv[1]
total_track = int(sys.argv[2])

for fn in glob.glob("*.mp3"):
    m = re.search('[0-9]+', fn, re.UNICODE)
    if not m:
        continue
    m = m.group(0)
    an = int(m)

    sfn = re.sub('%s[0-9]+'%strip_str, '', fn, re.UNICODE)
    sfn = sfn.strip()

    newfn = "%03d - %s" %(an, sfn)
    print(newfn)
    os.rename(fn, newfn)

    mp3 = MP3(newfn, ID3=EasyID3)
    mp3['album'] = [strip_str]
    mp3['tracknumber'] = "%d/%d"%(an, total_track)
    mp3.save()

