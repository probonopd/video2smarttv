video2smarttv
=============

Send mp4 video URLs or YouTube videos to Samsung Smart TV using UPnP, DLNA. This is a no-frills implementation intended to be as lightweight and portable as possible. Hence, it does not use any XML, SOAP, or UPnP libraries. Might work with other UPnP Smart TVs too.

Prerequisites
-------------

Python 2.7, should come preinstalled with OS X and most Linux distributions. Optionally, [youtube-dl](http://rg3.github.io/youtube-dl/download.html).

Installation
------------

Just download and make executable. This is just one Python file.

```
wget https://raw.githubusercontent.com/probonopd/video2smarttv/master/video2smarttv.py
chmod a+x ./video2smarttv.py
sudo wget https://yt-dl.org/downloads/2014.06.07/youtube-dl -O /usr/local/bin/youtube-dl # Optional
sudo chmod a+x /usr/local/bin/youtube-dl # Optional

````

Usage
-----

Send a mp4 video file to the Smart TV for playing by specifying the IP address of the TV and the URL to be played:

```
./video2smarttv.py -i 192.168.0.13 http://download.wavetlan.com/SVV/Media/HTTP/H264/Talkinghead_Media/H264_test1_Talkinghead_mp4_480x360.mp4
````

If you have youtube-dl installed, you can also use YouTube IDs or search keywords instead:

```
./video2smarttv.py -i 192.168.0.13 pf7BWCbGmVs
./video2smarttv.py -i 192.168.0.13 "some youtube search"
```

Note, if the port on your Smart TV is not 7676, you can specify one with 

```
./video2smarttv.py -i 192.168.0.13 -p 7676
````
