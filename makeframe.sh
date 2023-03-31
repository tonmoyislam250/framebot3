#!/bin/bash
pwd && ls -a
cd /usr/src/app
gdown $LINK
mkdir -pv videos/sub
mkdir -pv videos/raw \
&& unzip -d ./videos/ -j ${VIDEO_NAME}.zip
ls -a videos/sub && ls -a videos && uchardet videos/${VIDEO_NAME}.srt
rm -rf videos/raw/* && rm -rf videos/sub/*
ffmpeg -sub_charenc $(uchardet videos/${VIDEO_NAME}.srt) -i videos/${VIDEO_NAME}.srt videos/${VIDEO_NAME}.ass
ffmpeg -copyts -i \
       "./videos/${VIDEO_NAME}.mp4" \
       -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1",subtitles=videos/${VIDEO_NAME}.ass \
       -frame_pts true -vsync vfr -q:v 5 "videos/sub/%08d.jpg" \
       -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1" -frame_pts true \
       -vsync vfr -q:v 5 "videos/raw/%08d.jpg"

python3 yafot-facebook.py --page-id $PAGE_ID --pdir "videos/sub/" --token $ACCESS_TOKEN --start $START --count 1800 --delay 60
