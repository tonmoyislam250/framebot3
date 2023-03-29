#!/bin/bash
LINK=https://drive.google.com/file/d/1szSZvOG9vXj93C0WmCszEHP6-C3jG4sh/view
VIDEODIR=./videos/"Ben 10 Alien Force S01E02 Ben 10 Returns (2).mkv"
cd /usr/src/app
gdown $LINK
mkdir -pv videos && unzip -d ./videos/ -j Ben10AFS01.zip
ffmpeg -copyts -i "$VIDEO_DIR" -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1",subtitles=sub1.ass -frame_pts true -vsync vfr -q:v 5 "Sub_01/%08d.jpg" -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1" -frame_pts true -vsync vfr -q:v 5 "Raw_01/%08d.jpg"
