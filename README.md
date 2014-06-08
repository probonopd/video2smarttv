video2smarttv
=============

Send mp4 video URLs or YouTube videos to Samsung Smart TV. Might work with other UPnP Smart TVs too.

Usage
-----

Send a mp4 video file to the Smart TV for playing:

```
./sendSamsungVideo.py -i 192.168.0.13 http://download.wavetlan.com/SVV/Media/HTTP/H264/Talkinghead_Media/H264_test1_Talkinghead_mp4_480x360.mp4
````

If you have youtube-dl installed, you can also use YouTube IDs or search keywords instead:

```
./sendSamsungVideo.py -i 192.168.0.13 pf7BWCbGmVs
./sendSamsungVideo.py -i 192.168.0.13 "some youtube search"
```

Note, if the port on your Smart TV is not 7676, you can specify one with 

```
./sendSamsungVideo.py -i 192.168.0.13 -p 7676
````
