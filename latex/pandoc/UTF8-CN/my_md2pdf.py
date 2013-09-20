#!/usr/bin/python2
#-*-coding: utf-8 -*-
#pylint: disable=W0141, W0401, W0614

"""
my_md2pdf_cn.py <OPTIONS> <markdown_file>

DESCRITPION:
    Convert markdown to PDF

DEPENDENCIES:
    1. pandoc
    2. pdflatex
    3. latexmk
    4. strip_wikilink.py (my own script)

By: limijd@gmail.com
"""

import sys

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
gflags.DEFINE_string("output", None, "Output PDF file", GFLAGS)

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

try:
    GARGV[1]
except IndexError, e:
    print '%s\nOPTIONS:\n%s' % (__doc__, GFLAGS.MainModuleHelp())
    sys.exit(1)

import os
_SELF_PATH_ = os.path.realpath(os.path.abspath(__file__))
_SELF_DIR_ = os.path.dirname(_SELF_PATH_)

#==============================================================================
# program body
#==============================================================================
mdfile = GARGV[1]

if not GFLAGS.output:
    GFLAGS.output = mdfile

try:
    if GFLAGS.output[-4:] == ".pdf":
        GFLAGS.output=GFLAGS.output[:-4]
except:
    pass

import tempfile

tmpf = tempfile.NamedTemporaryFile(delete=False)
tmpfn = tmpf.name+".tex"
tmpf.close()
os.unlink(tmpf.name)

latex_tmpl = _SELF_DIR_ + "/latex.tmpl"
head_tmpl = _SELF_DIR_ + "/head.tex"
tail_tmpl = _SELF_DIR_ + "/tail.tex"

cmd_md2tex = "cat %s | strip_wikilink.py |pandoc --template=%s -H %s -A %s -o %s"\
    % (mdfile, latex_tmpl, head_tmpl, tail_tmpl, tmpfn)
cmd_tex2pdf = "latexmk -pdf -jobname=%s %s" % (GFLAGS.output, tmpfn)
cmd_tex2pdf_clean =  "latexmk -pdf -jobname=%s -c %s" % (GFLAGS.output, tmpfn)

import subprocess
print cmd_md2tex
subprocess.Popen(cmd_md2tex, shell=True).wait()

print cmd_tex2pdf
subprocess.Popen(cmd_tex2pdf, shell=True).wait()

print cmd_tex2pdf_clean
subprocess.Popen(cmd_tex2pdf_clean, shell=True).wait()
