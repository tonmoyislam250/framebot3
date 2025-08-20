#!/bin/bash
pwd && ls -a

cd /usr/src/app
mkdir -p RAW
gdown $LINK
unzip -q -d RAW/ "$VIDEO_NAME.zip"
TOTAL_COUNT=$(ls RAW/ | wc -l)
python3 post.py --page-id $PAGE_ID --pdir "RAW/" --token $ACCESS_TOKEN --start $START --count $TOTAL_COUNT --delay 60