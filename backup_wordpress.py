#!/usr/bin/env python
#-*-coding: utf-8 -*-
#pylint: disable=W0141,W0702,C0103

"""
backup_wordpress.py [--noincrmental]  --wp_site=<YOUR_BLOG_SITE> \
--wp_uname=<USERNAME> --wp_passwd=<PASSWORD> --output_dir=<BACKUP_DIR> 

DESCRITPION:
    Backup wordpress blog posts to json text files into local directory.

    Each post will be saved to a file with the post title as filename. 
    However, if there are some invalid charaters in the title like "/",
    the filename will be transformed to URL format.

    An additionl markdown file will also be saved if the post was originall
    created by vimrepress. However, even a usual HTML post, the script 
    will try to translate it to markdown format by python "html2text" 
    module.

AUTHOR:
    limijd@gmail.com 
    http://blog.limijd.me
"""

import sys
import gflags

if __name__ != "__main__":
    sys.exit(0)

#==============================================================================
# Option handling
#==============================================================================
GFLAGS = gflags.FlagValues()
gflags.DEFINE_boolean("help", False, "print help information", GFLAGS)
gflags.DEFINE_string("wp_site", None, "Your wordpress blog site", GFLAGS)
gflags.DEFINE_string("wp_uname", None, "Your wordpress username", GFLAGS)
gflags.DEFINE_string("wp_passwd", None, "Your wordpress password", GFLAGS)
gflags.DEFINE_string("output_dir", None, "The directory where your posts \
        will be backed up to.", GFLAGS)
gflags.DEFINE_bool("noincremental", False, "Backup all posts not matter "\
    "whether they have been backed up before." , GFLAGS)

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

if not GFLAGS.wp_site or not GFLAGS.wp_uname or not GFLAGS.wp_passwd \
    or not GFLAGS.output_dir:
    print '%s\nOPTIONS:\n%s' % (__doc__, GFLAGS.MainModuleHelp())
    sys.exit(1)

#==============================================================================
# program body
#==============================================================================
import urllib
import xmlrpclib
import os
import json
import binascii
try:
    import html2text
except:
    print \
""" 
Warning: python package html2ext is required to transform HTML blogs 
to markdown format if the original post was not created by vimrepress.

"""

_CAN_BE_ANY_VALUE_ = 1
_MAX_INT_ = 100000000

backup_posts = []
xmlrpc_obj = xmlrpclib.ServerProxy(os.path.join(GFLAGS.wp_site, "xmlrpc.php"))
all_posts_titles = getattr(xmlrpc_obj, "mt.getRecentPostTitles") \
    (_CAN_BE_ANY_VALUE_, GFLAGS.wp_uname, GFLAGS.wp_passwd, _MAX_INT_)

for post in all_posts_titles:
    for post_key in post.keys():
        value = post[post_key]
        try:
            post[post_key] = value.encode("utf-8")
        except:
            post[post_key] = value.__str__()
        post_title =  post["title"].strip().strip("\n").replace \
            ("/","_0x%s_"%binascii.hexlify("/"))
        post_id = post["postid"]

    save_to_fname = os.path.abspath(GFLAGS.output_dir + \
        "/%04d - "%int(post_id) + post_title + ".json")

    if not GFLAGS.noincremental:
        if not os.path.exists(save_to_fname):
            backup_posts.append([post, save_to_fname])
    else:
        backup_posts.append([post, save_to_fname])

print "\nWriting the index json: %s\n" % "index.json"
fp = open(os.path.abspath(GFLAGS.output_dir + "/index.json" ), "w")
json.dump(all_posts_titles, fp, ensure_ascii=False, indent=4)
fp.close()

if len(backup_posts)==0:
    #nothing need to be saved.
    print \
""" 
There is no new post need to be backed up!
If you want to backup all the posts again. Please use option:
    --noincremental 

"""
    sys.exit(0)

for backup in backup_posts:
    post = backup[0]
    fname = backup[1]
    fname_md = fname + ".md"

    blog_post = getattr(xmlrpc_obj, "metaWeblog.getPost")(post["postid"]\
        , GFLAGS.wp_uname, GFLAGS.wp_passwd)

    #get markdown data created by vimrepress
    md_text = None
    try:
        if blog_post["custom_fields"][0]["key"] == "mkd_text":
            md_text = blog_post["custom_fields"][0]["value"].encode("utf-8")
    except:
        pass

    #if markdown data doesn't exist, them translate the html to markdown
    #python module "html2text" is required.
    html_text = blog_post["description"]
    if not md_text and  html_text:
        try:
            md_text = html2text.html2text(html_text).encode("utf-8")
        except:
            pass

    #save the markdown file
    if md_text:
        fp = open(fname_md, "w")
        fp.write(md_text)
        fp.close()

    #textize
    try:
        blog_post["categories"] = ",".join(blog_post["categories"])
    except:
        pass
    for kw in blog_post.keys():
        try:
            blog_post[kw] = blog_post[kw].encode("utf-8")
        except:
            blog_post[kw] = blog_post[kw].__str__()

    #save the blog post to json text file.
    print "Save %04d - %s" % (int(post["postid"]), post["title"])
    try:
        fp = open(fname, "w")
    except:
        fname = urllib.quote(fname)
        fp = open(fname, "w")
    json.dump(blog_post, fp,  ensure_ascii=False, indent=4)
    fp.close()

print "Done. Thanks!"

