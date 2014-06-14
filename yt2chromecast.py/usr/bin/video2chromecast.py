#!/usr/bin/python

import time, sys

if(len(sys.argv) > 0):
    video = sys.argv[1]
else:
    video = "REjj1ruFQww"

try:
    import pychromecast
    pychromecast.play_youtube_video(video, pychromecast.PyChromecast().host)
except:
    pass
