#!/bin/bash

# IP of Raspberry Pi
TARGET_IP="192.168.0.154"

ffmpeg \
-f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 \
-f alsa -i default \
-vcodec libx264 -preset ultrafast -tune zerolatency \
-acodec aac -ar 44100 -b:a 128k \
-f mpegts udp://$TARGET_IP:1234

