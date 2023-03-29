#!/bin/bash
pwd && ls -a
LINK="https://drive.google.com/uc?id=1szSZvOG9vXj93C0WmCszEHP6-C3jG4sh"
VIDEO_DIR= "./videos"
VIDEO_NAME= "Ben 10 Alien Force S01E02 Ben 10 Returns (2).mkv"
cd /usr/src/app
gdown $LINK
file ben10AFS01.zip
mkdir -pv videos && unzip -d ./videos/ -j ben10AFS01.zip
ls -a
ffmpeg -copyts -i "$VIDEO_DIR/$VIDEO_NAME" -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1",subtitles=sub1.ass -frame_pts true -vsync vfr -q:v 5 "Sub_01/%08d.jpg" -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1" -frame_pts true -vsync vfr -q:v 5 "Raw_01/%08d.jpg"
